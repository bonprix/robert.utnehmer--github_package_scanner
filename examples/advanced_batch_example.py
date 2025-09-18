#!/usr/bin/env python3
"""
Advanced Batch Processing Example

This example demonstrates advanced batch processing features including:
- Custom configuration optimization
- Cross-repository batching
- Performance monitoring and analysis
- Error handling and recovery
- Memory-efficient processing
"""

import asyncio
import os
import time
from typing import List, Dict, Any

from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from github_ioc_scanner.async_github_client import AsyncGitHubClient
from github_ioc_scanner.cache_manager import CacheManager
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector
from github_ioc_scanner.batch_strategy_manager import BatchStrategyManager
from github_ioc_scanner.resource_manager import ResourceManager
from github_ioc_scanner.models import Repository


class AdvancedBatchProcessor:
    """Advanced batch processor with optimization and monitoring."""
    
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.github_client = AsyncGitHubClient(token=github_token)
        self.cache_manager = CacheManager()
        self.metrics_collector = BatchMetricsCollector()
        self.resource_manager = ResourceManager(max_memory_mb=1000)
        
    async def optimize_and_scan(self, repositories: List[Repository]) -> Dict[str, Any]:
        """Perform optimized batch scanning with performance analysis."""
        
        # Start with adaptive configuration
        config = BatchConfig(
            max_concurrent_requests=15,
            max_concurrent_repos=4,
            default_batch_size=12,
            max_batch_size=60,
            rate_limit_buffer=0.85,
            retry_attempts=4,
            max_memory_usage_mb=1000,
            stream_large_files_threshold=2 * 1024 * 1024,  # 2MB
            default_strategy=BatchStrategy.ADAPTIVE,
            enable_cross_repo_batching=True,
            enable_file_prioritization=True,
            enable_performance_monitoring=True,
            log_batch_metrics=True
        )
        
        coordinator = BatchCoordinator(
            github_client=self.github_client,
            cache_manager=self.cache_manager,
            config=config,
            metrics_collector=self.metrics_collector
        )
        
        try:
            print("🚀 Starting advanced batch processing...")
            print(f"📊 Processing {len(repositories)} repositories")
            
            # Phase 1: Analyze repositories for optimization opportunities
            print("\n📈 Phase 1: Repository Analysis")
            strategy_manager = BatchStrategyManager()
            cross_repo_opportunities = strategy_manager.identify_cross_repo_opportunities(repositories)
            
            if cross_repo_opportunities:
                print(f"✅ Found {len(cross_repo_opportunities)} cross-repository optimization opportunities")
                for opportunity in cross_repo_opportunities:
                    print(f"   - {len(opportunity.repositories)} repos, {len(opportunity.common_files)} common files")
                    print(f"     Estimated savings: {opportunity.estimated_savings:.1f}%")
            else:
                print("ℹ️  No cross-repository optimization opportunities found")
            
            # Phase 2: Execute optimized batch processing
            print("\n⚡ Phase 2: Optimized Batch Processing")
            start_time = time.time()
            
            results = await coordinator.process_repositories_batch(
                repositories=repositories,
                strategy=BatchStrategy.ADAPTIVE
            )
            
            processing_time = time.time() - start_time
            
            # Phase 3: Performance analysis and optimization recommendations
            print("\n📊 Phase 3: Performance Analysis")
            metrics = coordinator.get_batch_metrics()
            summary = self.metrics_collector.get_performance_summary()
            optimizations = self.metrics_collector.identify_optimization_opportunities()
            
            # Display comprehensive results
            self._display_results(results, metrics, summary, optimizations, processing_time)
            
            return {
                'results': results,
                'metrics': metrics,
                'summary': summary,
                'optimizations': optimizations,
                'processing_time': processing_time
            }
            
        except Exception as e:
            print(f"❌ Error during advanced batch processing: {e}")
            raise
        
        finally:
            await coordinator.cleanup()
    
    async def memory_efficient_large_scan(self, repositories: List[Repository]) -> Dict[str, Any]:
        """Demonstrate memory-efficient processing for large-scale scans."""
        
        print("\n🧠 Memory-Efficient Large Scale Scanning")
        print("=" * 45)
        
        # Configure for memory efficiency
        config = BatchConfig(
            max_concurrent_requests=8,  # Reduced for memory efficiency
            max_concurrent_repos=2,
            default_batch_size=6,       # Smaller batches
            max_batch_size=20,
            rate_limit_buffer=0.7,      # Conservative rate limiting
            max_memory_usage_mb=500,    # Limited memory usage
            stream_large_files_threshold=512 * 1024,  # 512KB streaming threshold
            default_strategy=BatchStrategy.CONSERVATIVE,
            enable_performance_monitoring=True
        )
        
        coordinator = BatchCoordinator(
            github_client=self.github_client,
            cache_manager=self.cache_manager,
            config=config,
            metrics_collector=self.metrics_collector
        )
        
        try:
            print(f"💾 Memory limit: {config.max_memory_usage_mb}MB")
            print(f"📦 Batch size: {config.default_batch_size} (max: {config.max_batch_size})")
            print(f"🔄 Concurrency: {config.max_concurrent_requests} requests, {config.max_concurrent_repos} repos")
            
            # Monitor memory usage during processing
            initial_memory = self.resource_manager.get_memory_usage()
            print(f"🏁 Initial memory usage: {initial_memory:.1f}MB")
            
            start_time = time.time()
            results = await coordinator.process_repositories_batch(repositories)
            processing_time = time.time() - start_time
            
            final_memory = self.resource_manager.get_memory_usage()
            peak_memory = max(initial_memory, final_memory)  # Simplified peak tracking
            
            print(f"🏁 Final memory usage: {final_memory:.1f}MB")
            print(f"📈 Peak memory usage: {peak_memory:.1f}MB")
            print(f"⏱️  Processing time: {processing_time:.2f}s")
            
            # Memory efficiency analysis
            metrics = coordinator.get_batch_metrics()
            memory_efficiency = (metrics.total_requests * 1024) / (peak_memory * 1024 * 1024)  # Requests per MB
            
            print(f"🎯 Memory efficiency: {memory_efficiency:.2f} requests/MB")
            
            return {
                'results': results,
                'memory_stats': {
                    'initial_mb': initial_memory,
                    'final_mb': final_memory,
                    'peak_mb': peak_memory,
                    'efficiency': memory_efficiency
                },
                'processing_time': processing_time
            }
            
        finally:
            await coordinator.cleanup()
    
    async def error_resilience_demo(self, repositories: List[Repository]) -> Dict[str, Any]:
        """Demonstrate error handling and resilience features."""
        
        print("\n🛡️  Error Resilience and Recovery Demo")
        print("=" * 40)
        
        # Configure for maximum resilience
        config = BatchConfig(
            max_concurrent_requests=5,   # Conservative concurrency
            default_batch_size=4,        # Small batches for easier recovery
            retry_attempts=6,            # More retry attempts
            retry_delay_base=2.0,        # Longer retry delays
            rate_limit_buffer=0.6,       # Very conservative rate limiting
            default_strategy=BatchStrategy.CONSERVATIVE,
            enable_performance_monitoring=True
        )
        
        coordinator = BatchCoordinator(
            github_client=self.github_client,
            cache_manager=self.cache_manager,
            config=config,
            metrics_collector=self.metrics_collector
        )
        
        # Add some invalid repositories to test error handling
        test_repositories = repositories + [
            Repository(
                name="non-existent-repo",
                full_name="invalid/non-existent-repo",
                owner="invalid"
            ),
            Repository(
                name="private-repo",
                full_name="private/inaccessible-repo", 
                owner="private"
            )
        ]
        
        try:
            print(f"🧪 Testing with {len(test_repositories)} repositories (including invalid ones)")
            print("🔄 Using conservative settings with enhanced error recovery")
            
            start_time = time.time()
            results = await coordinator.process_repositories_batch(test_repositories)
            processing_time = time.time() - start_time
            
            # Analyze error handling effectiveness
            metrics = coordinator.get_batch_metrics()
            success_rate = metrics.successful_requests / metrics.total_requests if metrics.total_requests > 0 else 0
            
            print(f"\n📊 Error Resilience Results:")
            print(f"   ✅ Success rate: {success_rate:.2%}")
            print(f"   🔄 Total requests: {metrics.total_requests}")
            print(f"   ✅ Successful: {metrics.successful_requests}")
            print(f"   ❌ Failed: {metrics.total_requests - metrics.successful_requests}")
            print(f"   ⏱️  Processing time: {processing_time:.2f}s")
            
            # Show which repositories were processed successfully
            print(f"\n📁 Successfully processed repositories:")
            for repo_name in results.keys():
                print(f"   ✅ {repo_name}")
            
            return {
                'results': results,
                'success_rate': success_rate,
                'processing_time': processing_time,
                'error_stats': {
                    'total_requests': metrics.total_requests,
                    'successful_requests': metrics.successful_requests,
                    'failed_requests': metrics.total_requests - metrics.successful_requests
                }
            }
            
        finally:
            await coordinator.cleanup()
    
    def _display_results(self, results: Dict, metrics: Any, summary: Dict, 
                        optimizations: List[str], processing_time: float):
        """Display comprehensive results and analysis."""
        
        print(f"\n🎉 Batch Processing Complete!")
        print(f"⏱️  Total processing time: {processing_time:.2f}s")
        
        # Results summary
        print(f"\n📋 Scan Results Summary:")
        total_matches = sum(len(matches) for matches in results.values())
        print(f"   📁 Repositories processed: {len(results)}")
        print(f"   🔍 Total IOC matches found: {total_matches}")
        
        if total_matches > 0:
            print(f"\n🚨 IOC Matches by Repository:")
            for repo_name, matches in results.items():
                if matches:
                    print(f"   📁 {repo_name}: {len(matches)} matches")
                    for match in matches[:3]:  # Show first 3 matches
                        print(f"      - {match.package_name} {match.version} in {match.file_path}")
                    if len(matches) > 3:
                        print(f"      ... and {len(matches) - 3} more")
        
        # Performance metrics
        print(f"\n📊 Performance Metrics:")
        print(f"   🔢 Total requests: {metrics.total_requests}")
        print(f"   ✅ Successful requests: {metrics.successful_requests}")
        print(f"   💾 Cache hits: {metrics.cache_hits}")
        print(f"   📈 Cache hit rate: {metrics.cache_hits / metrics.total_requests:.2%}")
        print(f"   📦 Average batch size: {metrics.average_batch_size:.1f}")
        print(f"   💾 API calls saved: {metrics.api_calls_saved}")
        print(f"   ⚡ Parallel efficiency: {metrics.parallel_efficiency:.2%}")
        
        # Detailed performance summary
        if summary:
            print(f"\n📈 Detailed Performance Analysis:")
            for key, value in summary.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.3f}")
                else:
                    print(f"   {key}: {value}")
        
        # Optimization recommendations
        if optimizations:
            print(f"\n💡 Optimization Recommendations:")
            for i, opt in enumerate(optimizations, 1):
                print(f"   {i}. {opt}")
        else:
            print(f"\n✅ No optimization recommendations - performance is optimal!")


