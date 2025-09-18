#!/usr/bin/env python3
"""
Example demonstrating memory-efficient batch processing with resource management.

This example shows how to use the memory monitoring, streaming processing,
and resource management features for efficient batch operations.
"""

import asyncio
import logging
from datetime import datetime
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.batch_models import BatchRequest, BatchConfig
from src.github_ioc_scanner.models import Repository
from src.github_ioc_scanner.parallel_batch_processor import ParallelBatchProcessor
from src.github_ioc_scanner.streaming_batch_processor import StreamingBatchProcessor, StreamingConfig
from src.github_ioc_scanner.memory_monitor import MemoryMonitor
from src.github_ioc_scanner.resource_manager import ResourceManager, ResourceConfig


async def demonstrate_memory_monitoring():
    """Demonstrate memory monitoring capabilities."""
    print("\n=== Memory Monitoring Demo ===")
    
    # Create memory monitor
    monitor = MemoryMonitor(
        max_memory_threshold=0.8,
        critical_memory_threshold=0.9,
        min_batch_size=1,
        max_batch_size=50
    )
    
    # Set baseline memory
    monitor.set_baseline_memory()
    print(f"Baseline memory set")
    
    # Get memory statistics
    stats = monitor.get_memory_stats()
    print(f"Current memory usage: {stats.percent_used:.1%}")
    print(f"Process memory: {stats.process_mb:.1f} MB")
    
    # Check if batch size should be reduced
    should_reduce = monitor.should_reduce_batch_size()
    print(f"Should reduce batch size: {should_reduce}")
    
    # Calculate adjusted batch size
    current_batch_size = 20
    adjusted_size = monitor.calculate_adjusted_batch_size(current_batch_size)
    print(f"Batch size adjustment: {current_batch_size} -> {adjusted_size}")
    
    # Get comprehensive memory report
    report = monitor.get_memory_report()
    print(f"Memory report: {report['current_stats']}")


async def demonstrate_streaming_processing():
    """Demonstrate streaming batch processing."""
    print("\n=== Streaming Processing Demo ===")
    
    # Create mock GitHub client
    github_client = AsyncGitHubClient("fake-token")
    
    # Configure streaming
    streaming_config = StreamingConfig(
        chunk_size=5,
        max_memory_per_chunk_mb=50.0,
        enable_memory_monitoring=True,
        stream_threshold=10,
        max_concurrent_chunks=2
    )
    
    # Create streaming processor
    processor = StreamingBatchProcessor(
        github_client,
        streaming_config
    )
    
    # Create sample requests
    sample_repo = Repository(
        name="test-repo",
        full_name="owner/test-repo",
        default_branch="main",
        archived=False,
        updated_at=datetime.now()
    )
    
    requests = [
        BatchRequest(
            repo=sample_repo,
            file_path=f"file_{i}.txt",
            priority=1,
            estimated_size=1024 * i
        )
        for i in range(1, 16)  # 15 requests
    ]
    
    # Check if streaming should be used
    should_stream = await processor.should_use_streaming(requests)
    print(f"Should use streaming for {len(requests)} requests: {should_stream}")
    
    # Create chunks
    chunks = processor.create_chunks(requests)
    print(f"Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i}: {len(chunk)} requests")
    
    # Estimate memory usage
    estimated_memory = await processor.estimate_memory_usage(requests)
    print(f"Estimated memory usage: {estimated_memory:.2f} MB")
    
    # Get streaming statistics
    stats = processor.get_streaming_stats()
    print(f"Streaming config: chunk_size={stats['config']['chunk_size']}, "
          f"threshold={stats['config']['stream_threshold']}")


async def demonstrate_resource_management():
    """Demonstrate resource management capabilities."""
    print("\n=== Resource Management Demo ===")
    
    # Create resource manager with custom config
    config = ResourceConfig(
        auto_cleanup_enabled=False,  # Disable for demo
        cleanup_interval_seconds=30.0,
        memory_cleanup_threshold=0.8,
        max_resource_age_seconds=60.0,
        force_gc_on_cleanup=True
    )
    
    manager = ResourceManager(config)
    
    # Demonstrate managed resource context
    print("Creating managed resources...")
    
    async with manager.managed_resource("demo-resource-1") as resource1:
        print(f"Created resource: {resource1.resource_id}")
        
        async with manager.managed_batch_resource(
            "demo-batch-resource",
            batch_data={"demo": "data"}
        ) as batch_resource:
            print(f"Created batch resource: {batch_resource.resource_id}")
            batch_resource.results.extend([1, 2, 3])
            
            # Get resource statistics
            stats = manager.get_resource_stats()
            print(f"Active resources: {stats['resource_stats']['active_resources']}")
            print(f"Total created: {stats['resource_stats']['total_resources_created']}")
    
    # Resources should be cleaned up automatically
    final_stats = manager.get_resource_stats()
    print(f"Final active resources: {final_stats['resource_stats']['active_resources']}")
    print(f"Total cleaned: {final_stats['resource_stats']['total_resources_cleaned']}")
    
    # Shutdown resource manager
    await manager.shutdown()


async def demonstrate_integrated_processing():
    """Demonstrate integrated memory-efficient batch processing."""
    print("\n=== Integrated Processing Demo ===")
    
    # Create mock GitHub client
    github_client = AsyncGitHubClient("fake-token")
    
    # Configure batch processing with memory efficiency
    batch_config = BatchConfig(
        max_concurrent_requests=5,
        max_batch_size=20,
        min_batch_size=2,
        max_memory_usage_mb=200,  # 200MB limit
        retry_attempts=2
    )
    
    # Create processor with memory monitoring
    processor = ParallelBatchProcessor(github_client, batch_config)
    
    # Get initial memory stats
    memory_stats = processor.get_memory_stats()
    print(f"Initial memory usage: {memory_stats['current_stats']['memory_usage_percent']:.1f}%")
    
    # Check memory pressure
    should_reduce, is_critical = processor.check_memory_pressure()
    print(f"Memory pressure - should reduce: {should_reduce}, critical: {is_critical}")
    
    # Get resource statistics
    resource_stats = processor.get_resource_stats()
    print(f"Resource manager active: {resource_stats['resource_stats']['active_resources']}")
    
    # Demonstrate cleanup
    cleanup_stats = await processor.cleanup_resources()
    print(f"Cleanup performed - freed {cleanup_stats.get('memory_freed_mb', 0):.2f} MB")
    
    # Shutdown processor
    await processor.shutdown_processor()
    print("Processor shutdown complete")


async def main():
    """Run all demonstrations."""
    print("Memory-Efficient Batch Processing Demo")
    print("=" * 50)
    
    try:
        await demonstrate_memory_monitoring()
        await demonstrate_streaming_processing()
        await demonstrate_resource_management()
        await demonstrate_integrated_processing()
        
        print("\n=== Demo Complete ===")
        print("All memory-efficient processing features demonstrated successfully!")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())