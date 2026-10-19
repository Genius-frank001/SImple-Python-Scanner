# pyscan

Async TCP connect scanner with banner grabbing, written in pure Python (stdlib only).

> **Legal notice:** only scan systems you own or have explicit written permission to test. Unauthorized scanning may be illegal.

## Features
- Concurrent TCP connect scanning (asyncio)
- Port specs: single, comma list, ranges (`22,80,8000-8100`)
- Banner grabbing for services that speak first (SSH, FTP, SMTP)
- JSON report output

## Requirements
Python 3.9+. No third-party packages.

## Usage
```
python3 scanner.py <host> [-p PORTS] [-c CONCURRENCY] [-t TIMEOUT] [-o FILE]
```

| Option | Description | Default |
|---|---|---|
| `host` | Target hostname or IPv4 address | required |
| `-p, --ports` | Ports to scan | `1-1024` |
| `-c, --concurrency` | Max simultaneous connections | `500` |
| `-t, --timeout` | Connect timeout (seconds) | `1.0` |
| `-o, --json FILE` | Write JSON report | off |

### Examples
```
python3 scanner.py 127.0.0.1
python3 scanner.py scanme.nmap.org -p 22,80,443
python3 scanner.py 192.168.56.101 -p 1-65535 -c 1000 -o report.json
```

### Sample output
```
 8765/tcp open  

1 open of 11 in 1.01s
```

## Limitations (v0.1)
- Cannot distinguish closed from filtered ports
- No protocol probes: HTTP and other silent services show empty banners
- IPv4 only, single host

## Roadmap
- [ ] v0.2: closed vs filtered, protocol probes, service names
- [ ] v0.3: CIDR/multi-host, rate limiting, progress
- [ ] v0.4: CSV/HTML output, tests
- [ ] v0.5: banner fingerprint database

## License
MIT
