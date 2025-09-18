#!/usr/bin/env python3
"""
Example demonstrating batch processing with progress monitoring.

This example shows how the GitHub IOC Scanner uses batch processing
with real-time progress updates while maintaining parallel processing
performance.
"""

import asyncio
import os
import tempfile
from datetime import datetime
from typing import List

from src.github_ioc_scanner.cli import CLIInterface
from src.github_ioc_scanner.models import ScanConfig, Repository
from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.github_client import GitHubClient
from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.batch_models import BatchConfig, BatchStrategy


def create_example_ioc_files(issues_dir: str):
    """Create example IOC files for demonstration."""
    
    # S1ngularity attack IOCs
    s1ngularity_content = '''
"""S1ngularity NX attack IOC definitions."""

IOC_PACKAGES = {
    # Compromised packages from the S1ngularity NX attack
    "s1ngularity-nx": None,  # Any version is compromised
    "malicious-dep": ["1.0.0", "1.0.1", "1.0.2"],
    "backdoor-package": None,
    "evil-dependency": ["2.1.0", "2.1.1"]
}
'''
    
    # Supply chain attack IOCs
    supply_chain_content = '''
"""Supply chain attack IOC definitions."""

IOC_PACKAGES = {
    # Common supply chain attack packages
    "fake-lodash": None,
    "malicious-request": ["1.0.0"],
    "compromised-util": None,
    "backdoor-crypto": ["3.0.0", "3.0.1"]
}
'''
    
    with open(os.path.join(issues_dir, "s1ngularity_attack.py"), "w") as f:
        f.write(s1ngularity_content)
    
    with open(os.path.join(issues_dir, "supply_chain_attack.py"), "w") as f:
        f.write(supply_chain_content)


def create_test_repositories() -> List[Repository]:
    """Create a realistic set of test repositories."""
    return [
        Repository(
            name="frontend-app",
            full_name="myorg/frontend-app",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="backend-api",
            full_name="myorg/backend-api",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="shared-components",
            full_name="myorg/shared-components",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="data-pipeline",
            full_name="myorg/data-pipeline",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="mobile-app",
            full_name="myorg/mobile-app",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ),
        Repository(
            name="infrastructure",
            full_name="myorg/infrastructure",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
    ]


async def demonstrate_batch_progress():
    """Demonstrate batch processing with progress monitoring."""
    print("🚀 GitHub IOC Scanner - Batch Processing with Progress Monitoring")
    print("=" * 70)
    
    # Create temporary directory for IOCs
    with tempfile.TemporaryDirectory() as temp_dir:
        issues_dir = os.path.join(temp_dir, "issues")
        os.makedirs(issues_dir)
        create_example_ioc_files(issues_dir)
        
        print(f"📁 Created IOC definitions in: {issues_dir}")
        print(f"   - s1ngularity_attack.py")
        print(f"   - supply_chain_attack.py")
        
        # Create configuration for batch processing
        config = ScanConfig(
            org="myorg",
            fast_mode=False,  # Full scan for demonstration
            verbose=True,
            issues_dir=issues_dir
        )
        
        # Create CLI interface for progress display
        cli = CLIInterface()
        
        # Create progress callback that shows real-time updates
        def progress_callback(current: int, total: int, repo_name: str, start_time: float = None):
            """Enhanced progress callback with batch information."""
            cli.display_progress(current, total, repo_name, config, start_time)
            
            # Add batch-specific information
            if current < total:
                print(f"   🔍 Processing: {repo_name}")
            else:
                print(f"   ✅ Completed batch processing of {total} repositories")
        
        # Configure batch processing for optimal performance
        batch_config = BatchConfig(
            max_concurrent_requests=5,  # Moderate concurrency
            max_concurrent_repos=2,     # Process 2 repos in parallel
            default_batch_size=10,      # Batch size for file requests
            default_strategy=BatchStrategy.ADAPTIVE,  # Adaptive strategy
            enable_cross_repo_batching=True,  # Enable cross-repo optimization
            enable_performance_monitoring=True,  # Monitor performance
            log_batch_metrics=True      # Log detailed metrics
        )
        
        print(f"\n⚙️  Batch Configuration:")
        print(f"   - Strategy: {batch_config.default_strategy.value}")
        print(f"   - Max concurrent requests: {batch_config.max_concurrent_requests}")
        print(f"   - Max concurrent repos: {batch_config.max_concurrent_repos}")
        print(f"   - Batch size: {batch_config.default_batch_size}")
        print(f"   - Cross-repo batching: {batch_config.enable_cross_repo_batching}")
        
        # Create mock GitHub client (for demonstration)
        github_client = GitHubClient(token="demo-token")
        cache_manager = CacheManager()
        
        # Create scanner with batch processing enabled
        scanner = GitHubIOCScanner(
            config=config,
            github_client=github_client,
            cache_manager=cache_manager,
            progress_callback=progress_callback,
            batch_config=batch_config,
            enable_batch_processing=True
        )
        
        print(f"\n🔧 Scanner Configuration:")
        print(f"   - Batch processing: {'✅ Enabled' if scanner.enable_batch_processing else '❌ Disabled'}")
        print(f"   - Progress monitoring: {'✅ Configured' if scanner.progress_callback else '❌ Not configured'}")
        print(f"   - Batch coordinator: {'✅ Ready' if scanner.batch_coordinator else '❌ Not available'}")
        
        # Verify progress monitoring integration
        if (scanner.batch_coordinator and 
            scanner.progress_callback and 
            hasattr(scanner.batch_coordinator.progress_monitor, 'progress_callback')):
            print(f"   - Progress integration: ✅ Active")
        else:
            print(f"   - Progress integration: ❌ Not configured")
        
        print(f"\n📊 Progress Monitoring Features:")
        print(f"   - Real-time progress updates")
        print(f"   - ETA calculation based on processing rate")
        print(f"   - Success/failure rate tracking")
        print(f"   - Batch performance metrics")
        print(f"   - Cross-repository optimization")
        
        # Simulate what would happen during a real scan
        print(f"\n🎯 Batch Processing Workflow:")
        print(f"   1. Repository discovery and optimization")
        print(f"   2. Cross-repo batching analysis")
        print(f"   3. Parallel processing with progress tracking")
        print(f"   4. Real-time ETA updates")
        print(f"   5. Performance metrics collection")
        
        # Show example progress output
        print(f"\n📈 Example Progress Output:")
        print(f"   (This is what you would see during a real scan)")
        
        # Simulate progress updates
        test_repos = create_test_repositories()
        start_time = datetime.now().timestamp()
        
        for i, repo in enumerate(test_repos, 1):
            await asyncio.sleep(0.3)  # Simulate processing time
            progress_callback(i, len(test_repos), repo.full_name, start_time)
        
        print(f"\n✨ Key Benefits of Batch Processing with Progress Monitoring:")
        print(f"   ✅ Maintains parallel processing performance")
        print(f"   ✅ Provides real-time feedback to users")
        print(f"   ✅ Calculates accurate ETAs")
        print(f"   ✅ Tracks success/failure rates")
        print(f"   ✅ Optimizes cross-repository operations")
        print(f"   ✅ Prevents timeout issues with long scans")
        
        print(f"\n🎉 Batch processing with progress monitoring is ready!")
        print(f"   Use --batch-strategy adaptive for optimal performance")
        print(f"   Use --verbose for detailed progress information")


if __name__ == "__main__":
    asyncio.run(demonstrate_batch_progress())