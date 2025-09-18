# Usage Examples

This document provides comprehensive examples of using the GitHub IOC Scanner in various scenarios and use cases.

## Basic Usage Examples

### Security Analyst Daily Workflow
```bash
# Quick daily scan (quiet mode - only shows threats)
github-ioc-scan --org mycompany --quiet

# Comprehensive weekly audit
github-ioc-scan --org mycompany --log-file weekly-audit-$(date +%Y%m%d).log

# Emergency threat investigation (verbose mode)
github-ioc-scan --org mycompany --team critical-services --verbose
```

### Simple Organization Scan
```bash
# Scan all repositories in an organization (professional output)
github-ioc-scan --org mycompany

# Example output:
============================================================
GitHub IOC Scanner - Security Analysis Report
============================================================
Target: Organization 'mycompany'
Configuration: Comprehensive mode (all files), Excluding archived repositories
IOC Database: 372 threat indicators loaded
Scan initiated: 2025-09-17 13:11:40
------------------------------------------------------------
✅ SCAN COMPLETE - No threats detected
   All scanned packages are clean
------------------------------------------------------------
SCAN STATISTICS:
  Repositories scanned: 15
  Files analyzed: 127
Scan completed: 2025-09-17 13:11:40
============================================================
```

### Team-Specific Scanning
```bash
# Scan repositories belonging to a specific team
github-ioc-scan --org mycompany --team security-team

# Scan multiple teams (run separately)
github-ioc-scan --org mycompany --team frontend-team
github-ioc-scan --org mycompany --team backend-team
```

### Single Repository Scan
```bash
# Scan a specific repository
github-ioc-scan --org mycompany --repo critical-app

# Scan your own repository
github-ioc-scan --org yourusername --repo your-project
```

## Advanced Scanning Options

### Fast Mode Scanning
```bash
# Quick scan of root-level files only
github-ioc-scan --org mycompany --fast

# Fast scan of specific repository
github-ioc-scan --org mycompany --repo large-monorepo --fast
```

### Including Archived Repositories
```bash
# Include archived repositories in scan
github-ioc-scan --org mycompany --include-archived

# Fast scan including archived repos
github-ioc-scan --org mycompany --fast --include-archived
```

## Authentication Examples

### Using Environment Variable
```bash
# Set GitHub token
export GITHUB_TOKEN="ghp_your_token_here"

# Run scan
github-ioc-scan --org mycompany
```

### Using GitHub CLI
```bash
# Authenticate with GitHub CLI
gh auth login

# Tool automatically uses gh auth token
github-ioc-scan --org mycompany
```

### Verifying Authentication
```bash
# Check if token is working
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check rate limit status
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

## IOC Definition Examples

### Basic IOC File
```python
# issues/basic_threats.py
IOC_PACKAGES = {
    # Specific compromised versions
    "event-stream": ["3.3.4"],
    "eslint-scope": ["3.7.2"],
    
    # Any version is suspicious
    "malicious-package": None,
    
    # Multiple compromised versions
    "ua-parser-js": ["0.7.29", "0.8.0", "1.0.0"],
}
```

### Language-Specific IOC Files
```python
# issues/npm_threats.py - JavaScript/Node.js packages
IOC_PACKAGES = {
    "colors": ["1.4.1", "1.4.2"],
    "faker": ["6.6.6"],
    "node-ipc": ["9.2.2", "10.1.1", "10.1.2"],
}

# issues/python_threats.py - Python packages
IOC_PACKAGES = {
    "ctx": None,  # Typosquatting attack
    "codecov": ["2.1.11"],
    "urllib3": ["1.26.5"],
}

# issues/ruby_threats.py - Ruby gems
IOC_PACKAGES = {
    "strong_password": ["0.0.7"],
    "rest-client": ["1.6.10"],
}
```

### Typosquatting Detection
```python
# issues/typosquatting.py
IOC_PACKAGES = {
    # Common npm typos
    "reqeust": None,      # request typo
    "expres": None,       # express typo
    "loadsh": None,       # lodash typo
    
    # Python typos
    "requsts": None,      # requests typo
    "numpay": None,       # numpy typo
    "djago": None,        # django typo
    
    # Cross-language typos
    "beautifulsoup": None,
    "crytography": None,
}
```

## Real-World Scenarios

### Security Audit Workflow
```bash
# 1. Initial fast assessment
github-ioc-scan --org mycompany --fast

