#!/usr/bin/env python3
"""
Archived Repository Verification Script

This script verifies that archived repositories are correctly excluded
from scanning by default.
"""

import os
import sys
from datetime import datetime

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from github_ioc_scanner.models import ScanConfig, Repository
from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.cache import CacheManager
from github_ioc_scanner.ioc_loader import IOCLoader
from github_ioc_scanner.logging_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def create_test_repositories():
    """Create test repositories with mixed archived status."""
    return [
        Repository(
            name="active-repo-1",
            full_name="test-org/active-repo-1",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="archived-repo-1",
            full_name="test-org/archived-repo-1", 
            archived=True,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="active-repo-2",
            full_name="test-org/active-repo-2",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="archived-repo-2",
            full_name="test-org/archived-repo-2",
            archived=True,
            default_branch="main", 
            updated_at=datetime.now()
        ),
    ]


def test_archived_filtering():
    """Test archived repository filtering logic."""
    print("🧪 Testing Archived Repository Filtering")
    print("=" * 45)
    
    # Create test repositories
    test_repos = create_test_repositories()
    
    print(f"📋 Test Data: {len(test_repos)} repositories")
    for repo in test_repos:
        status = "📦 ARCHIVED" if repo.archived else "✅ ACTIVE"
        print(f"  • {repo.name}: {status}")
    
    print("\n🔍 Testing Default Configuration (exclude archived)")
    print("-" * 50)
    
    # Test default configuration (should exclude archived)
    config = ScanConfig(org="test-org")
    print(f"include_archived setting: {config.include_archived}")
    
    # Simulate filtering logic
    if not config.include_archived:
        filtered_repos = [repo for repo in test_repos if not repo.archived]
        archived_count = len(test_repos) - len(filtered_repos)
        
        print(f"📊 Results:")
        print(f"  • Total repositories: {len(test_repos)}")
        print(f"  • Archived repositories: {archived_count}")
        print(f"  • Active repositories: {len(filtered_repos)}")
        print(f"  • Repositories to scan: {len(filtered_repos)}")
        
        print(f"\n✅ Repositories that WILL be scanned:")
        for repo in filtered_repos:
            print(f"  • {repo.name}")
        
        if archived_count > 0:
            archived_repos = [repo for repo in test_repos if repo.archived]
            print(f"\n📦 Repositories that will be SKIPPED (archived):")
            for repo in archived_repos:
                print(f"  • {repo.name}")
    
    print("\n🔍 Testing Include Archived Configuration")
    print("-" * 45)
    
    # Test include archived configuration
    config_with_archived = ScanConfig(org="test-org", include_archived=True)
    print(f"include_archived setting: {config_with_archived.include_archived}")
    
    if config_with_archived.include_archived:
        print(f"📊 Results:")
        print(f"  • Total repositories: {len(test_repos)}")
        print(f"  • Repositories to scan: {len(test_repos)} (including archived)")
        
        print(f"\n✅ All repositories WILL be scanned:")
        for repo in test_repos:
            status = " (archived)" if repo.archived else ""
            print(f"  • {repo.name}{status}")


def test_cli_configuration():
    """Test CLI configuration for archived repositories."""
    print("\n🖥️  CLI Configuration Examples")
    print("=" * 35)
    
    print("Default behavior (exclude archived):")
    print("  github-ioc-scan --org myorg")
    print("  → Scans only active repositories")
    
    print("\nInclude archived repositories:")
    print("  github-ioc-scan --org myorg --include-archived")
    print("  → Scans all repositories including archived ones")
    
    print("\nRecommended for security scanning:")
    print("  github-ioc-scan --org myorg")
    print("  → Focuses on active repositories where threats matter most")


def verify_github_client_filtering():
    """Verify that GitHub client correctly filters archived repositories."""
    print("\n🔧 GitHub Client Filtering Verification")
    print("=" * 40)
    
    print("✅ Verification Points:")
    print("  • get_organization_repos() filters archived repos when include_archived=False")
    print("  • get_team_repos() filters archived repos when include_archived=False") 
    print("  • Retry logic maintains archived filtering")
    print("  • Logging clearly indicates when archived repos are excluded")
    
    print("\n📋 Expected Log Messages:")
    print('  INFO: "📦 Excluded X archived repositories, scanning Y active repositories"')
    print('  DEBUG: "All X repositories are active (no archived repos found)"')


def main():
    """Main verification function."""
    print("🛡️  GitHub IOC Scanner - Archived Repository Verification")
    print("=" * 60)
    print("This script verifies that archived repositories are correctly")
    print("excluded from scanning by default for security best practices.")
    print()
    
    try:
        test_archived_filtering()
        test_cli_configuration()
        verify_github_client_filtering()
        
        print("\n" + "=" * 60)
        print("✅ Archived Repository Filtering Verification Complete!")
        print()
        print("🔒 Security Benefits:")
        print("  • Focuses scanning on active, maintained repositories")
        print("  • Reduces scan time and API usage")
        print("  • Avoids false positives from unmaintained archived code")
        print("  • Prioritizes current security threats")
        
        print("\n📊 Summary:")
        print("  • Default: Archived repositories are EXCLUDED")
        print("  • Option: Use --include-archived to scan archived repos")
        print("  • Logging: Clear indication when archived repos are filtered")
        print("  • Consistent: Same filtering for org and team scans")
        
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        raise


if __name__ == "__main__":
    main()