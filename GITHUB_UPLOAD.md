# Uploading pyscan to GitHub

## One-time setup
1. Create an account at github.com and install Git (`git --version` to check).
2. Set your identity:
   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

## Create the repo
1. GitHub > **New repository**. Name: `pyscan`. Public. Do NOT tick "Add README/.gitignore/license" (you already have them).
2. Add a description and topics: `python`, `asyncio`, `port-scanner`, `pentesting`, `security-tools`.

## Push the code
From the `pyscan` folder:
```
git init
git add .
git commit -m "Initial commit: async TCP scanner v0.1"
git branch -M main
git remote add origin https://github.com/<your-username>/pyscan.git
git push -u origin main
```
If prompted for a password, use a Personal Access Token (GitHub > Settings > Developer settings > Tokens), or authenticate with `gh auth login`.

## Before you push, check
- No real client IPs, hostnames, or scan results in the repo.
- The legal notice is in the README.
- Your name is in LICENSE.

## After the first push
- Tag releases: `git tag v0.1.0 && git push --tags`
- Commit small and often with clear messages (`feat:`, `fix:`, `docs:`).
- Add a `tests/` folder and a screenshot or sample output to the README.
