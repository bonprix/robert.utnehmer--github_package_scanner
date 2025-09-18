#!/usr/bin/env python3
"""
Example: Team-First Organization Scanning

This example demonstrates how to use the team-first organization scanning feature
to scan all repositories in an organization, organized by teams.

The team-first approach:
1. Discovers all repositories in the organization
2. Discovers all teams in the organization  
3. Iterates through teams, scanning their repositories
4. Displays results grouped by team
5. Scans any remaining repositories not assigned to teams

This provides better organization and visibility into which teams
have security issues that need attention.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.models import ScanConfig


def main():
    """Run team-first organization scanning example."""
    
    # Check for required environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable is required")
        print("Please set your GitHub personal access token:")
        print("export GITHUB_TOKEN=your_token_here")
        return 1
    
    # Get organization from command line or use default
    org_name = sys.argv[1] if len(sys.argv) > 1 else "octocat"
    
    print(f"🔍 Team-First Organization Scanning Example")
    print(f"Organization: {org_name}")
    print("=" * 60)
    
    # Create a sample IOC file for demonstration
    sample_iocs = {
        "packages": [
            {
                "name": "malicious-package",
                "versions": ["1.0.0", "1.0.1", "2.0.0"],
                "description": "Example malicious package"
            },
            {
                "name": "compromised-lib", 
                "versions": ["0.1.0"],
                "description": "Example compromised library"
            }
        ]
    }
    
    # Write IOCs to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        import json
        json.dump(sample_iocs, f, indent=2)
        ioc_file = f.name
    
    try:
        # Configure scanner for team-first organization scan
        config = ScanConfig(
            org=org_name,
            team_first_org=True,  # Enable team-first scanning
            ioc_files=[ioc_file],
            quiet=False,  # Show progress
            fast_mode=True,  # Use fast mode for demo
            include_archived=False  # Skip archived repos
        )
        
        # Create and run scanner
        print("🚀 Starting team-first organization scan...")
        print()
        
        scanner = GitHubIOCScanner(config)
        results = scanner.scan()
        
        # Display final summary
        print()
        print("📊 SCAN SUMMARY")
        print("=" * 60)
        print(f"Organization: {org_name}")
        print(f"Repositories scanned: {results.repositories_scanned}")
        print(f"Files analyzed: {results.files_scanned}")
        print(f"Total IOC matches: {len(results.matches)}")
        print(f"Scan duration: {results.scan_duration:.2f} seconds")
        
        if results.matches:
            print()
            print("🚨 SECURITY ALERTS")
            print("=" * 60)
            
            # Group matches by repository for better display
            repo_matches = {}
            for match in results.matches:
                if match.repository not in repo_matches:
                    repo_matches[match.repository] = []
                repo_matches[match.repository].append(match)
            
            for repo_name, matches in repo_matches.items():
                print(f"📦 {repo_name}")
                for match in matches:
                    print(f"   ⚠️  {match.file_path}")
                    print(f"      Package: {match.package_name} {match.version}")
                print()
        else:
            print()
            print("✅ No IOC matches found - organization appears clean!")
        
        # Display cache statistics if available
        if results.cache_stats:
            print()
            print("💾 CACHE PERFORMANCE")
            print("=" * 60)
            print(f"Cache hits: {results.cache_stats.hits}")
            print(f"Cache misses: {results.cache_stats.misses}")
            if results.cache_stats.hits + results.cache_stats.misses > 0:
                hit_rate = results.cache_stats.hits / (results.cache_stats.hits + results.cache_stats.misses) * 100
                print(f"Hit rate: {hit_rate:.1f}%")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Scan interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Scan failed: {e}")
        return 1
    finally:
        # Clean up temporary IOC file
        os.unlink(ioc_file)


if __name__ == "__main__":
    print(__doc__)
    exit_code = main()
    sys.exit(exit_code)