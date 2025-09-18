#!/usr/bin/env python3
"""
SBOM Scanning Example

This example demonstrates how to use the GitHub IOC Scanner with SBOM 
(Software Bill of Materials) support to scan repositories for security threats.
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.models import ScanConfig, Repository
from github_ioc_scanner.cache import CacheManager
from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.ioc_loader import IOCLoader
from github_ioc_scanner.logging_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def create_sample_sbom_files():
    """Create sample SBOM files for demonstration."""
    
    # Sample SPDX JSON SBOM
    spdx_sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "MyProject-SBOM",
        "documentNamespace": "https://example.com/sbom/myproject",
        "creationInfo": {
            "created": datetime.now().isoformat() + "Z",
            "creators": ["Tool: github-ioc-scanner-example"]
        },
        "packages": [
            {
                "SPDXID": "SPDXRef-Package-express",
                "name": "express",
                "versionInfo": "4.18.2",
                "downloadLocation": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
                "filesAnalyzed": False,
                "copyrightText": "Copyright (c) 2009-2014 TJ Holowaychuk"
            },
            {
                "SPDXID": "SPDXRef-Package-lodash",
                "name": "lodash", 
                "versionInfo": "4.17.21",
                "downloadLocation": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
                "filesAnalyzed": False,
                "copyrightText": "Copyright OpenJS Foundation and other contributors"
            },
            {
                "SPDXID": "SPDXRef-Package-django",
                "name": "django",
                "versionInfo": "4.2.0",
                "downloadLocation": "https://pypi.org/project/Django/4.2.0/",
                "filesAnalyzed": False,
                "copyrightText": "Copyright (c) Django Software Foundation"
            }
        ]
    }
    
    # Sample CycloneDX JSON SBOM
    cyclonedx_sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "serialNumber": f"urn:uuid:example-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now().isoformat() + "Z",
            "tools": [
                {
                    "vendor": "GitHub IOC Scanner",
                    "name": "SBOM Example Generator",
                    "version": "1.0.0"
                }
            ],
            "component": {
                "type": "application",
                "name": "MyWebApp",
                "version": "1.0.0"
            }
        },
        "components": [
            {
                "type": "library",
                "bom-ref": "pkg:npm/react@18.2.0",
                "name": "react",
                "version": "18.2.0",
                "purl": "pkg:npm/react@18.2.0",
                "licenses": [
                    {
                        "license": {
                            "id": "MIT"
                        }
                    }
                ]
            },
            {
                "type": "library",
                "bom-ref": "pkg:npm/vue@3.3.4",
                "name": "vue",
                "version": "3.3.4",
                "purl": "pkg:npm/vue@3.3.4",
                "licenses": [
                    {
                        "license": {
                            "id": "MIT"
                        }
                    }
                ]
            },
            {
                "type": "library",
                "bom-ref": "pkg:pypi/requests@2.31.0",
                "name": "requests",
                "version": "2.31.0",
                "purl": "pkg:pypi/requests@2.31.0"
            }
        ]
    }
    
    return {
        "spdx_sbom.json": json.dumps(spdx_sbom, indent=2),
        "cyclonedx_bom.json": json.dumps(cyclonedx_sbom, indent=2)
    }


def demonstrate_sbom_scanning_modes():
    """Demonstrate different SBOM scanning modes."""
    
    print("🔍 SBOM Scanning Modes Demonstration")
    print("=" * 50)
    
    # Mode 1: Default (lockfiles + SBOM)
    print("\n1. Default Mode: Scan both lockfiles and SBOM files")
    config_default = ScanConfig(
        org="example-org",
        repo="example-repo",
        enable_sbom=True  # This is the default
    )
    print(f"   Config: enable_sbom={config_default.enable_sbom}")
    
    # Mode 2: SBOM only
    print("\n2. SBOM-Only Mode: Scan only SBOM files")
    config_sbom_only = ScanConfig(
        org="example-org", 
        repo="example-repo",
        sbom_only=True
    )
    print(f"   Config: sbom_only={config_sbom_only.sbom_only}")
    
    # Mode 3: Disable SBOM
    print("\n3. Lockfiles-Only Mode: Disable SBOM scanning")
    config_no_sbom = ScanConfig(
        org="example-org",
        repo="example-repo", 
        disable_sbom=True
    )
    print(f"   Config: disable_sbom={config_no_sbom.disable_sbom}")


def demonstrate_sbom_file_patterns():
    """Demonstrate SBOM file pattern recognition."""
    
    print("\n🎯 SBOM File Pattern Recognition")
    print("=" * 40)
    
    from github_ioc_scanner.parsers.sbom import SBOMParser
    parser = SBOMParser()
    
    test_files = [
        "sbom.json",
        "bom.json", 
        "cyclonedx.json",
        "spdx.json",
        "software-bill-of-materials.json",
        "frontend/sbom.xml",
        "backend/bom.xml",
        "my-project-sbom.json",
        "package.json",  # Should not match
        "requirements.txt",  # Should not match
        "random-file.txt"  # Should not match
    ]
    
    print("File Pattern Matching Results:")
    for file_path in test_files:
        is_sbom = parser.can_parse(file_path)
        status = "✅ SBOM" if is_sbom else "❌ Not SBOM"
        print(f"  {file_path:<35} {status}")


def demonstrate_sbom_parsing():
    """Demonstrate SBOM parsing capabilities."""
    
    print("\n📋 SBOM Parsing Demonstration")
    print("=" * 35)
    
    from github_ioc_scanner.parsers.sbom import SBOMParser
    parser = SBOMParser()
    
    sample_files = create_sample_sbom_files()
    
    for filename, content in sample_files.items():
        print(f"\nParsing {filename}:")
        print("-" * (len(filename) + 9))
        
        packages = parser.parse(content, filename)
        
        print(f"Found {len(packages)} packages:")
        for pkg in packages:
            print(f"  • {pkg.name} v{pkg.version} ({pkg.dependency_type})")


async def demonstrate_batch_sbom_scanning():
    """Demonstrate batch SBOM scanning with async processing."""
    
    print("\n⚡ Batch SBOM Scanning Demonstration")
    print("=" * 40)
    
    # This would require actual GitHub credentials and repositories
    # For demonstration, we'll show the configuration
    
    from github_ioc_scanner.batch_models import BatchConfig
    
    batch_config = BatchConfig(
        default_batch_size=10,
        max_concurrent_requests=5,
        enable_cross_repo_batching=True
    )
    
    config = ScanConfig(
        org="example-org",
        enable_sbom=True,
        batch_size=batch_config.default_batch_size,
        max_concurrent=batch_config.max_concurrent_requests
    )
    
    print("Batch Configuration for SBOM Scanning:")
    print(f"  • Batch Size: {batch_config.default_batch_size}")
    print(f"  • Max Concurrent: {batch_config.max_concurrent_requests}")
    print(f"  • Cross-Repo Batching: {batch_config.enable_cross_repo_batching}")
    print(f"  • SBOM Enabled: {config.enable_sbom}")
    
    print("\nNote: This would scan multiple repositories concurrently,")
    print("      processing both traditional lockfiles and SBOM files")
    print("      with intelligent caching and rate limiting.")


def demonstrate_sbom_caching():
    """Demonstrate SBOM caching strategies."""
    
    print("\n💾 SBOM Caching Demonstration")
    print("=" * 30)
    
    print("SBOM Caching Strategy:")
    print("  1. File Content Caching:")
    print("     • Cache key: file:<org>/<repo>/<path>")
    print("     • Uses ETag for conditional requests")
    print("     • Avoids re-downloading unchanged SBOM files")
    
    print("\n  2. Parsed Package Caching:")
    print("     • Cache key: sbom_packages:<org>/<repo>:<path>")
    print("     • Caches parsed package lists by file SHA")
    print("     • Avoids re-parsing unchanged SBOM content")
    
    print("\n  3. Scan Results Caching:")
    print("     • Cache key: sbom:<org>/<repo>:<path>")
    print("     • Caches IOC match results by file SHA + IOC hash")
    print("     • Avoids re-scanning with same IOC definitions")
    
    print("\n  4. Cross-Repository Optimization:")
    print("     • Shared package metadata across repositories")
    print("     • Intelligent cache warming for common packages")
    print("     • Batch cache operations for performance")


def demonstrate_sbom_ioc_matching():
    """Demonstrate IOC matching with SBOM packages."""
    
    print("\n🚨 SBOM IOC Matching Demonstration")
    print("=" * 35)
    
    # Sample IOC definitions (these would come from the issues directory)
    sample_iocs = {
        "malicious-packages": {
            "express": ["4.17.0", "4.17.1"],  # Vulnerable versions
            "lodash": ["4.17.20"],  # Vulnerable version
            "requests": ["2.25.0", "2.25.1"]  # Vulnerable versions
        },
        "suspicious-patterns": {
            "crypto-mining": ["*"],  # Any version suspicious
            "data-exfiltration": ["*"]
        }
    }
    
    # Sample SBOM packages
    sbom_packages = [
        {"name": "express", "version": "4.18.2", "type": "npm"},
        {"name": "lodash", "version": "4.17.20", "type": "npm"},  # Matches IOC!
        {"name": "requests", "version": "2.31.0", "type": "pypi"},
        {"name": "react", "version": "18.2.0", "type": "npm"}
    ]
    
    print("IOC Matching Results:")
    print("Package Name        Version    Status")
    print("-" * 45)
    
    for pkg in sbom_packages:
        name = pkg["name"]
        version = pkg["version"]
        
        # Check for exact version matches
        threat_found = False
        if name in sample_iocs["malicious-packages"]:
            vulnerable_versions = sample_iocs["malicious-packages"][name]
            if version in vulnerable_versions:
                print(f"{name:<18} {version:<10} 🚨 THREAT DETECTED")
                threat_found = True
        
        # Check for pattern matches
        if name in sample_iocs["suspicious-patterns"]:
            print(f"{name:<18} {version:<10} ⚠️  SUSPICIOUS")
            threat_found = True
        
        if not threat_found:
            print(f"{name:<18} {version:<10} ✅ Clean")


def main():
    """Main demonstration function."""
    
    print("🛡️  GitHub IOC Scanner - SBOM Feature Demonstration")
    print("=" * 60)
    print("This example demonstrates the SBOM (Software Bill of Materials)")
    print("scanning capabilities of the GitHub IOC Scanner.")
    print()
    
    try:
        # Demonstrate different aspects of SBOM scanning
        demonstrate_sbom_scanning_modes()
        demonstrate_sbom_file_patterns()
        demonstrate_sbom_parsing()
        
        # Async demonstration
        print("\nRunning async demonstrations...")
        asyncio.run(demonstrate_batch_sbom_scanning())
        
        demonstrate_sbom_caching()
        demonstrate_sbom_ioc_matching()
        
        print("\n" + "=" * 60)
        print("✅ SBOM Feature Demonstration Complete!")
        print()
        print("Key Benefits of SBOM Scanning:")
        print("  • Comprehensive dependency visibility")
        print("  • Standardized security scanning (SPDX, CycloneDX)")
        print("  • Supply chain risk assessment")
        print("  • Compliance and audit support")
        print("  • Integration with existing lockfile scanning")
        
        print("\nUsage Examples:")
        print("  # Scan with SBOM enabled (default)")
        print("  github-ioc-scan --org myorg")
        print()
        print("  # Scan only SBOM files")
        print("  github-ioc-scan --org myorg --sbom-only")
        print()
        print("  # Disable SBOM scanning")
        print("  github-ioc-scan --org myorg --disable-sbom")
        
    except Exception as e:
        logger.error(f"Demonstration failed: {e}")
        raise


if __name__ == "__main__":
    main()