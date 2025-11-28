# Secrets Detection

This document describes the secrets and credential detection capabilities of the GitHub IOC Scanner.

## Overview

The secrets scanner analyzes repository files to detect exposed credentials, API keys, and other sensitive data. This is particularly useful for identifying exfiltrated secrets from supply chain attacks like Shai Hulud 2.

## Supported Secret Types

### AWS Credentials

| Pattern | Description | Example |
|---------|-------------|---------|
| AWS Access Key ID | 20-character key starting with AKIA | `AKIAIOSFODNN7EXAMPLE` |
| AWS Secret Access Key | 40-character base64 string | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |

### GitHub Tokens

| Pattern | Description | Example |
|---------|-------------|---------|
| Personal Access Token | Starts with `ghp_` | `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| OAuth Access Token | Starts with `gho_` | `gho_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| GitHub App Token | Starts with `ghs_` | `ghs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| Refresh Token | Starts with `ghr_` | `ghr_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

### Other Tokens

| Pattern | Description |
|---------|-------------|
| Slack Token | `xoxb-`, `xoxp-`, `xoxa-`, `xoxr-`, `xoxs-` prefixes |
| Generic API Key | `api_key`, `apikey`, `api-key` patterns |
| Private Keys | `-----BEGIN PRIVATE KEY-----`, RSA, EC, OpenSSH |

### Shai Hulud 2 Artifacts

The scanner specifically detects exfiltration artifacts from the Shai Hulud 2 attack:

| File | Description |
|------|-------------|
| `cloud.json` | Exfiltrated AWS/cloud credentials |
| `contents.json` | Stolen repository contents |
| `environment.json` | Captured environment variables |
| `truffleSecrets.json` | Truffle security scan results |

## Secret Masking

All detected secrets are automatically masked in output to prevent accidental exposure:

```
🚨 Secret Detected:
   Type: AWS Access Key
   Value: AKIA************  (masked)
   File: config/settings.py
   Line: 42
```

### Masking Rules

- First 4 characters are shown for identification
- Remaining characters replaced with `***`
- Full secrets are NEVER logged or displayed
- JSON/YAML output also uses masked values

## Usage

### Enable Secrets Scanning

Secrets scanning is enabled by default:

```bash
# Default behavior - secrets are scanned
github-ioc-scan --org your-org
```

### Disable Secrets Scanning

```bash
# Skip secrets analysis
github-ioc-scan --org your-org --no-scan-secrets
```

### Verbose Output

```bash
# See detailed secrets analysis
github-ioc-scan --org your-org --verbose
```

## Example Output

```
🔍 Scanning repository: your-org/backend-api

📁 Secrets Analysis:
├── config/database.py
│   └── 🚨 CRITICAL: AWS Access Key detected
│       └── Value: AKIA************
│       └── Line: 15
│       └── Recommendation: Rotate this credential immediately
├── .env.example
│   └── ⚠️ HIGH: GitHub Token detected
│       └── Value: ghp_************
│       └── Line: 8
│       └── Recommendation: Remove and rotate token
├── cloud.json
│   └── 🚨 CRITICAL: Shai Hulud 2 exfiltration artifact
│       └── Recommendation: Investigate potential compromise

📈 Secrets Summary:
├── Files scanned: 127
├── Secrets found: 3
├── Critical: 2
├── High: 1
```

## File Filtering

### Skipped Files

The scanner automatically skips:

- **Binary files**: Images, compiled code, archives
- **Large files**: Files larger than 10MB
- **Vendor directories**: `node_modules/`, `vendor/`, etc.
- **Build artifacts**: `dist/`, `build/`, `.next/`

### Scanned Files

Priority is given to:

- Configuration files (`.env`, `config.*`, `settings.*`)
- Source code files (`.py`, `.js`, `.ts`, `.java`, etc.)
- CI/CD files (`.github/`, `.gitlab-ci.yml`)
- Documentation with code examples

## False Positive Handling

### Common False Positives

1. **Example/placeholder values** in documentation
2. **Test fixtures** with fake credentials
3. **Base64 encoded non-secrets**
4. **Hash values** that match key patterns

### Reducing False Positives

The scanner uses several techniques:

- **Context analysis**: Checks if value is in comments or documentation
- **Entropy checking**: Low entropy strings are less likely to be secrets
- **Pattern validation**: Validates format matches expected secret structure

### Reporting False Positives

If you encounter false positives:

1. Check if the value is a real secret or placeholder
2. Consider adding to a local allowlist
3. Report patterns that cause frequent false positives via GitHub issues

## Severity Levels

| Severity | Secret Type | Action Required |
|----------|-------------|-----------------|
| **Critical** | AWS keys, private keys, Shai Hulud artifacts | Immediate rotation |
| **High** | GitHub tokens, API keys | Rotate soon |
| **Medium** | Generic secrets, potential credentials | Review and assess |
| **Low** | Possible secrets, low confidence | Verify if sensitive |

## Remediation Steps

### When Secrets Are Found

1. **Don't panic** - but act quickly
2. **Rotate the credential** immediately
3. **Check access logs** for unauthorized use
4. **Remove from repository** (note: history still contains it)
5. **Use git-filter-repo** to remove from history if needed
6. **Enable secret scanning** in GitHub settings

### Preventing Future Exposure

1. **Use environment variables** for secrets
2. **Use secret management** tools (Vault, AWS Secrets Manager)
3. **Enable pre-commit hooks** to catch secrets before commit
4. **Use .gitignore** for sensitive files
5. **Enable GitHub secret scanning** alerts

## Integration with Other Scanners

The secrets scanner complements:

- **Package scanning**: Detects compromised dependencies
- **Workflow scanning**: Identifies dangerous CI/CD configurations
- **Combined analysis**: Correlates findings across scan types

### Shai Hulud 2 Detection

When all scanners are enabled, the tool can detect the full attack chain:

1. **Package scanner**: Detects compromised npm packages
2. **Workflow scanner**: Identifies malicious GitHub Actions
3. **Secrets scanner**: Finds exfiltrated credentials

## Best Practices

### Secret Management Checklist

- [ ] Never commit secrets to version control
- [ ] Use environment variables or secret managers
- [ ] Rotate credentials regularly
- [ ] Enable GitHub secret scanning
- [ ] Use pre-commit hooks (e.g., git-secrets, detect-secrets)
- [ ] Review `.gitignore` for sensitive file patterns
- [ ] Audit repository history for past exposures

### Recommended Tools

- **git-secrets**: Pre-commit hook for AWS credentials
- **detect-secrets**: Yelp's secret detection tool
- **truffleHog**: Git history secret scanner
- **gitleaks**: Fast secret scanner with regex support

## Related Documentation

- [Workflow Scanning](WORKFLOW_SCANNING.md) - GitHub Actions security
- [IOC Definitions](S1NGULARITY_IOC_SUMMARY.md) - Current IOC coverage
- [Troubleshooting](TROUBLESHOOTING.md) - General troubleshooting guide
