# Supported Package Managers

This document provides detailed information about all package managers and file formats supported by the GitHub IOC Scanner.

## JavaScript/Node.js Ecosystem

### package.json
**Description**: npm package manifest file  
**Parser**: `JavaScriptParser`  
**Dependencies Checked**: `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies`

**Example**:
```json
{
  "name": "my-app",
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "~4.17.21"
  },
  "devDependencies": {
    "jest": ">=28.0.0"
  }
}
```

**Version Handling**: 
- Semver ranges (`^`, `~`, `>=`, etc.) are normalized to potential exact matches
- The scanner checks if any version in the range could match IOC definitions

### package-lock.json (npm)
**Description**: npm lockfile with exact dependency versions  
**Parser**: `JavaScriptParser`  
**Format**: npm lockfile v1, v2, and v3

**Example**:
```json
{
  "name": "my-app",
  "lockfileVersion": 2,
  "packages": {
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
    }
  }
}
```

**Parsing Logic**: Extracts exact versions from the `packages` section

### yarn.lock (Yarn v1 and v2+)
**Description**: Yarn lockfile format  
**Parser**: `JavaScriptParser`  
**Formats**: Both Yarn Classic (v1) and Yarn Berry (v2+) formats

**Yarn v1 Example**:
```
express@^4.18.0:
  version "4.18.2"
  resolved "https://registry.yarnpkg.com/express/-/express-4.18.2.tgz"
```

**Yarn v2+ Example**:
```
"express@npm:^4.18.0":
  version: 4.18.2
  resolution: "express@npm:4.18.2"
```

**Parsing Logic**: Uses regex patterns to extract package names and versions from both formats

### pnpm-lock.yaml (pnpm)
**Description**: pnpm lockfile format  
**Parser**: `JavaScriptParser`  
**Format**: YAML-based lockfile

**Example**:
```yaml
lockfileVersion: 5.4
specifiers:
  express: ^4.18.0
packages:
  /express/4.18.2:
    resolution: {integrity: sha512-...}
```

**Parsing Logic**: Parses YAML and extracts versions from package paths in the `packages` section

### bun.lockb (Bun)
**Description**: Bun binary lockfile format  
**Parser**: `JavaScriptParser`  
**Format**: Binary format (limited parsing)

**Parsing Logic**: 
- Attempts to extract readable package information from binary data
- May have limited accuracy due to binary format complexity
- Fallback to package.json if lockfile parsing fails

## Python Ecosystem

### requirements.txt
**Description**: pip requirements file  
**Parser**: `PythonParser`  
**Format**: Plain text with package specifications

**Example**:
```
Django==4.1.0
requests>=2.28.0
numpy~=1.23.0
pytest  # Latest version
```

**Version Handling**:
- Exact versions (`==`) are matched directly
- Version ranges (`>=`, `~=`, etc.) are checked for potential matches
- Packages without version specifiers match any IOC version

### Pipfile.lock (Pipenv)
**Description**: Pipenv lockfile with exact versions  
**Parser**: `PythonParser`  
**Format**: JSON-based lockfile

**Example**:
```json
{
    "_meta": {
        "pipfile-spec": 6
    },
    "default": {
        "django": {
            "hashes": ["sha256:..."],
            "version": "==4.1.0"
        }
    },
    "develop": {
        "pytest": {
            "version": "==7.1.2"
        }
    }
}
```

**Parsing Logic**: Extracts exact versions from both `default` and `develop` sections

### poetry.lock (Poetry)
**Description**: Poetry lockfile format  
**Parser**: `PythonParser`  
**Format**: TOML-based lockfile

**Example**:
```toml
[[package]]
name = "django"
version = "4.1.0"
description = "A high-level Python Web framework"

[[package]]
name = "requests"
version = "2.28.1"
```

**Parsing Logic**: Parses TOML format and extracts name/version pairs from package sections

### pyproject.toml
**Description**: Modern Python project configuration  
**Parser**: `PythonParser`  
**Formats**: PEP 621 and Poetry dependency specifications

**PEP 621 Example**:
```toml
[project]
dependencies = [
    "django>=4.0",
    "requests~=2.28.0"
]

[project.optional-dependencies]
dev = ["pytest>=7.0"]
```

**Poetry Example**:
```toml
[tool.poetry.dependencies]
python = "^3.8"
django = "^4.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.1.0"
```

**Parsing Logic**: Handles both PEP 621 and Poetry formats, extracting dependencies from appropriate sections

## Ruby Ecosystem

### Gemfile.lock (Bundler)
**Description**: Bundler lockfile with exact gem versions  
**Parser**: `RubyParser`  
**Format**: Custom Bundler format

**Example**:
```
GEM
  remote: https://rubygems.org/
  specs:
    rails (7.0.4)
      actioncable (= 7.0.4)
      actionmailbox (= 7.0.4)
    rack (2.2.4)

PLATFORMS
  ruby

DEPENDENCIES
  rails (~> 7.0.0)
```

**Parsing Logic**: Parses the `specs` section to extract gem names and exact versions

## PHP Ecosystem

### composer.lock (Composer)
**Description**: Composer lockfile with exact package versions  
**Parser**: `PHPParser`  
**Format**: JSON-based lockfile

