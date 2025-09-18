# Batch Processing Tutorial

## Introduction

This tutorial will guide you through using the GitHub IOC Scanner's advanced batch processing capabilities to dramatically improve scanning performance. You'll learn how to configure, optimize, and troubleshoot batch operations for different scenarios.

## Prerequisites

- Python 3.8 or higher
- GitHub personal access token
- GitHub IOC Scanner installed
- Basic understanding of async/await in Python

## Tutorial Overview

1. [Getting Started with Basic Batch Processing](#getting-started)
2. [Understanding Batch Strategies](#batch-strategies)
3. [Optimizing Performance](#optimizing-performance)
4. [Memory-Efficient Processing](#memory-efficient-processing)
5. [Error Handling and Resilience](#error-handling)
6. [Advanced Configuration](#advanced-configuration)
7. [Monitoring and Metrics](#monitoring-and-metrics)
8. [Troubleshooting Common Issues](#troubleshooting)

## Getting Started

### Step 1: Basic Setup

First, let's set up the basic components for batch processing:

```python
import asyncio
import os
from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from github_ioc_scanner.async_github_client import AsyncGitHubClient
from github_ioc_scanner.cache_manager import CacheManager

# Get your GitHub token
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("Please set GITHUB_TOKEN environment variable")

# Initialize components
github_client = AsyncGitHubClient(token=github_token)
cache_manager = CacheManager()
```

### Step 2: Basic Configuration

Create a basic batch configuration:

```python
# Start with conservative settings
config = BatchConfig(
    max_concurrent_requests=5,    # Start small
    default_batch_size=8,         # Moderate batch size
    default_strategy=BatchStrategy.ADAPTIVE,  # Let the system optimize
    enable_performance_monitoring=True        # Always monitor performance
)

# Initialize the batch coordinator
coordinator = BatchCoordinator(
    github_client=github_client,
    cache_manager=cache_manager,
    config=config
)
```

### Step 3: Your First Batch Scan

Let's perform a simple batch scan:

```python
from github_ioc_scanner.models import Repository

async def first_batch_scan():
    # Define repositories to scan
    repositories = [
        Repository(name="repo1", full_name="owner/repo1", owner="owner"),
        Repository(name="repo2", full_name="owner/repo2", owner="owner"),
    ]
    
    try:
        print("Starting batch scan...")
        
        # Process repositories in batches
        results = await coordinator.process_repositories_batch(repositories)
        
        # Display results
        for repo_name, matches in results.items():
            print(f"{repo_name}: {len(matches)} IOC matches found")
        
        # Get performance metrics
        metrics = coordinator.get_batch_metrics()
        print(f"Processed {metrics.total_requests} requests in {metrics.total_processing_time:.2f}s")
        
    finally:
        await coordinator.cleanup()

# Run the scan
asyncio.run(first_batch_scan())
```

**Expected Output:**
```
Starting batch scan...
owner/repo1: 3 IOC matches found
owner/repo2: 0 IOC matches found
Processed 15 requests in 2.34s
```

## Batch Strategies

Understanding and choosing the right batch strategy is crucial for optimal performance.

### Available Strategies

#### 1. ADAPTIVE (Recommended)
Automatically adjusts based on current conditions:

```python
config = BatchConfig(
    default_strategy=BatchStrategy.ADAPTIVE,
    max_concurrent_requests=10,
    default_batch_size=12
)
```

**When to use:** Most scenarios, especially when conditions vary

#### 2. PARALLEL
Maximizes parallel processing:

```python
config = BatchConfig(
    default_strategy=BatchStrategy.PARALLEL,
    max_concurrent_requests=20,
    default_batch_size=15
)
```

**When to use:** High rate limits, stable network, abundant resources

#### 3. CONSERVATIVE
Minimizes resource usage and risk:

```python
config = BatchConfig(
    default_strategy=BatchStrategy.CONSERVATIVE,
    max_concurrent_requests=3,
    default_batch_size=5
)
```

**When to use:** Limited resources, unreliable network, rate-limited tokens

#### 4. AGGRESSIVE
Maximizes throughput at the cost of resources:

```python
config = BatchConfig(
    default_strategy=BatchStrategy.AGGRESSIVE,
    max_concurrent_requests=25,
    default_batch_size=20,
    rate_limit_buffer=0.95
)
```

**When to use:** Time-critical scans, high-performance environments

### Strategy Comparison Example

```python
async def compare_strategies():
    """Compare different batch strategies."""
    
    strategies = [
        (BatchStrategy.CONSERVATIVE, "Conservative"),
        (BatchStrategy.ADAPTIVE, "Adaptive"),
        (BatchStrategy.PARALLEL, "Parallel"),
        (BatchStrategy.AGGRESSIVE, "Aggressive")
    ]
    
    repositories = [
        Repository(name=f"repo{i}", full_name=f"owner/repo{i}", owner="owner")
        for i in range(1, 6)
    ]
    
    results = {}
    
    for strategy, name in strategies:
        config = BatchConfig(
            default_strategy=strategy,
            enable_performance_monitoring=True
        )
        
        coordinator = BatchCoordinator(
            github_client=github_client,
            cache_manager=cache_manager,
            config=config
        )
        
        try:
            start_time = time.time()
            await coordinator.process_repositories_batch(repositories)
            processing_time = time.time() - start_time
            
            metrics = coordinator.get_batch_metrics()
            results[name] = {
                'time': processing_time,
                'requests': metrics.total_requests,
                'efficiency': metrics.parallel_efficiency
            }
            
        finally:
            await coordinator.cleanup()
    
    # Display comparison
    print("Strategy Comparison:")
    for name, data in results.items():
        print(f"{name:12}: {data['time']:.2f}s, {data['efficiency']:.1%} efficiency")

asyncio.run(compare_strategies())
```

## Optimizing Performance

### Step 1: Baseline Measurement

Always start by measuring current performance:

```python
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector

async def measure_baseline():
    """Measure baseline performance."""
    
    metrics_collector = BatchMetricsCollector()
    
    config = BatchConfig(
        enable_performance_monitoring=True,
        log_batch_metrics=True
    )
    
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config,
        metrics_collector=metrics_collector
    )
    
    # Your scan code here...
    
    # Analyze performance
    summary = metrics_collector.get_performance_summary()
    optimizations = metrics_collector.identify_optimization_opportunities()
    
    print("Performance Summary:", summary)
    print("Optimization Opportunities:", optimizations)
```

### Step 2: Iterative Optimization

Optimize one parameter at a time:

```python
async def optimize_concurrency():
    """Find optimal concurrency level."""
    
    concurrency_levels = [5, 10, 15, 20, 25]
    results = {}
    
    for concurrency in concurrency_levels:
        config = BatchConfig(
            max_concurrent_requests=concurrency,
            enable_performance_monitoring=True
        )
        
        coordinator = BatchCoordinator(
            github_client=github_client,
            cache_manager=cache_manager,
            config=config
        )
        
        try:
            start_time = time.time()
            await coordinator.process_repositories_batch(repositories)
            processing_time = time.time() - start_time
            
            metrics = coordinator.get_batch_metrics()
            results[concurrency] = {
                'time': processing_time,
                'success_rate': metrics.successful_requests / metrics.total_requests,
                'efficiency': metrics.parallel_efficiency
            }
            
        finally:
            await coordinator.cleanup()
    
    # Find optimal concurrency
    optimal = min(results.items(), key=lambda x: x[1]['time'])
    print(f"Optimal concurrency: {optimal[0]} ({optimal[1]['time']:.2f}s)")
```

### Step 3: Batch Size Optimization

```python
async def optimize_batch_size():
    """Find optimal batch size."""
    
    batch_sizes = [5, 8, 12, 16, 20, 25]
    results = {}
    
    for batch_size in batch_sizes:
        config = BatchConfig(
            default_batch_size=batch_size,
            max_batch_size=batch_size * 2,
            enable_performance_monitoring=True
        )
        
        coordinator = BatchCoordinator(
            github_client=github_client,
            cache_manager=cache_manager,
            config=config
        )
        
        try:
            start_time = time.time()
            await coordinator.process_files_batch(
                repo=repository,
                file_paths=file_list
            )
            processing_time = time.time() - start_time
            
            results[batch_size] = processing_time
            
        finally:
            await coordinator.cleanup()
    
    # Find optimal batch size
    optimal_size = min(results.items(), key=lambda x: x[1])
    print(f"Optimal batch size: {optimal_size[0]} ({optimal_size[1]:.2f}s)")
```

## Memory-Efficient Processing

For large-scale scans, memory efficiency is crucial:

### Step 1: Configure Memory Limits

```python
config = BatchConfig(
    max_memory_usage_mb=500,                    # Limit memory usage
    stream_large_files_threshold=1024 * 1024,  # Stream files > 1MB
    default_batch_size=8,                      # Smaller batches
    max_batch_size=20,                         # Lower maximum
    default_strategy=BatchStrategy.CONSERVATIVE
)
```

### Step 2: Use Streaming for Large Batches

```python
from github_ioc_scanner.streaming_batch_processor import StreamingBatchProcessor

async def memory_efficient_scan():
    """Perform memory-efficient scanning."""
    
    streaming_processor = StreamingBatchProcessor(
        chunk_size=10,
        max_memory_mb=300
    )
    
    # Process large batch with streaming
    large_batch_requests = create_large_batch()  # Your batch creation logic
    
    async for batch_chunk in streaming_processor.process_large_batch_streaming(
        large_batch_requests
    ):
        # Process each chunk as it becomes available
        for result in batch_chunk:
            if result.content:
                process_file_content(result.content)
            
        # Memory is automatically managed between chunks
```

### Step 3: Monitor Memory Usage

```python
from github_ioc_scanner.resource_manager import ResourceManager

async def monitor_memory_usage():
    """Monitor and manage memory usage during scanning."""
    
    resource_manager = ResourceManager(
        max_memory_mb=500,
        cleanup_threshold=0.8
    )
    
    config = BatchConfig(
        max_memory_usage_mb=500,
        enable_performance_monitoring=True
    )
    
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config
    )
    
    try:
        initial_memory = resource_manager.get_memory_usage()
        print(f"Initial memory: {initial_memory:.1f}MB")
        
        # Perform scanning with memory monitoring
        results = await coordinator.process_repositories_batch(repositories)
        
        # Check if batch size should be reduced
        if resource_manager.should_reduce_batch_size():
            print("⚠️  High memory usage detected - consider reducing batch size")
        
        final_memory = resource_manager.get_memory_usage()
        print(f"Final memory: {final_memory:.1f}MB")
        
    finally:
        # Clean up resources
        resource_manager.cleanup_batch_resources([])
        await coordinator.cleanup()
```

## Error Handling and Resilience

Robust error handling ensures your scans complete successfully:

### Step 1: Configure Retry Logic

```python
config = BatchConfig(
    retry_attempts=5,           # More retry attempts
    retry_delay_base=2.0,       # Longer base delay
    rate_limit_buffer=0.7,      # Conservative rate limiting
    default_strategy=BatchStrategy.CONSERVATIVE
)
```

### Step 2: Handle Different Error Types

```python
from github_ioc_scanner.batch_error_handler import BatchErrorHandler

async def resilient_scan():
    """Perform scanning with comprehensive error handling."""
    
    error_handler = BatchErrorHandler()
    
    config = BatchConfig(
        retry_attempts=4,
        retry_delay_base=1.5,
        enable_performance_monitoring=True
    )
    
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config
    )
    
    try:
        # Include some potentially problematic repositories
        test_repositories = repositories + [
            Repository(name="nonexistent", full_name="invalid/nonexistent", owner="invalid")
        ]
        
        results = await coordinator.process_repositories_batch(test_repositories)
        
        # Analyze success rate
        metrics = coordinator.get_batch_metrics()
        success_rate = metrics.successful_requests / metrics.total_requests
        
        print(f"Success rate: {success_rate:.2%}")
        print(f"Successfully processed: {len(results)} repositories")
        
        if success_rate < 0.9:
            print("⚠️  Low success rate - check error logs")
        
    except Exception as e:
        print(f"❌ Scan failed: {e}")
        # Implement your error recovery logic here
        
    finally:
        await coordinator.cleanup()
```

### Step 3: Implement Circuit Breaker Pattern

```python
class CircuitBreaker:
    """Simple circuit breaker for batch operations."""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def can_execute(self):
        """Check if operation can be executed."""
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        """Record successful operation."""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        """Record failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

async def scan_with_circuit_breaker():
    """Scan with circuit breaker protection."""
    
    circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
    
    for repo in repositories:
        if not circuit_breaker.can_execute():
            print(f"⚠️  Circuit breaker OPEN - skipping {repo.name}")
            continue
        
        try:
            # Perform individual repository scan
            result = await coordinator.process_repositories_batch([repo])
            circuit_breaker.record_success()
            print(f"✅ {repo.name} processed successfully")
            
        except Exception as e:
            circuit_breaker.record_failure()
            print(f"❌ {repo.name} failed: {e}")
```

## Advanced Configuration

### Environment-Specific Configurations

Create different configurations for different environments:

```python
def get_config_for_environment(env: str) -> BatchConfig:
    """Get configuration optimized for specific environment."""
    
    if env == "development":
        return BatchConfig(
            max_concurrent_requests=5,
            default_batch_size=6,
            default_strategy=BatchStrategy.ADAPTIVE,
            enable_performance_monitoring=True,
            log_batch_metrics=True
        )
    
    elif env == "production":
        return BatchConfig(
            max_concurrent_requests=15,
            default_batch_size=12,
            max_batch_size=50,
            rate_limit_buffer=0.8,
            retry_attempts=4,
            max_memory_usage_mb=1000,
            default_strategy=BatchStrategy.ADAPTIVE,
            enable_cross_repo_batching=True,
            enable_file_prioritization=True,
            enable_performance_monitoring=True,
            log_batch_metrics=False
        )
    
    elif env == "high_performance":
        return BatchConfig(
            max_concurrent_requests=25,
            max_concurrent_repos=8,
            default_batch_size=20,
            max_batch_size=100,
            rate_limit_buffer=0.95,
            retry_attempts=3,
            max_memory_usage_mb=2000,
            stream_large_files_threshold=5 * 1024 * 1024,
            default_strategy=BatchStrategy.AGGRESSIVE,
            enable_cross_repo_batching=True,
            enable_file_prioritization=True,
            enable_performance_monitoring=True
        )
    
    else:
        raise ValueError(f"Unknown environment: {env}")

# Usage
env = os.getenv("ENVIRONMENT", "development")
config = get_config_for_environment(env)
```

### Configuration from Files

Load configuration from YAML files:

```python
import yaml

def load_config_from_file(config_path: str) -> BatchConfig:
    """Load batch configuration from YAML file."""
    
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    batch_config = config_data.get('batch', {})
    
    return BatchConfig(
        max_concurrent_requests=batch_config.get('max_concurrent_requests', 10),
        default_batch_size=batch_config.get('default_batch_size', 10),
        max_batch_size=batch_config.get('max_batch_size', 50),
        rate_limit_buffer=batch_config.get('rate_limit_buffer', 0.8),
        retry_attempts=batch_config.get('retry_attempts', 3),
        max_memory_usage_mb=batch_config.get('max_memory_usage_mb', 500),
        default_strategy=BatchStrategy(batch_config.get('default_strategy', 'adaptive')),
        enable_cross_repo_batching=batch_config.get('enable_cross_repo_batching', True),
        enable_file_prioritization=batch_config.get('enable_file_prioritization', True),
        enable_performance_monitoring=batch_config.get('enable_performance_monitoring', True),
        log_batch_metrics=batch_config.get('log_batch_metrics', False)
    )

# Usage
config = load_config_from_file('batch_config.yaml')
```

## Monitoring and Metrics

### Comprehensive Performance Monitoring

```python
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector
from github_ioc_scanner.batch_progress_monitor import BatchProgressMonitor

async def comprehensive_monitoring():
    """Demonstrate comprehensive performance monitoring."""
    
    # Initialize monitoring components
    metrics_collector = BatchMetricsCollector()
    progress_monitor = BatchProgressMonitor()
    
    config = BatchConfig(
        enable_performance_monitoring=True,
        log_batch_metrics=True
    )
    
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config,
        metrics_collector=metrics_collector
    )
    
    try:
        # Start progress monitoring
        progress_monitor.start_monitoring()
        
        # Perform scanning with monitoring
        total_repos = len(repositories)
        for i, repo in enumerate(repositories):
            # Update progress
            progress_monitor.update_progress(
                completed=i,
                total=total_repos,
                current_batch_size=config.default_batch_size,
                eta_seconds=(total_repos - i) * 2  # Estimated 2s per repo
            )
            
            # Process repository
            await coordinator.process_repositories_batch([repo])
        
        # Final progress update
        progress_monitor.update_progress(
            completed=total_repos,
            total=total_repos,
            current_batch_size=0,
            eta_seconds=0
        )
        
        # Analyze comprehensive metrics
        summary = metrics_collector.get_performance_summary()
        optimizations = metrics_collector.identify_optimization_opportunities()
        
        print("\n📊 Comprehensive Performance Report:")
        print("=" * 40)
        
        # Performance summary
        print("Performance Summary:")
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.3f}")
            else:
                print(f"  {key}: {value}")
        
        # Optimization recommendations
        if optimizations:
            print("\nOptimization Recommendations:")
            for i, opt in enumerate(optimizations, 1):
                print(f"  {i}. {opt}")
        
        # Batch metrics
        metrics = coordinator.get_batch_metrics()
        print(f"\nBatch Metrics:")
        print(f"  Total requests: {metrics.total_requests}")
        print(f"  Success rate: {metrics.successful_requests / metrics.total_requests:.2%}")
        print(f"  Cache hit rate: {metrics.cache_hits / metrics.total_requests:.2%}")
        print(f"  Parallel efficiency: {metrics.parallel_efficiency:.2%}")
        print(f"  API calls saved: {metrics.api_calls_saved}")
        
    finally:
        await coordinator.cleanup()
```

### Custom Metrics Collection

```python
class CustomMetricsCollector:
    """Custom metrics collector for specific use cases."""
    
    def __init__(self):
        self.repo_processing_times = {}
        self.file_type_stats = {}
        self.error_categories = {}
    
    def record_repo_processing(self, repo_name: str, processing_time: float, file_count: int):
        """Record repository processing metrics."""
        self.repo_processing_times[repo_name] = {
            'time': processing_time,
            'files': file_count,
            'files_per_second': file_count / processing_time if processing_time > 0 else 0
        }
    
    def record_file_type(self, file_type: str, processing_time: float):
        """Record file type processing metrics."""
        if file_type not in self.file_type_stats:
            self.file_type_stats[file_type] = {'count': 0, 'total_time': 0}
        
        self.file_type_stats[file_type]['count'] += 1
        self.file_type_stats[file_type]['total_time'] += processing_time
    
    def record_error(self, error_type: str):
        """Record error occurrence."""
        self.error_categories[error_type] = self.error_categories.get(error_type, 0) + 1
    
    def get_custom_report(self) -> dict:
        """Generate custom performance report."""
        return {
            'repo_stats': self.repo_processing_times,
            'file_type_stats': {
                ft: {
                    'count': stats['count'],
                    'avg_time': stats['total_time'] / stats['count']
                }
                for ft, stats in self.file_type_stats.items()
            },
            'error_stats': self.error_categories
        }

# Usage in scanning
custom_metrics = CustomMetricsCollector()

async def scan_with_custom_metrics():
    """Scan with custom metrics collection."""
    
    for repo in repositories:
        start_time = time.time()
        
        try:
            results = await coordinator.process_repositories_batch([repo])
            processing_time = time.time() - start_time
            
            # Record custom metrics
            file_count = sum(len(matches) for matches in results.values())
            custom_metrics.record_repo_processing(repo.name, processing_time, file_count)
            
        except Exception as e:
            custom_metrics.record_error(type(e).__name__)
    
    # Generate custom report
    report = custom_metrics.get_custom_report()
    print("Custom Metrics Report:", report)
```

## Troubleshooting Common Issues

### Issue 1: High Memory Usage

**Symptoms:**
- Out of memory errors
- System slowdown
- Swap usage increase

**Solutions:**

```python
# Reduce memory usage
config = BatchConfig(
    max_memory_usage_mb=300,           # Lower memory limit
    stream_large_files_threshold=512 * 1024,  # Stream smaller files
    default_batch_size=5,              # Smaller batches
    max_batch_size=15,                 # Lower maximum
    default_strategy=BatchStrategy.CONSERVATIVE
)

# Monitor memory usage
from github_ioc_scanner.resource_manager import ResourceManager

resource_manager = ResourceManager(max_memory_mb=300)

async def memory_conscious_scan():
    for batch in create_batches(repositories, batch_size=3):
        if resource_manager.should_reduce_batch_size():
            batch = batch[:len(batch)//2]  # Reduce batch size
        
        await process_batch(batch)
        resource_manager.cleanup_batch_resources([])  # Clean up after each batch
```

### Issue 2: Rate Limit Errors

**Symptoms:**
- 403 HTTP errors
- "API rate limit exceeded" messages
- Slow processing due to rate limiting

**Solutions:**

```python
# Conservative rate limiting
config = BatchConfig(
    max_concurrent_requests=3,         # Reduce concurrency
    rate_limit_buffer=0.5,             # Use only 50% of rate limit
    retry_attempts=6,                  # More retries
    retry_delay_base=3.0,              # Longer delays
    default_strategy=BatchStrategy.CONSERVATIVE
)

# Monitor rate limits
async def rate_limit_aware_scan():
    rate_limit_remaining = await github_client.get_rate_limit_remaining()
    
    if rate_limit_remaining < 100:
        print("⚠️  Low rate limit - using conservative settings")
        config.max_concurrent_requests = 1
        config.default_batch_size = 3
    
    # Proceed with scan...
```

### Issue 3: Network Timeouts

**Symptoms:**
- Connection timeout errors
- Intermittent failures
- Slow response times

**Solutions:**

```python
# Network resilience configuration
config = BatchConfig(
    max_concurrent_requests=5,         # Reduce load
    retry_attempts=8,                  # More retries
    retry_delay_base=2.0,              # Longer delays
    default_strategy=BatchStrategy.CONSERVATIVE
)

# Implement network health checking
async def network_resilient_scan():
    max_consecutive_failures = 3
    consecutive_failures = 0
    
    for repo in repositories:
        try:
            await coordinator.process_repositories_batch([repo])
            consecutive_failures = 0  # Reset on success
            
        except Exception as e:
            consecutive_failures += 1
            
            if consecutive_failures >= max_consecutive_failures:
                print("⚠️  Multiple network failures - pausing for 30 seconds")
                await asyncio.sleep(30)
                consecutive_failures = 0
            
            print(f"❌ Failed to process {repo.name}: {e}")
```

### Issue 4: Poor Performance

**Symptoms:**
- Slow scan times
- Low throughput
- Poor parallel efficiency

**Diagnostic Steps:**

```python
async def diagnose_performance():
    """Diagnose performance issues."""
    
    # Enable detailed monitoring
    config = BatchConfig(
        enable_performance_monitoring=True,
        log_batch_metrics=True
    )
    
    metrics_collector = BatchMetricsCollector()
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config,
        metrics_collector=metrics_collector
    )
    
    try:
        # Run test scan
        start_time = time.time()
        await coordinator.process_repositories_batch(repositories[:3])  # Test with 3 repos
        total_time = time.time() - start_time
        
        # Analyze performance
        metrics = coordinator.get_batch_metrics()
        summary = metrics_collector.get_performance_summary()
        optimizations = metrics_collector.identify_optimization_opportunities()
        
        print("Performance Diagnosis:")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Requests per second: {metrics.total_requests / total_time:.2f}")
        print(f"  Parallel efficiency: {metrics.parallel_efficiency:.2%}")
        print(f"  Cache hit rate: {metrics.cache_hits / metrics.total_requests:.2%}")
        
        if metrics.parallel_efficiency < 0.5:
            print("⚠️  Low parallel efficiency - consider:")
            print("    - Increasing batch size")
            print("    - Reducing concurrency")
            print("    - Checking network latency")
        
        if metrics.cache_hits / metrics.total_requests < 0.2:
            print("⚠️  Low cache hit rate - consider:")
            print("    - Running scans more frequently")
            print("    - Checking cache configuration")
        
        print("Optimization recommendations:")
        for opt in optimizations:
            print(f"  - {opt}")
    
    finally:
        await coordinator.cleanup()
```

## Best Practices Summary

### 1. Configuration Best Practices

- **Start Conservative**: Begin with conservative settings and optimize incrementally
- **Monitor Performance**: Always enable performance monitoring during optimization
- **Environment-Specific**: Use different configurations for different environments
- **Version Control**: Keep configuration files in version control

### 2. Performance Optimization

- **Measure First**: Always measure baseline performance before optimizing
- **One Change at a Time**: Optimize one parameter at a time
- **Consider Trade-offs**: Balance performance, reliability, and resource usage
- **Regular Review**: Regularly review and update configurations

### 3. Error Handling

- **Expect Failures**: Design for partial failures and recovery
- **Retry Logic**: Implement appropriate retry strategies
- **Circuit Breakers**: Use circuit breakers for persistent failures
- **Monitoring**: Monitor error rates and patterns

### 4. Resource Management

- **Memory Limits**: Set appropriate memory limits
- **Streaming**: Use streaming for large files
- **Cleanup**: Always clean up resources
- **Monitoring**: Monitor resource usage

### 5. Security and Rate Limiting

- **Respect Limits**: Stay well within API rate limits
- **Token Management**: Use appropriate tokens for your use case
- **Error Handling**: Handle authentication errors gracefully
- **Monitoring**: Monitor API usage patterns

## Conclusion

This tutorial has covered the essential aspects of using the GitHub IOC Scanner's batch processing capabilities. Key takeaways:

1. **Start Simple**: Begin with basic configurations and gradually optimize
2. **Monitor Everything**: Use performance monitoring to guide optimization
3. **Handle Errors**: Implement robust error handling and recovery
4. **Manage Resources**: Be mindful of memory and API usage
5. **Iterate**: Continuously monitor and improve your configurations

With these techniques, you can achieve significant performance improvements while maintaining reliability and staying within resource constraints.

For more advanced topics and specific use cases, refer to the [Batch API Documentation](BATCH_API_DOCUMENTATION.md) and [Configuration Guide](BATCH_CONFIGURATION_GUIDE.md).