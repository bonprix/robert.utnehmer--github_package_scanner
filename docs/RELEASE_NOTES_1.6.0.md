# Release Notes - Version 1.6.0

**Release Date:** November 27, 2025

## Overview

Version 1.6.0 is a major release that introduces three significant new security scanning capabilities: Maven/Java support, GitHub Actions workflow security scanning, and secrets detection. This release also includes comprehensive code cleanup and documentation improvements.

## 🚀 Major New Features

### Maven/Java Support

The scanner now fully supports Java projects using Maven:

- **pom.xml Parsing**: Extracts dependencies from Maven project files
- **Dependency Extraction**: Captures groupId, artifactId, and version information
- **Property Resolution**: Handles Maven property references like `${project.version}`
- **Dependency Management**: Scans both `<dependencies>` and `<dependencyManagement>` sections
- **Maven IOCs**: New threat database for Java-specific malicious packages

**Usage:**
```bash
# Maven scanning is enabled by default
github-ioc-scan --org your-org

# Disable Maven scanning
github-ioc-scan --org your-org --disable-maven
```

### GitHub Actions Workflow Security Scanning

New capability to detect dangerous configurations in GitHub Actions workflows:

- **Dangerous Triggers**: Detects `pull_request_target` with unsafe checkout patterns
- **Privilege Escalation**: Identifies `workflow_run` triggers that could enable attacks
- **Malicious Runners**: Detects known malicious self-hosted runners (e.g., SHA1HULUD)
- **Shai Hulud 2 Patterns**: Identifies attack-specific workflow files
- **Severity Classification**: Findings categorized as critical, high, medium, or low

**Usage:**
```bash
# Enable workflow scanning
github-ioc-scan --org your-org --scan-workflows

# Disable workflow scanning
github-ioc-scan --org your-org --no-scan-workflows
```

### Secrets Detection

New capability to detect exfiltrated credentials and secrets:

- **AWS Credentials**: Access keys (AKIA...) and secret keys
- **GitHub Tokens**: PATs (ghp_), OAuth (gho_), App tokens (ghs_)
- **API Keys**: Generic API key pattern detection
- **Private Keys**: RSA, EC, and OpenSSH private keys
- **Slack Tokens**: Bot and user tokens
- **Shai Hulud 2 Artifacts**: Exfiltration files (cloud.json, environment.json, etc.)
- **Automatic Masking**: All detected secrets are masked in output

**Usage:**
```bash
# Enable secrets scanning
github-ioc-scan --org your-org --scan-secrets

# Disable secrets scanning
github-ioc-scan --org your-org --no-scan-secrets
```

## 🧹 Code Cleanup

This release includes significant code cleanup:

- New `CodeAnalyzer` utility for project analysis
- Removal of unused modules and outdated documentation
- Updated imports and fixed broken references
- All tests verified to pass after cleanup

## 📚 New Documentation

- **[Maven Support](MAVEN_SUPPORT.md)**: Complete guide to Maven/Java scanning
- **[Workflow Scanning](WORKFLOW_SCANNING.md)**: GitHub Actions security guide
- **[Secrets Detection](SECRETS_DETECTION.md)**: Credential detection documentation
- **[Project Cleanup Report](PROJECT_CLEANUP_REPORT.md)**: Analysis findings

## 🔧 Technical Details

### New Modules
- `parsers/maven.py`: Maven POM parser
- `workflow_scanner.py`: GitHub Actions analyzer
- `secrets_scanner.py`: Secrets detector
- `code_analyzer.py`: Project analysis utility

### New Data Models
- `WorkflowFinding`: Workflow security findings
- `SecretFinding`: Detected secrets with masking
- `MavenDependency`: Maven dependency information

### Test Coverage
- 82 new tests for Maven, workflow, and secrets scanning
- Test coverage: Maven (100%), Secrets (96%), Workflow (91%)
- New test fixtures in `tests/fixtures/`

## 📊 Updated Metrics

- **Total IOC Database**: 2,932+ packages
- **Supported Languages**: 7 (added Java/Maven)
- **Security Scan Types**: 4 (packages, workflows, secrets, SBOM)

## Upgrade Instructions

```bash
# Upgrade via pip
pip install --upgrade github-ioc-scanner

# Or install from source
git clone https://github.com/christianherweg0807/github_package_scanner.git
cd github_package_scanner
pip install -e .
```

## Breaking Changes

None. All existing functionality remains backward compatible.

## Known Issues

- Maven parent POM resolution is not supported (documented limitation)
- Complex Maven property expressions may not resolve correctly

## Contributors

Thanks to all contributors who made this release possible!

## Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for the complete list of changes.
