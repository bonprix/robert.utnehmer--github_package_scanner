# Maven Support

This document describes the Maven/Java dependency scanning capabilities of the GitHub IOC Scanner.

## Overview

The scanner supports Maven-based Java projects by parsing `pom.xml` files to extract dependency information. This enables detection of compromised Java packages in your repositories.

## Supported Files

| File | Description |
|------|-------------|
| `pom.xml` | Maven Project Object Model file |

## Dependency Extraction

The Maven parser extracts dependencies from the following sections:

### Standard Dependencies

```xml
<dependencies>
    <dependency>
        <groupId>org.example</groupId>
        <artifactId>my-library</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

### Dependency Management

Dependencies defined in `<dependencyManagement>` are also extracted:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.example</groupId>
            <artifactId>managed-lib</artifactId>
            <version>2.0.0</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Dependency Scopes

All dependency scopes are supported:
- `compile` (default)
- `provided`
- `runtime`
- `test`
- `system`

## IOC Format

Maven IOCs use the `groupId:artifactId` format for package identification:

```python
MAVEN_IOC_PACKAGES = {
    "org.example:malicious-lib": {"1.0.0", "1.0.1"},
    "com.attacker:backdoor": {"2.5.0"},
}
```

### Matching Behavior

- Package names are matched as `groupId:artifactId`
- Version matching is exact (must match a known compromised version)
- Both `<dependencies>` and `<dependencyManagement>` sections are scanned

## Property Resolution

The parser supports basic Maven property resolution:

### Supported Properties

```xml
<properties>
    <spring.version>5.3.0</spring.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>${spring.version}</version>  <!-- Resolved to 5.3.0 -->
    </dependency>
</dependencies>
```

### Built-in Properties

- `${project.version}` - Resolved from `<version>` in project root
- `${project.groupId}` - Resolved from `<groupId>` in project root
- `${project.artifactId}` - Resolved from `<artifactId>` in project root

## Limitations

### Parent POM Resolution

Parent POM files are **not** automatically resolved. If a dependency version is defined in a parent POM, it will not be detected:

```xml
<!-- This parent POM is NOT fetched -->
<parent>
    <groupId>org.example</groupId>
    <artifactId>parent-pom</artifactId>
    <version>1.0.0</version>
</parent>
```

**Workaround**: Ensure critical dependencies have explicit versions in the scanned `pom.xml`.

### Complex Property Resolution

The following property patterns are **not** supported:
- Properties defined in parent POMs
- Properties from external files
- Nested property references (`${${property.name}}`)
- Profile-specific properties

### Multi-Module Projects

Each `pom.xml` is scanned independently. Module relationships are not resolved.

## Usage Examples

### Basic Scan

```bash
# Scan organization for Maven dependencies
github-ioc-scan --org your-org
```

### Maven-Only Scan

```bash
# Focus on Java repositories
github-ioc-scan --org your-org --repo java-project
```

### Verbose Output

```bash
# See detailed Maven parsing information
github-ioc-scan --org your-org --verbose
```

## Example Output

```
🔍 Scanning repository: your-org/java-service

📁 Files analyzed:
├── pom.xml
│   └── Dependencies found: 15
│   └── 🚨 CRITICAL: org.example:malicious-lib@1.0.0
│       └── IOC Source: shai_hulud_2.py
│       └── Description: Compromised Maven package

📈 Scan Summary:
├── Maven files scanned: 1
├── Dependencies analyzed: 15
├── Threats found: 1
```

## Adding Maven IOCs

To add new Maven IOC definitions:

1. Edit `src/github_ioc_scanner/issues/shai_hulud_2.py` (or create a new issue file)
2. Add entries to `MAVEN_IOC_PACKAGES`:

```python
MAVEN_IOC_PACKAGES = {
    # Format: "groupId:artifactId": {"version1", "version2", ...}
    "com.malicious:evil-package": {"1.0.0", "1.0.1"},
}
```

3. The IOC loader automatically includes Maven packages in scans

## Troubleshooting

### No Dependencies Found

- Verify the `pom.xml` is valid XML
- Check for XML namespace issues (the parser handles standard Maven namespaces)
- Ensure dependencies are in `<dependencies>` or `<dependencyManagement>` sections

### Property Not Resolved

- Check if the property is defined in the same `pom.xml`
- Parent POM properties are not resolved (see Limitations)
- Use explicit versions for critical dependencies

### False Positives

- Verify the `groupId:artifactId` combination matches exactly
- Check version numbers match the IOC definition
- Report false positives via GitHub issues

## Related Documentation

- [Package Manager Support](PACKAGE_MANAGERS.md) - All supported package managers
- [IOC Definitions](S1NGULARITY_IOC_SUMMARY.md) - Current IOC coverage
- [Troubleshooting](TROUBLESHOOTING.md) - General troubleshooting guide
