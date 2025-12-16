#!/usr/bin/env python3
"""
Auto-update script for Shai-Hulud IOC packages from Wiz Research.

This script downloads the latest Shai-Hulud package list from Wiz Research
and updates the local IOC definitions.

Usage:
    python scripts/update_shai_hulud_iocs.py
"""

import csv
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# URL to Wiz Research IOC CSV
WIZ_IOC_URL = "https://raw.githubusercontent.com/wiz-sec-public/wiz-research-iocs/main/reports/shai-hulud-2-packages.csv"

# Path to IOC file
IOC_FILE = Path(__file__).parent.parent / "src" / "github_ioc_scanner" / "issues" / "shai_hulud_2.py"


def download_csv(url: str) -> list:
    """Download and parse CSV from URL.
    
    Args:
        url: URL to CSV file
        
    Returns:
        List of dictionaries with package data
    """
    print(f"Downloading IOC data from {url}...")
    
    try:
        with urlopen(url) as response:
            content = response.read().decode('utf-8')
            
        # Parse CSV
        reader = csv.DictReader(content.splitlines())
        packages = list(reader)
        
        print(f"✓ Downloaded {len(packages)} packages")
        return packages
        
    except Exception as e:
        print(f"✗ Failed to download CSV: {e}", file=sys.stderr)
        sys.exit(1)


def parse_packages(csv_data: list) -> dict:
    """Parse CSV data into IOC format.
    
    Args:
        csv_data: List of dictionaries from CSV
        
    Returns:
        Dictionary mapping package names to versions
    """
    ioc_packages = {}
    
    for row in csv_data:
        # Try both lowercase and capitalized column names
        package_name = (row.get('Package') or row.get('package', '')).strip()
        version = (row.get('Version') or row.get('version', '')).strip()
        
        # Remove version prefix (e.g., "= 0.0.7" -> "0.0.7")
        if version.startswith('= '):
            version = version[2:].strip()
        
        if not package_name:
            continue
            
        # Add to IOC list
        if package_name not in ioc_packages:
            ioc_packages[package_name] = []
        
        if version and version not in ioc_packages[package_name]:
            ioc_packages[package_name].append(version)
    
    print(f"✓ Parsed {len(ioc_packages)} unique packages")
    return ioc_packages


def generate_ioc_file(packages: dict) -> str:
    """Generate Python IOC file content.
    
    Args:
        packages: Dictionary of package names to versions
        
    Returns:
        Python file content as string
    """
    lines = [
        '"""',
        'Shai-Hulud 2.0 Supply Chain Attack IOC Definitions',
        '',
        'This file contains Indicators of Compromise (IOCs) for the Shai-Hulud 2.0',
        'supply chain attack targeting npm packages.',
        '',
        'Source: Wiz Research',
        'URL: https://github.com/wiz-sec-public/wiz-research-iocs',
        f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        '',
        'References:',
        '- https://www.wiz.io/blog/shai-hulud-2-0-ongoing-supply-chain-attack',
        '- https://securitylabs.datadoghq.com/articles/shai-hulud-2.0-npm-worm/',
        '- https://xygeni.io/de/blog/shai-hulud-the-npm-packages-worm-explained/',
        '"""',
        '',
        '# Compromised npm packages from Shai-Hulud 2.0 attack',
        'IOC_PACKAGES = {',
    ]
    
    # Sort packages alphabetically
    for package_name in sorted(packages.keys()):
        versions = packages[package_name]
        
        if versions:
            # Specific versions
            versions_str = ', '.join(f'"{v}"' for v in sorted(versions))
            lines.append(f'    "{package_name}": [{versions_str}],')
        else:
            # All versions compromised
            lines.append(f'    "{package_name}": None,  # All versions')
    
    lines.append('}')
    lines.append('')
    
    return '\n'.join(lines)


def update_ioc_file(content: str) -> None:
    """Write IOC content to file.
    
    Args:
        content: Python file content
    """
    print(f"Writing to {IOC_FILE}...")
    
    try:
        IOC_FILE.parent.mkdir(parents=True, exist_ok=True)
        IOC_FILE.write_text(content)
        print(f"✓ Successfully updated {IOC_FILE}")
        
    except Exception as e:
        print(f"✗ Failed to write file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function."""
    print("=" * 60)
    print("Shai-Hulud IOC Auto-Update")
    print("=" * 60)
    print()
    
    # Download CSV
    csv_data = download_csv(WIZ_IOC_URL)
    
    # Parse packages
    packages = parse_packages(csv_data)
    
    # Generate IOC file
    content = generate_ioc_file(packages)
    
    # Update file
    update_ioc_file(content)
    
    print()
    print("=" * 60)
    print("✓ Update complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the changes: git diff src/github_ioc_scanner/issues/shai_hulud_2.py")
    print("2. Run tests: pytest tests/")
    print("3. Commit changes: git add src/github_ioc_scanner/issues/shai_hulud_2.py")


if __name__ == "__main__":
    main()
