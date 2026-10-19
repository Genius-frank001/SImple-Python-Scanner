#!/usr/bin/env python3
"""pyscan v0.1 - async TCP connect scanner with banner grabbing.
Only scan hosts you own or have written permission to test."""
import argparse
import asyncio
import json
import socket
import time


def normalize_host(target: str) -> str:
    """'http://example.com:8080/path' -> 'example.com'."""
    if "://" in target:
        target = target.split("://", 1)[1]
    return target.split("/", 1)[0].split(":", 1)[0]


def parse_ports(spec: str) -> list[int]:
    """'22,80,8000-8100' -> sorted list of unique ports."""
    ports = set()
    for part in spec.split(","):
        if "-" in part:
            lo, hi = part.split("-", 1)
            ports.update(range(int(lo), int(hi) + 1))
        else:
            ports.add(int(part))
    if not all(0 < p < 65536 for p in ports):
        raise ValueError("ports must be between 1 and 65535")
    return sorted(ports)


async def scan_port(host: str, port: int, timeout: float, sem: asyncio.Semaphore):
    async with sem:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout
            )
        except (asyncio.TimeoutError, OSError):
            return None  # closed or filtered (v0.2: distinguish these)
        banner = ""
        try:
            data = await asyncio.wait_for(reader.read(128), 1.0)
            banner = data.decode(errors="replace").strip()
        except (asyncio.TimeoutError, OSError):
            pass  # many services stay silent until probed (v0.2: add probes)
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except OSError:
                pass
        return {"port": port, "state": "open", "banner": banner}


async def main(args):
    host = normalize_host(args.host)
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        raise SystemExit(f"error: cannot resolve '{host}' (check spelling/DNS)")
    args.host = host
    ports = parse_ports(args.ports)
    sem = asyncio.Semaphore(args.concurrency)
    start = time.perf_counter()
    results = await asyncio.gather(
        *(scan_port(ip, p, args.timeout, sem) for p in ports)
    )
    open_ports = [r for r in results if r]
    report = {
        "target": args.host,
        "ip": ip,
        "scanned": len(ports),
        "open": open_ports,
        "seconds": round(time.perf_counter() - start, 2),
    }
    if args.json:
        with open(args.json, "w") as f:
            json.dump(report, f, indent=2)
    for r in open_ports:
        print(f"{r['port']:>5}/tcp open  {r['banner'][:60]}")
    print(f"\n{len(open_ports)} open of {len(ports)} in {report['seconds']}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        prog="scanner.py",
        description="Async TCP connect scanner with banner grabbing.",
        epilog=(
            "examples:\n"
            "  python3 scanner.py 127.0.0.1\n"
            "  python3 scanner.py scanme.nmap.org -p 22,80,443\n"
            "  python3 scanner.py 192.168.56.101 -p 1-65535 -c 1000 -o report.json\n\n"
            "Only scan systems you own or have written permission to test."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("host", help="target hostname or IPv4 address")
    ap.add_argument("-p", "--ports", default="1-1024",
                    help="ports: single, comma list, ranges (default: 1-1024)")
    ap.add_argument("-c", "--concurrency", type=int, default=500,
                    help="max simultaneous connections (default: 500)")
    ap.add_argument("-t", "--timeout", type=float, default=1.0,
                    help="connect timeout in seconds (default: 1.0)")
    ap.add_argument("-o", "--json", metavar="FILE",
                    help="write JSON report to FILE")
    asyncio.run(main(ap.parse_args()))
