# IOC Update Scripts

This directory contains scripts for automatically updating IOC (Indicators of Compromise) definitions.

## Shai-Hulud IOC Auto-Update

The `update_shai_hulud_iocs.py` script automatically downloads the latest Shai-Hulud 2.0 package list from Wiz Research and updates the local IOC definitions.

### Usage

**Via CLI (Recommended):**
```bash
python3 -m src.github_ioc_scanner.cli --update-iocs
```

**Via Script:**
```bash
python3 scripts/update_shai_hulud_iocs.py
```

### What it does

1. Downloads the latest CSV from: https://github.com/wiz-sec-public/wiz-research-iocs
2. Parses the package names and versions
3. Generates a Python IOC file at `src/github_ioc_scanner/issues/shai_hulud_2.py`
4. Includes metadata (source, last updated, references)

### Automation

You can automate this with a cron job or GitHub Action:

**Cron (daily at 2 AM):**
```bash
0 2 * * * cd /path/to/github-ioc-scanner && python3 scripts/update_shai_hulud_iocs.py
```

**GitHub Action (weekly):**
```yaml
name: Update Shai-Hulud IOCs
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Update IOCs
        run: python3 scripts/update_shai_hulud_iocs.py
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: 'chore: update Shai-Hulud IOCs'
          title: 'Update Shai-Hulud IOC Definitions'
          body: 'Automated update of Shai-Hulud 2.0 IOC definitions from Wiz Research'
          branch: update-shai-hulud-iocs
```

### After Update

1. Review changes: `git diff src/github_ioc_scanner/issues/shai_hulud_2.py`
2. Run tests: `pytest tests/`
3. Commit: `git add src/github_ioc_scanner/issues/shai_hulud_2.py && git commit -m "Update Shai-Hulud IOCs"`

### Source

- **Wiz Research IOCs**: https://github.com/wiz-sec-public/wiz-research-iocs
- **Shai-Hulud 2.0 Report**: https://www.wiz.io/blog/shai-hulud-2-0-ongoing-supply-chain-attack
