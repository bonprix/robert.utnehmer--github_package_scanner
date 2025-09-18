# Batch API Documentation

## Overview

The GitHub IOC Scanner's Batch API provides advanced batch processing capabilities that can dramatically improve scanning performance for large-scale operations. The batch system implements intelligent parallel processing, dynamic optimization, and sophisticated error handling to achieve 60-80% performance improvements over sequential scanning.

## Core Components

### BatchCoordinator

The `BatchCoordinator` is the central orchestrator for all batch operations, providing a unified interface for batch processing.

```python
from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchStrategy

# Initialize coordinator
coordinator = BatchCoordinator(
    github_client=github_client,
    cache_manager=cache_manager,
    config=batch_config
)

# Process multiple repositories
results = await coordinator.process_repositories_batch(
    repositories=repo_list,
    strategy=BatchStrategy.ADAPTIVE
)

# Process files within a repository
file_contents = await coordinator.process_files_batch(
    repo=repository,
    file_paths=file_list,
    priority_files=["package.json", "requirements.txt"]
)
```

#### Key Methods

- `process_repositories_batch()`: Process multiple repositories with optimal batching
- `process_files_batch()`: Process multiple files with intelligent batching
- `get_batch_metrics()`: Get detailed performance metrics
- `cleanup()`: Clean up resources after batch operations

### ParallelBatchProcessor

Handles concurrent API requests with intelligent throttling and rate limit management.

```python
from github_ioc_scanner.parallel_batch_processor import ParallelBatchProcessor

# Initialize processor
processor = ParallelBatchProcessor(
    max_concurrent=10,
    rate_limit_buffer=0.8,
    retry_attempts=3
)

# Process batch requests in parallel
results = await processor.process_batch_parallel(batch_requests)
```

#### Configuration Options

- `max_concurrent`: Maximum number of concurrent requests (default: 10)
- `rate_limit_buffer`: Percentage of rate limit to use (default: 0.8)
- `retry_attempts`: Number of retry attempts for failed requests (default: 3)

### BatchStrategyManager

Implements intelligent batching decisions based on file characteristics and system conditions.

```python
from github_ioc_scanner.batch_strategy_manager import BatchStrategyManager

# Initialize strategy manager
strategy_manager = BatchStrategyManager()

# Calculate optimal batch size
batch_size = strategy_manager.calculate_optimal_batch_size(
    files=file_info_list,
    rate_limit_remaining=remaining_requests,
    network_conditions=network_info
)

# Prioritize files by importance
prioritized_files = strategy_manager.prioritize_files(file_paths)

# Identify cross-repository batching opportunities
cross_repo_batches = strategy_manager.identify_cross_repo_opportunities(repositories)
```

### AsyncGitHubClient

Extended GitHub client with advanced batch capabilities and parallel processing.

```python
from github_ioc_scanner.async_github_client import AsyncGitHubClient

# Initialize async client
async_client = AsyncGitHubClient(token=github_token)

# Get multiple file contents in parallel
file_contents = await async_client.get_multiple_file_contents_parallel(
    repo=repository,
    file_paths=file_list,
    max_concurrent=5
)

# Stream large file content
async for chunk in async_client.stream_large_file_content(
    repo=repository,
    file_path="large_file.json",
    chunk_size=8192
):
    process_chunk(chunk)
```

## Data Models

### BatchRequest

Represents a single request in a batch operation.

```python
@dataclass
class BatchRequest:
    repo: Repository
    file_path: str
    priority: int = 0
    estimated_size: int = 0
    cache_key: Optional[str] = None
```

### BatchResult

Contains the result of a batch request, including content, error information, and performance metrics.

```python
@dataclass
class BatchResult:
    request: BatchRequest
    content: Optional[FileContent] = None
    error: Optional[Exception] = None
    from_cache: bool = False
    processing_time: float = 0.0
```

### BatchMetrics

Performance metrics for batch operations.

```python
@dataclass
class BatchMetrics:
    total_requests: int
    successful_requests: int
    cache_hits: int
    average_batch_size: float
    total_processing_time: float
    api_calls_saved: int
    parallel_efficiency: float
```

### BatchStrategy

Enumeration of available batching strategies.

```python
class BatchStrategy(Enum):
    SEQUENTIAL = "sequential"      # Process requests one by one
    PARALLEL = "parallel"          # Process requests in parallel
    ADAPTIVE = "adaptive"          # Adapt strategy based on conditions
    AGGRESSIVE = "aggressive"      # Maximize parallelism
    CONSERVATIVE = "conservative"  # Minimize resource usage
```

## Configuration

### BatchConfig

Comprehensive configuration for batch processing behavior.

