# Release Notes v1.5.0 - Critical Security Update

## 🚨 Shai Hulud Worm Attack Response

This release addresses the critical Shai Hulud worm attack that infected 500+ npm packages with sophisticated worm payloads capable of self-propagation across the npm ecosystem.

### 🛡️ Security Enhancements

#### IOC Database Expansion
- **500+ New Malicious Packages**: Complete coverage of the Shai Hulud attack surface
- **Worm Payload Detection**: Enhanced detection capabilities for self-propagating malware
- **Cross-Platform Coverage**: 
  - Mobile development packages (Capacitor, Cordova)
  - Web frameworks (Ember, React, Angular)
  - Development tooling and build systems
  - Security tool impersonation packages

#### Key Attack Vectors Covered
- **Supply Chain Worm**: First documented worm in npm supply chain attacks
- **CrowdStrike Impersonation**: Malicious packages mimicking security tools
- **Framework Targeting**: Broad attack on popular JavaScript ecosystems
- **Version-Specific Threats**: Precise version targeting for maximum impact

### 📦 New IOC Packages Added

#### Mobile Development
- `capacitor-notificationhandler` (0.0.2, 0.0.3)
- `capacitor-plugin-healthapp` (0.0.2, 0.0.3)
- `capacitor-plugin-ihealth` (1.1.8, 1.1.9)
- `capacitor-plugin-vonage` (1.0.2, 1.0.3)
- `cordova-plugin-voxeet2` (1.0.24)
- `cordova-voxeet` (1.0.32)

#### Web Frameworks
- `ember-browser-services` (5.0.2, 5.0.3)
- `ember-headless-form` (1.1.2, 1.1.3)
- `ember-headless-table` (2.1.5, 2.1.6)
- `ember-velcro` (2.2.1, 2.2.2)

#### Security Tool Impersonation
- `eslint-config-crowdstrike` (11.0.2, 11.0.3)
- `eslint-config-crowdstrike-node` (4.0.3, 4.0.4)
- `remark-preset-lint-crowdstrike` (4.0.1, 4.0.2)

#### Development Tools
- `@rxap/ngx-bootstrap` (19.0.3, 19.0.4)
- `browser-webdriver-downloader` (3.0.8)
- `create-hest-app` (0.1.9)
- `mcp-knowledge-base` (0.0.2)
- `mcp-knowledge-graph` (1.2.1)

### 🧹 Repository Maintenance

#### Documentation Organization
- Moved all summary documents to `docs/` directory
- Cleaned up root directory structure
- Organized development artifacts

#### Test Code Cleanup
- Removed temporary development test files
- Cleaned up debug artifacts
- Streamlined test suite

### 🔍 Detection Capabilities

#### Worm Behavior Detection
The scanner now detects patterns associated with worm payloads:
- Package installation hooks
- Network communication patterns
- File system modifications beyond normal package behavior
- Self-propagation mechanisms

#### Version-Specific Targeting
Enhanced precision in detecting compromised package versions:
- Exact version matching for known threats
- Range-based detection for version families
- Behavioral analysis for unknown variants

### 📊 Attack Intelligence

#### Threat Landscape
- **Attack Type**: Supply chain attack with worm payload
- **Threat Level**: CRITICAL
- **Affected Ecosystems**: npm, mobile development, web frameworks
- **Geographic Impact**: Global
- **First Seen**: December 2024

#### Indicators of Compromise
- 500+ malicious npm packages
- Worm payload capabilities
- Cross-platform targeting
- Security tool impersonation
- Framework ecosystem infiltration

### 🚀 Upgrade Instructions

1. **Update the scanner**:
   ```bash
   pip install --upgrade github-ioc-scanner
   ```

2. **Verify new IOCs are loaded**:
   ```bash
   github-ioc-scan --list-iocs | grep -i shai
   ```

3. **Run immediate scan on critical repositories**:
   ```bash
   github-ioc-scan --org your-org --priority-scan
   ```

### 🔗 References

- [Securelist Report](https://securelist.com/shai-hulud-worm-infects-500-npm-packages-in-a-supply-chain-attack/117547/)
- [Shai Hulud Expansion Summary](docs/SHAI_HULUD_EXPANSION_SUMMARY.md)
- [IOC Database](issues/shai_hulud.py)

### ⚠️ Immediate Action Required

Organizations using npm packages should:
1. **Scan immediately** for affected packages
2. **Review package.json** files for suspicious dependencies
3. **Update security policies** to include worm detection
4. **Monitor** for unusual network activity from build processes

This release provides critical protection against one of the most sophisticated supply chain attacks to date. Update immediately to ensure your organization is protected.