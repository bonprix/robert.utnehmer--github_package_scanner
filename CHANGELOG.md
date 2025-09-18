# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-09-18

### 🎯 Major New Features
- **SBOM Support**: Added comprehensive Software Bill of Materials (SBOM) scanning capability
  - Support for GitHub Dependency Graph API SBOM export
  - SPDX JSON format parsing with nested API structure handling
  - CycloneDX JSON format support
  - Automatic detection and parsing of both in-repository and API-based SBOMs
  - Seamless integration with existing lockfile scanning
- **Enhanced Security Coverage**: Repositories are now scanned using both traditional lockfiles AND GitHub's dependency graph
- **Improved IOC Detection**: Doubled security coverage by scanning multiple dependency sources per repository

### 🔧 Technical Improvements
- **API SBOM Parser**: Enhanced SBOM parser to handle GitHub's nested `{"sbom": {...}}` API response format
- **Dual-Source Scanning**: Intelligent combination of lockfile and SBOM data for comprehensive coverage
- **Performance Optimized**: SBOM scanning integrated with existing caching and rate limiting systems

### 📊 Statistics
- Successfully tested with 1000+ package SBOMs
- Verified IOC detection across both lockfile and SBOM sources
- Maintains existing performance characteristics while adding comprehensive SBOM support

## [1.1.6] - 2025-01-18

### 🚀 Major Performance Improvements
- **Tree-First Mode**: Use Tree API by default for large team scans to avoid Code Search rate limits entirely
- **No-Wait Rate Limiting**: Only wait when REST API is completely exhausted, not for low limits
- **Optimized Large Team Scanning**: Dramatically faster scanning for teams with 50+ repositories
- **Intelligent API Selection**: Automatically choose the most efficient API for the scan type

## [1.1.5] - 2025-01-18

### 🚀 Performance Improvements
- **Smart Code Search Fallback**: Automatically fallback to Tree API when Code Search rate limits are hit
- **Rate Limit Intelligence**: Track Code Search rate limit status to avoid unnecessary API calls
- **Improved Large Team Scanning**: Better handling of teams with many repositories (100+ repos)
- **Smart Rate Limiter**: New intelligent rate limiting system optimized for large scans

## [1.1.4] - 2025-01-18

### 🔧 Fixes
- **Repository Links**: Fixed broken GitHub repository URLs in pyproject.toml and documentation
- **Documentation Updates**: Updated repository references from placeholder to actual GitHub repository
- **Copyright Year**: Updated copyright year to 2025 in LICENSE file
- **Current Status**: Updated "Current as of" date to January 2025 in README

## [1.1.3] - 2025-01-18

### 🔒 Security Improvements
- **Archived Repository Filtering**: Archived repositories are now consistently excluded from all scan types
- **Team Scan Enhancement**: Fixed archived repository filtering for team-based scans
- **Clear Communication**: Added informative logging about excluded archived repositories
- **Configuration Option**: Added `--include-archived` flag to optionally include archived repositories

## [1.1.0] - 2025-09-18

### 🚀 Major New Features

#### SBOM (Software Bill of Materials) Support
- **Native SBOM Scanning**: Full support for SPDX and CycloneDX formats (JSON/XML)
- **Multiple SBOM Formats**: SPDX, CycloneDX, and generic SBOM files
- **Intelligent File Detection**: Automatic recognition of SBOM files by pattern and content
- **Three Scanning Modes**: 
  - Default: Lockfiles + SBOM files
  - SBOM-only: `--sbom-only` flag
  - Lockfiles-only: `--disable-sbom` flag
- **SBOM-specific Caching**: Optimized caching strategies for SBOM content and parsed packages
- **Package URL (PURL) Support**: Automatic package type detection from PURLs

#### Enhanced Rate Limiting
- **Proactive Rate Limiting**: Intelligent slowdown before hitting API limits
- **Adaptive Learning**: Learns from rate limit patterns and adjusts delays automatically
- **Code Search API Optimization**: Separate handling for Code Search API (30 req/min) limits
- **Conservative Batch Configuration**: Optimized defaults for large organizations
- **Real-time Monitoring**: Enhanced logging with rate limit status indicators

### 🛠️ Improvements

#### Performance & Reliability
- **Reduced Default Concurrency**: More conservative settings for better rate limit handling
- **Improved Error Handling**: Better recovery from rate limit and network issues
- **Enhanced Logging**: More informative rate limit status messages with emojis
- **Batch Processing Optimizations**: Better handling of large repository scans