```python
@dataclass
class BatchConfig:
    # Concurrency settings
    max_concurrent_requests: int = 10
    max_concurrent_repos: int = 3
    
    # Batch size settings
    default_batch_size: int = 10
    max_batch_size: int = 50
    min_batch_size: int = 1
    
    # Performance settings
    rate_limit_buffer: float = 0.8
    retry_attempts: int = 3
    retry_delay_base: float = 1.0
    
    # Memory settings
    max_memory_usage_mb: int = 500
    stream_large_files_threshold: int = 1024 * 1024  # 1MB
    
    # Strategy settings
    default_strategy: BatchStrategy = BatchStrategy.ADAPTIVE
    enable_cross_repo_batching: bool = True
    enable_file_prioritization: bool = True
    
    # Monitoring settings
    enable_performance_monitoring: bool = True
    log_batch_metrics: bool = False
```

### Configuration File Format

Batch settings can be configured via YAML or JSON files:

```yaml
# batch_config.yaml
batch:
  concurrency:
    max_concurrent_requests: 15
    max_concurrent_repos: 5
  
  batch_sizes:
    default: 12
    max: 60
    min: 2
  
  performance:
    rate_limit_buffer: 0.85
    retry_attempts: 4
    retry_delay_base: 1.5
  
  memory:
    max_usage_mb: 750
    stream_threshold_bytes: 2097152  # 2MB
  
  strategy:
    default: "adaptive"
    enable_cross_repo_batching: true
    enable_file_prioritization: true
  
  monitoring:
    enable_performance_monitoring: true
    log_batch_metrics: true
```

## Error Handling

### BatchErrorHandler

Sophisticated error handling with recovery strategies.

```python
from github_ioc_scanner.batch_error_handler import BatchErrorHandler

# Initialize error handler
error_handler = BatchErrorHandler()

# Handle batch failures
recovery_plan = error_handler.handle_batch_failure(
    failed_batch=failed_requests,
    error=exception
)

# Handle partial failures
retry_requests = error_handler.handle_partial_failure(
    successful_results=successful_results,
    failed_requests=failed_requests
)
```

### Error Categories

1. **Network Errors**: Temporary connectivity issues
   - Automatic retry with exponential backoff
   - Circuit breaker for persistent failures

2. **Rate Limit Errors**: GitHub API rate limit exceeded
   - Automatic pause and resume
   - Dynamic concurrency adjustment

3. **Authentication Errors**: Invalid or expired tokens
   - Immediate failure with clear error message
   - No retry attempts

4. **Individual File Errors**: File-specific issues
   - Continue processing other files
   - Log detailed error information

5. **Repository Access Errors**: Permission or availability issues
   - Skip repository and continue with others
   - Report inaccessible repositories

## Performance Monitoring

### BatchMetricsCollector

Collects and analyzes batch performance metrics.

```python
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector

# Initialize metrics collector
metrics_collector = BatchMetricsCollector()

# Record batch operation
metrics_collector.record_batch_operation(
    operation_type="file_batch",
    duration=2.5,
    batch_size=15,
    success_count=14,
    cache_hits=8
)

# Get performance summary
summary = metrics_collector.get_performance_summary()
print(f"Average batch size: {summary['avg_batch_size']}")
print(f"Cache hit rate: {summary['cache_hit_rate']:.2%}")
print(f"Success rate: {summary['success_rate']:.2%}")
```

### BatchProgressMonitor

Real-time progress monitoring for batch operations.

```python
from github_ioc_scanner.batch_progress_monitor import BatchProgressMonitor

# Initialize progress monitor
progress_monitor = BatchProgressMonitor()

# Start monitoring
progress_monitor.start_monitoring()

# Update progress
progress_monitor.update_progress(
    completed=50,
    total=200,
    current_batch_size=10,
    eta_seconds=120
)
```

## Memory Management

### ResourceManager

Manages memory usage and resource cleanup during batch operations.

```python
from github_ioc_scanner.resource_manager import ResourceManager

# Initialize resource manager
resource_manager = ResourceManager(
    max_memory_mb=500,
    cleanup_threshold=0.8
)

# Monitor memory usage
if resource_manager.should_reduce_batch_size():
    # Reduce batch size to prevent memory issues
    batch_size = max(1, batch_size // 2)

# Clean up resources
resource_manager.cleanup_batch_resources(batch_results)
```

### StreamingBatchProcessor

Memory-efficient processing for large batches.

```python
from github_ioc_scanner.streaming_batch_processor import StreamingBatchProcessor

# Initialize streaming processor
streaming_processor = StreamingBatchProcessor(
    chunk_size=10,
    max_memory_mb=300
)

# Process large batch with streaming
async for batch_chunk in streaming_processor.process_large_batch_streaming(
    large_batch_requests
):
    # Process each chunk as it becomes available
    process_batch_chunk(batch_chunk)
```