async def main():
    """Main function demonstrating advanced batch processing."""
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    
    # Initialize advanced batch processor
    processor = AdvancedBatchProcessor(github_token)
    
    # Define test repositories
    repositories = [
        Repository(name="repo1", full_name="owner/repo1", owner="owner"),
        Repository(name="repo2", full_name="owner/repo2", owner="owner"),
        Repository(name="repo3", full_name="owner/repo3", owner="owner"),
        Repository(name="repo4", full_name="owner/repo4", owner="owner"),
        Repository(name="repo5", full_name="owner/repo5", owner="owner"),
    ]
    
    print("🔬 GitHub IOC Scanner - Advanced Batch Processing Demo")
    print("=" * 55)
    
    try:
        # Demo 1: Optimized batch processing with analysis
        print("\n🚀 Demo 1: Optimized Batch Processing")
        results1 = await processor.optimize_and_scan(repositories)
        
        # Demo 2: Memory-efficient processing
        print("\n" + "=" * 55)
        results2 = await processor.memory_efficient_large_scan(repositories)
        
        # Demo 3: Error resilience
        print("\n" + "=" * 55)
        results3 = await processor.error_resilience_demo(repositories[:3])  # Use fewer repos for error demo
        
        # Final summary
        print("\n" + "=" * 55)
        print("🎯 Advanced Batch Processing Demo Complete!")
        print("\nKey Takeaways:")
        print("✅ Batch processing can significantly improve performance")
        print("✅ Adaptive strategies automatically optimize based on conditions")
        print("✅ Memory-efficient processing enables large-scale scans")
        print("✅ Error resilience ensures reliable operation")
        print("✅ Performance monitoring provides optimization insights")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())