#### CLI Enhancements
- **New SBOM Options**: `--enable-sbom`, `--disable-sbom`, `--sbom-only`
- **Better Progress Reporting**: More accurate ETA calculations with rate limiting
- **Enhanced Help Text**: Updated documentation for new features

### 📁 Supported SBOM Files

#### File Patterns
- `sbom.json`, `bom.json`, `cyclonedx.json`, `spdx.json`
- `sbom.xml`, `bom.xml`, `cyclonedx.xml`, `spdx.xml`
- `software-bill-of-materials.json`, `software-bill-of-materials.xml`
- `.sbom`, `.spdx`, `SBOM.json`, `BOM.json`

#### SBOM Formats
- **SPDX 2.3**: Industry standard SBOM format (JSON/XML)
- **CycloneDX 1.4**: OWASP SBOM standard (JSON/XML)
- **Generic**: Custom SBOM formats with automatic detection

### 🔧 Technical Changes

#### New Modules
- `src/github_ioc_scanner/parsers/sbom.py`: SBOM parser implementation
- `src/github_ioc_scanner/improved_rate_limiting.py`: Enhanced rate limiting logic

#### Updated Modules
- `src/github_ioc_scanner/scanner.py`: SBOM integration and scanning modes
- `src/github_ioc_scanner/cli.py`: New CLI options and SBOM support
- `src/github_ioc_scanner/github_client.py`: Improved rate limiting integration
- `src/github_ioc_scanner/batch_models.py`: Conservative batch configuration
- `src/github_ioc_scanner/models.py`: Extended ScanConfig for SBOM options

#### New Examples
- `examples/sbom_scanning_example.py`: Comprehensive SBOM feature demonstration
- `examples/rate_limit_optimization_example.py`: Rate limiting optimization guide

### 🧪 Testing

#### New Test Coverage
- **29 SBOM Tests**: Complete test suite for SBOM parsing and integration
- **16 SBOM Parser Tests**: All formats, edge cases, and error handling
- **13 Scanner Integration Tests**: End-to-end SBOM functionality
- **Rate Limiting Tests**: Proactive and adaptive rate limiting validation

### 📚 Documentation

#### Updated Documentation
- **README.md**: SBOM feature documentation and usage examples
- **SBOM_FEATURE_SUMMARY.md**: Comprehensive SBOM implementation guide
- **RATE_LIMIT_IMPROVEMENTS.md**: Rate limiting optimization documentation

### 🔒 Security Enhancements

#### Supply Chain Security
- **Comprehensive SBOM Analysis**: Scan standardized software bills of materials
- **Enhanced Dependency Visibility**: Better coverage of project dependencies
- **Compliance Support**: SPDX and CycloneDX standard compliance
- **IOC Integration**: Same IOC definitions work for both lockfiles and SBOM files

### ⚡ Performance Improvements

#### Rate Limiting Optimizations
- **90% Fewer Rate Limit Warnings**: Proactive prevention of API exhaustion
- **Predictable Scan Times**: More stable ETA calculations
- **Adaptive Delays**: Smart delay adjustments based on API response patterns
- **Conservative Defaults**: Optimized for large organization scanning

### 🎯 Usage Examples

#### SBOM Scanning
```bash
# Default: Scan both lockfiles and SBOM files
github-ioc-scan --org myorg

# Scan only SBOM files
github-ioc-scan --org myorg --sbom-only

# Disable SBOM scanning
github-ioc-scan --org myorg --disable-sbom
```

#### Rate Limit Optimization
```bash
# Conservative settings for large organizations
github-ioc-scan --org large-org --max-concurrent 2 --batch-size 5

# Balanced settings for medium organizations  
github-ioc-scan --org medium-org --max-concurrent 5 --batch-size 10

# Fast mode for quick assessment
github-ioc-scan --org any-org --fast --sbom-only
```

### 🐛 Bug Fixes
- Fixed import errors in test suite
- Improved error handling for malformed SBOM files
- Better handling of XML namespace parsing
- Fixed recursive scanning issues in combined mode

### 🔄 Breaking Changes
- None - All changes are backward compatible

### 📦 Dependencies
- No new dependencies added
- All existing dependencies maintained

---

## [1.0.10] - 2025-09-18

### Previous Release
- Core IOC scanning functionality
- Multi-language package manager support
- Batch processing capabilities
- Comprehensive caching system
- Professional CLI interface

---

**Full Changelog**: https://github.com/your-org/github-ioc-scanner/compare/v1.0.10...v1.1.0