## Best Practices

### 1. Choosing the Right Strategy

- **ADAPTIVE**: Best for most use cases, automatically adjusts based on conditions
- **PARALLEL**: Use when you have high rate limits and good network conditions
- **CONSERVATIVE**: Use when resources are limited or network is unreliable
- **AGGRESSIVE**: Use for time-critical scans with abundant resources

### 2. Optimizing Batch Sizes

- Start with default settings and monitor performance
- Larger batches are better for small files
- Smaller batches are better for large files or limited memory
- Consider rate limits when setting maximum batch size

### 3. Memory Management

- Enable streaming for large files (>1MB)
- Monitor memory usage in long-running scans
- Use resource cleanup for batch operations
- Set appropriate memory limits based on system resources

### 4. Error Handling

- Enable retry logic for network errors
- Set appropriate retry limits to avoid infinite loops
- Monitor error rates and adjust strategies accordingly
- Use detailed logging for troubleshooting

### 5. Performance Monitoring

- Enable performance monitoring for optimization insights
- Log batch metrics for analysis
- Monitor cache hit rates to optimize caching
- Track API usage to stay within rate limits

## Integration Examples

### Basic Batch Scanning

```python
import asyncio
from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy

async def batch_scan_repositories(repositories):
    # Configure batch processing
    config = BatchConfig(
        max_concurrent_requests=15,
        default_batch_size=12,
        default_strategy=BatchStrategy.ADAPTIVE
    )
    
    # Initialize coordinator
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config
    )
    
    try:
        # Process repositories in batches
        results = await coordinator.process_repositories_batch(
            repositories=repositories,
            strategy=BatchStrategy.ADAPTIVE
        )
        
        # Get performance metrics
        metrics = coordinator.get_batch_metrics()
        print(f"Processed {metrics.total_requests} requests")
        print(f"Cache hit rate: {metrics.cache_hits / metrics.total_requests:.2%}")
        
        return results
        
    finally:
        # Clean up resources
        await coordinator.cleanup()

# Run batch scan
results = asyncio.run(batch_scan_repositories(repo_list))
```

### Advanced Configuration

```python
from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector

async def advanced_batch_scan():
    # Advanced configuration
    config = BatchConfig(
        max_concurrent_requests=20,
        max_concurrent_repos=5,
        default_batch_size=15,
        max_batch_size=75,
        rate_limit_buffer=0.9,
        retry_attempts=5,
        max_memory_usage_mb=1000,
        stream_large_files_threshold=2 * 1024 * 1024,  # 2MB
        default_strategy=BatchStrategy.AGGRESSIVE,
        enable_cross_repo_batching=True,
        enable_file_prioritization=True,
        enable_performance_monitoring=True,
        log_batch_metrics=True
    )
    
    # Initialize components
    metrics_collector = BatchMetricsCollector()
    coordinator = BatchCoordinator(
        github_client=github_client,
        cache_manager=cache_manager,
        config=config,
        metrics_collector=metrics_collector
    )
    
    try:
        # Process with priority files
        results = await coordinator.process_files_batch(
            repo=repository,
            file_paths=all_files,
            priority_files=["package.json", "requirements.txt", "Gemfile.lock"]
        )
        
        # Analyze performance
        summary = metrics_collector.get_performance_summary()
        optimizations = metrics_collector.identify_optimization_opportunities()
        
        print("Performance Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        if optimizations:
            print("Optimization Opportunities:")
            for opt in optimizations:
                print(f"  - {opt}")
        
        return results
        
    finally:
        await coordinator.cleanup()
```

## Troubleshooting

### Common Issues

1. **High Memory Usage**
   - Reduce batch size
   - Enable streaming for large files
   - Increase cleanup frequency

2. **Rate Limit Errors**
   - Reduce concurrency
   - Increase rate limit buffer
   - Use conservative strategy

3. **Network Timeouts**
   - Reduce batch size
   - Increase retry attempts
   - Use adaptive strategy

4. **Poor Performance**
   - Enable performance monitoring
   - Analyze batch metrics
   - Adjust strategy based on conditions

### Debugging

Enable detailed logging to troubleshoot issues:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('github_ioc_scanner.batch')

# Enable batch metrics logging
config = BatchConfig(log_batch_metrics=True)
```

## API Reference

For complete API reference documentation, see the individual module documentation:

- `batch_coordinator.py`: Central batch orchestration
- `parallel_batch_processor.py`: Parallel processing implementation
- `batch_strategy_manager.py`: Intelligent batching strategies
- `async_github_client.py`: Async GitHub API client
- `batch_models.py`: Data models and enums
- `batch_error_handler.py`: Error handling and recovery
- `batch_metrics_collector.py`: Performance monitoring
- `resource_manager.py`: Memory and resource management