**Example**:
```json
{
    "packages": [
        {
            "name": "symfony/console",
            "version": "v6.1.4",
            "source": {
                "type": "git",
                "url": "https://github.com/symfony/console.git"
            }
        }
    ],
    "packages-dev": [
        {
            "name": "phpunit/phpunit",
            "version": "9.5.24"
        }
    ]
}
```

**Parsing Logic**: Extracts packages from both `packages` and `packages-dev` sections

## Go Ecosystem

### go.mod
**Description**: Go modules file  
**Parser**: `GoParser`  
**Format**: Go module syntax

**Example**:
```go
module github.com/myorg/myapp

go 1.19

require (
    github.com/gin-gonic/gin v1.8.1
    github.com/gorilla/mux v1.8.0
)

replace github.com/old/package => github.com/new/package v1.0.0
```

**Parsing Logic**: Parses `require` directives to extract module names and versions

### go.sum
**Description**: Go checksums file  
**Parser**: `GoParser`  
**Format**: Module checksums with versions

**Example**:
```
github.com/gin-gonic/gin v1.8.1 h1:4+fr/el88TOO3ewCmQr8cx/CtZ/umlIRIs5M4NTNjf8=
github.com/gin-gonic/gin v1.8.1/go.mod h1:ji8BvRH1azfM+SYow9zQ6SZMvR8qOMdHmWbZOot6+dE=
```

**Parsing Logic**: Extracts module names and versions from checksum entries

## Rust Ecosystem

### Cargo.lock
**Description**: Cargo lockfile with exact crate versions  
**Parser**: `RustParser`  
**Format**: TOML-based lockfile

**Example**:
```toml
[[package]]
name = "serde"
version = "1.0.144"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "tokio"
version = "1.21.2"
dependencies = [
    "pin-project-lite",
]
```

**Parsing Logic**: Parses TOML format and extracts crate names and versions from package sections

## Parser Architecture

### Base Parser Interface
All parsers implement the `PackageParser` abstract base class:

```python
class PackageParser(ABC):
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file."""
        
    @abstractmethod
    def parse(self, content: str) -> List[PackageDependency]:
        """Parse file content and return list of dependencies."""
```

### Parser Factory
The `PackageParserFactory` automatically selects the appropriate parser based on file patterns:

```python
# File pattern to parser mapping
PARSER_PATTERNS = {
    r"package\.json$": JavaScriptParser,
    r"package-lock\.json$": JavaScriptParser,
    r"yarn\.lock$": JavaScriptParser,
    r"pnpm-lock\.yaml$": JavaScriptParser,
    r"bun\.lockb$": JavaScriptParser,
    r"requirements.*\.txt$": PythonParser,
    r"Pipfile\.lock$": PythonParser,
    r"poetry\.lock$": PythonParser,
    r"pyproject\.toml$": PythonParser,
    r"Gemfile\.lock$": RubyParser,
    r"composer\.lock$": PHPParser,
    r"go\.mod$": GoParser,
    r"go\.sum$": GoParser,
    r"Cargo\.lock$": RustParser,
}
```

### Adding New Parsers

To add support for a new package manager:

1. **Create Parser Class**:
   ```python
   class NewLanguageParser(PackageParser):
       def can_parse(self, file_path: str) -> bool:
           return file_path.endswith('.newformat')
           
       def parse(self, content: str) -> List[PackageDependency]:
           # Implementation here
           pass
   ```

2. **Register Parser**: Add pattern to factory registration

3. **Add Tests**: Create comprehensive test cases

4. **Update Documentation**: Add to this file and README

## Version Matching Logic

### Exact Version Matching
When IOC definitions specify exact versions:
```python
IOC_PACKAGES = {
    "package-name": ["1.0.0", "1.0.1"]
}
```
The scanner matches only these specific versions.

### Wildcard Matching
When IOC definitions use `None`:
```python
IOC_PACKAGES = {
    "package-name": None
}
```
The scanner matches any version of the package.

### Range Handling
For manifest files with version ranges:
- The scanner checks if any version in the range could match IOC definitions
- Lockfiles with exact versions are preferred for accuracy
- Range matching may produce false positives but avoids false negatives

## Performance Considerations

### Parser Efficiency
- **Lockfiles**: Preferred for accuracy and performance (exact versions)
- **Manifest Files**: Require version range analysis (slower)
- **Binary Formats**: Limited parsing capability (bun.lockb)

### Caching Strategy
- Parsed package lists are cached by file SHA
- Cache invalidation occurs when files change
- Parser selection is cached to avoid repeated pattern matching

### Error Handling
- Malformed files are logged as warnings
- Parsing continues with other files if one fails
- Unknown file formats are skipped with informational messages

## Limitations

### Binary Formats
- **bun.lockb**: Limited parsing due to binary format
- May miss some dependencies or have parsing errors

### Version Ranges
- **Manifest Files**: May produce false positives with complex ranges
- **Lockfiles**: Always preferred when available

### Language-Specific Issues
- **Go**: Module replacement directives may affect accuracy
- **Python**: Complex version specifiers may not be fully supported
- **JavaScript**: Workspace configurations may complicate parsing

### Future Enhancements
- Support for additional package managers (Conda, Conan, etc.)
- Better binary format parsing
- Enhanced version range analysis
- Workspace and monorepo support