# 2. Deep scan of critical repositories
github-ioc-scan --org mycompany --repo production-api
github-ioc-scan --org mycompany --repo user-frontend
github-ioc-scan --org mycompany --repo payment-service

# 3. Team-based detailed scanning
github-ioc-scan --org mycompany --team security-team
github-ioc-scan --org mycompany --team infrastructure-team

# 4. Comprehensive organization scan
github-ioc-scan --org mycompany
```

### Incident Response
```bash
# Quick check for specific IOC across all repos
# Add new IOC to issues/ directory first
echo 'IOC_PACKAGES = {"suspicious-package": ["1.2.3"]}' > issues/incident_response.py

# Scan entire organization
github-ioc-scan --org mycompany

# Clean up after incident
rm issues/incident_response.py
```

### Continuous Monitoring
```bash
# Daily security scan (cron job)
#!/bin/bash
export GITHUB_TOKEN="your_token"
github-ioc-scan --org mycompany --fast > /var/log/ioc-scan-$(date +%Y%m%d).log

# Weekly comprehensive scan
#!/bin/bash
export GITHUB_TOKEN="your_token"
github-ioc-scan --org mycompany > /var/log/ioc-scan-full-$(date +%Y%m%d).log
```

## CI/CD Integration Examples

### GitHub Actions
```yaml
# .github/workflows/security-scan.yml
name: IOC Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  ioc-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install IOC Scanner
      run: |
        git clone https://github.com/your-org/github-ioc-scanner.git
        cd github-ioc-scanner
        pip install -e .
    
    - name: Run IOC Scan
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        github-ioc-scan --org ${{ github.repository_owner }} --repo ${{ github.event.repository.name }}
```

### GitLab CI
```yaml
# .gitlab-ci.yml
ioc-scan:
  stage: security
  image: python:3.9
  before_script:
    - git clone https://github.com/your-org/github-ioc-scanner.git
    - cd github-ioc-scanner && pip install -e .
  script:
    - github-ioc-scan --org $CI_PROJECT_NAMESPACE --repo $CI_PROJECT_NAME
  variables:
    GITHUB_TOKEN: $GITHUB_ACCESS_TOKEN
  only:
    - main
    - merge_requests
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        GITHUB_TOKEN = credentials('github-token')
    }
    
    stages {
        stage('IOC Scan') {
            steps {
                sh '''
                    git clone https://github.com/your-org/github-ioc-scanner.git
                    cd github-ioc-scanner
                    pip install -e .
                    github-ioc-scan --org mycompany --repo ${JOB_NAME}
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'ioc-scan-results.log', allowEmptyArchive: true
        }
    }
}
```

## Output Processing Examples

### Parsing Results in Scripts
```bash
#!/bin/bash
# Save results to file
github-ioc-scan --org mycompany > scan_results.txt

# Check if any IOCs were found
if grep -q "|" scan_results.txt; then
    echo "IOCs found! Alerting security team..."
    # Send alert (email, Slack, etc.)
    cat scan_results.txt | mail -s "IOC Alert" security@company.com
else
    echo "No IOCs found."
fi

# Extract just the IOC matches (ignore cache stats)
grep "|" scan_results.txt > ioc_matches.txt
```

### JSON Output Processing
```bash
# Convert output to structured format for processing
github-ioc-scan --org mycompany | grep "|" | while IFS='|' read -r repo file package version; do
    echo "{\"repo\":\"$repo\", \"file\":\"$file\", \"package\":\"$package\", \"version\":\"$version\"}"
done > ioc_results.json
```

### Integration with Security Tools
```python
#!/usr/bin/env python3
# Process IOC scan results and send to SIEM
import subprocess
import json
import requests

def run_ioc_scan(org):
    result = subprocess.run(['github-ioc-scan', '--org', org], 
                          capture_output=True, text=True)
    return result.stdout

def parse_results(output):
    iocs = []
    for line in output.split('\n'):
        if '|' in line and 'Cache Statistics' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) == 4:
                iocs.append({
                    'repo': parts[0],
                    'file': parts[1], 
                    'package': parts[2],
                    'version': parts[3]
                })
    return iocs

def send_to_siem(iocs):
    for ioc in iocs:
        # Send to your SIEM/security platform
        requests.post('https://siem.company.com/api/alerts', json=ioc)

# Main execution
if __name__ == '__main__':
    output = run_ioc_scan('mycompany')
    iocs = parse_results(output)
    if iocs:
        send_to_siem(iocs)
        print(f"Sent {len(iocs)} IOC alerts to SIEM")
    else:
        print("No IOCs found")
```

## Performance Optimization Examples

### Large Organization Scanning
```bash
# Strategy for organizations with 1000+ repositories

# 1. Fast initial assessment
time github-ioc-scan --org large-company --fast

# 2. Parallel team scanning
github-ioc-scan --org large-company --team team1 &
github-ioc-scan --org large-company --team team2 &
github-ioc-scan --org large-company --team team3 &
wait

# 3. Cache warm-up for future scans
github-ioc-scan --org large-company

# 4. Subsequent scans are very fast due to caching
time github-ioc-scan --org large-company  # Should be <30 seconds
```

### Cache Management
```bash
# Check cache performance
github-ioc-scan --org mycompany | tail -1

# Expected output for good cache performance:
# Cache Statistics: Hits: 245, Misses: 12, Time Saved: 45.7s

# Clear cache if performance degrades
rm -rf ~/.cache/github-ioc-scan/

# Rebuild cache
github-ioc-scan --org mycompany
```

## Troubleshooting Examples

### Authentication Issues
```bash
# Test GitHub token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check token scopes
curl -H "Authorization: token $GITHUB_TOKEN" -I https://api.github.com/user | grep -i x-oauth-scopes

# Use GitHub CLI as fallback
gh auth login
github-ioc-scan --org mycompany
```

### Rate Limit Management
```bash
# Check current rate limit
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit

# Monitor rate limit during scan
watch -n 30 'curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit | jq .rate'
```

### IOC Definition Validation
```bash
# Validate IOC file syntax
python -m py_compile issues/my_iocs.py

# Test IOC loading
python -c "
import sys
sys.path.append('issues')
import my_iocs
print(my_iocs.IOC_PACKAGES)
"
```

## Integration Examples

### Slack Notifications
```bash
#!/bin/bash
# Slack webhook integration
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

results=$(github-ioc-scan --org mycompany)
ioc_count=$(echo "$results" | grep -c "|")

if [ $ioc_count -gt 0 ]; then
    message="🚨 IOC Alert: Found $ioc_count indicators in organization repositories"
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"$message\"}" \
        $SLACK_WEBHOOK
fi
```

### Email Alerts
```bash
#!/bin/bash
# Email notification script
results=$(github-ioc-scan --org mycompany)

if echo "$results" | grep -q "|"; then
    echo "$results" | mail -s "IOC Scan Results - $(date)" security@company.com
fi
```

### Jira Integration
```python
#!/usr/bin/env python3
# Create Jira tickets for IOC findings
import subprocess
import requests
from requests.auth import HTTPBasicAuth

def create_jira_ticket(ioc_data):
    jira_url = "https://company.atlassian.net"
    auth = HTTPBasicAuth("user@company.com", "api_token")
    
    issue_data = {
        "fields": {
            "project": {"key": "SEC"},
            "summary": f"IOC Found: {ioc_data['package']} in {ioc_data['repo']}",
            "description": f"Package: {ioc_data['package']}\nVersion: {ioc_data['version']}\nFile: {ioc_data['file']}",
            "issuetype": {"name": "Security Issue"}
        }
    }
    
    response = requests.post(f"{jira_url}/rest/api/2/issue/", 
                           json=issue_data, auth=auth)
    return response.json()

# Run scan and create tickets for findings
# (Implementation similar to previous SIEM example)
```

## Custom IOC Sources

### CVE Database Integration
```python
# issues/cve_based_iocs.py
# Generated from CVE database
IOC_PACKAGES = {
    # CVE-2021-44228 (Log4j)
    "log4j-core": ["2.0", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12", "2.13", "2.14.0", "2.14.1"],
    
    # CVE-2022-23812 (node-ipc)
    "node-ipc": ["9.2.2", "10.1.1", "10.1.2", "10.1.3"],
    
    # CVE-2021-3807 (ansi-regex)
    "ansi-regex": ["3.0.0", "4.0.0", "5.0.0"],
}
```

### Threat Intelligence Integration
```python
# issues/threat_intel.py
# Based on threat intelligence feeds
IOC_PACKAGES = {
    # Packages identified by security researchers
    "malicious-npm-package": None,
    "backdoored-python-lib": ["1.0.0", "1.0.1"],
    
    # Supply chain attack indicators
    "compromised-utility": ["2.1.0"],
}
```

This comprehensive examples file demonstrates the flexibility and power of the GitHub IOC Scanner across various use cases, from simple security audits to complex CI/CD integrations and threat intelligence workflows.