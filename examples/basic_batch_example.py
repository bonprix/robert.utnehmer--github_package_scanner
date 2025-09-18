#!/usr/bin/env python3
"""
Basic Batch Processing Example

This example demonstrates the basic usage of the GitHub IOC Scanner's
batch processing capabilities for improved performance.
"""

import asyncio
import os
from typing import List

from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from github_ioc_scanner.async_github_client import AsyncGitHubClient
from github_ioc_scanner.cache_manager import CacheManager
from github_ioc_scanner.models import Repository


async def basic_batch_scan():
    """Demonstrate basic batch scanning of repositories."""
    
    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    
    # Initialize components
    github_client = AsyncGitHubClient(token=github_token)
    cache_manager = CacheManager()
    
    # Configure batch processing with basic settings
    config = BatchConfig(
        max_concurrent_requests=10,
        default_batch_size=8,
        default_strategy=BatchStrategy.ADAPTIVE,
        enable_performance_monitoring=True
    )
    
    # Initialize batch coordinator
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config
    )
    
    # Define repositories to scan
    repositories = [
        Repository(
            name="example-repo-1",
            full_name="owner/example-repo-1",
            owner="owner"
        ),
        Repository(
            name="example-repo-2", 
            full_name="owner/example-repo-2",
            owner="owner"
        ),
        Repository(
            name="example-repo-3",
            full_name="owner/example-repo-3", 
            owner="owner"
        )
    ]
    
    try:
        print("Starting batch scan of repositories...")
        print(f"Scanning {len(repositories)} repositories")
        
        # Process repositories in batches
        results = await coordinator.process_repositories_batch(
            repositories=repositories,
            strategy=BatchStrategy.ADAPTIVE
        )
        
        # Display results
        print("\nScan Results:")
        for repo_name, matches in results.items():
            print(f"\n{repo_name}:")
            if matches:
                for match in matches:
                    print(f"  - {match.package_name} {match.version} in {match.file_path}")
            else:
                print("  No IOC matches found")
        
        # Get and display performance metrics
        metrics = coordinator.get_batch_metrics()
        print(f"\nPerformance Metrics:")
        print(f"  Total requests: {metrics.total_requests}")
        print(f"  Successful requests: {metrics.successful_requests}")
        print(f"  Cache hits: {metrics.cache_hits}")
        print(f"  Cache hit rate: {metrics.cache_hits / metrics.total_requests:.2%}")
        print(f"  Average batch size: {metrics.average_batch_size:.1f}")
        print(f"  Total processing time: {metrics.total_processing_time:.2f}s")
        print(f"  API calls saved: {metrics.api_calls_saved}")
        print(f"  Parallel efficiency: {metrics.parallel_efficiency:.2%}")
        
    except Exception as e:
        print(f"Error during batch scan: {e}")
        raise
    
    finally:
        # Clean up resources
        await coordinator.cleanup()
        print("\nBatch scan completed and resources cleaned up")


async def batch_scan_single_repository():
    """Demonstrate batch scanning of files within a single repository."""
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    
    # Initialize components
    github_client = AsyncGitHubClient(token=github_token)
    cache_manager = CacheManager()
    
    # Configure for single repository scanning
    config = BatchConfig(
        max_concurrent_requests=15,
        default_batch_size=12,
        default_strategy=BatchStrategy.PARALLEL,
        enable_file_prioritization=True
    )
    
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config
    )
    
    # Define repository and files to scan
    repository = Repository(
        name="large-repo",
        full_name="owner/large-repo",
        owner="owner"
    )
    
    # List of files to scan (in a real scenario, these would be discovered)
    file_paths = [
        "package.json",
        "requirements.txt",
        "Gemfile.lock",
        "composer.lock",
        "go.mod",
        "Cargo.lock",
        "src/package.json",
        "backend/requirements.txt",
        "frontend/package-lock.json",
        "services/api/package.json"
    ]
    
    # Priority files (will be processed first)
    priority_files = [
        "package.json",
        "requirements.txt",
        "Gemfile.lock"
    ]
    
    try:
        print(f"Starting batch scan of {repository.full_name}")
        print(f"Scanning {len(file_paths)} files")
        print(f"Priority files: {', '.join(priority_files)}")
        
        # Process files in batches with prioritization
        file_contents = await coordinator.process_files_batch(
            repo=repository,
            file_paths=file_paths,
            priority_files=priority_files
        )
        
        # Display results
        print(f"\nRetrieved {len(file_contents)} files:")
        for file_path, content in file_contents.items():
            print(f"  - {file_path} ({len(content.content)} bytes)")
        
        # Get performance metrics
        metrics = coordinator.get_batch_metrics()
        print(f"\nPerformance Summary:")
        print(f"  Processing time: {metrics.total_processing_time:.2f}s")
        print(f"  Average batch size: {metrics.average_batch_size:.1f}")
        print(f"  Parallel efficiency: {metrics.parallel_efficiency:.2%}")
        
    except Exception as e:
        print(f"Error during file batch scan: {e}")
        raise
    
    finally:
        await coordinator.cleanup()


if __name__ == "__main__":
    print("GitHub IOC Scanner - Basic Batch Processing Example")
    print("=" * 50)
    
    # Run basic repository batch scan
    print("\n1. Basic Repository Batch Scan")
    print("-" * 30)
    asyncio.run(basic_batch_scan())
    
    print("\n" + "=" * 50)
    
    # Run single repository file batch scan
    print("\n2. Single Repository File Batch Scan")
    print("-" * 35)
    asyncio.run(batch_scan_single_repository())