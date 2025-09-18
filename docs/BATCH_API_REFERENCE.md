# Batch API Reference

## Module: batch_coordinator

### Class: BatchCoordinator

Central orchestrator for all batch operations.

#### Constructor

```python
BatchCoordinator(
    github_client: GitHubClient,
    cache_manager: CacheManager,
    config: BatchConfig,
    metrics_collector: Optional[BatchMetricsCollector] = None
)
```

**Parameters:**
- `github_client`: GitHub API client instance
- `cache_manager`: Cache manager for storing results
- `config`: Batch processing configuration
- `metrics_collector`: Optional metrics collector for performance monitoring

#### Methods

##### process_repositories_batch

```python
async def process_repositories_batch(
    self,
    repositories: List[Repository],
    strategy: BatchStrategy = BatchStrategy.ADAPTIVE
) -> Dict[str, List[IOCMatch]]
```

Process multiple repositories with optimal batching.

**Parameters:**
- `repositories`: List of repositories to process
- `strategy`: Batching strategy to use

**Returns:**
- Dictionary mapping repository names to IOC matches

**Raises:**
- `BatchProcessingError`: If batch processing fails
- `RateLimitError`: If rate limits are exceeded

##### process_files_batch

```python
async def process_files_batch(
    self,
    repo: Repository,
    file_paths: List[str],
    priority_files: Optional[List[str]] = None
) -> Dict[str, FileContent]
```

Process multiple files with intelligent batching.

**Parameters:**
- `repo`: Repository containing the files
- `file_paths`: List of file paths to process
- `priority_files`: Optional list of high-priority files

**Returns:**
- Dictionary mapping file paths to file contents

**Raises:**
- `BatchProcessingError`: If batch processing fails
- `FileNotFoundError`: If files cannot be found

##### get_batch_metrics

```python
def get_batch_metrics(self) -> BatchMetrics
```

Get detailed performance metrics for batch operations.

**Returns:**
- BatchMetrics object with performance data

##### cleanup

```python
async def cleanup(self) -> None
```

Clean up resources after batch operations.

---

## Module: parallel_batch_processor

### Class: ParallelBatchProcessor

Handles parallel processing of batch requests with rate limiting.

#### Constructor

```python
ParallelBatchProcessor(
    max_concurrent: int = 10,
    rate_limit_buffer: float = 0.8,
    retry_attempts: int = 3
)
```

**Parameters:**
- `max_concurrent`: Maximum number of concurrent requests
- `rate_limit_buffer`: Percentage of rate limit to use
- `retry_attempts`: Number of retry attempts for failed requests

#### Methods

##### process_batch_parallel

```python
async def process_batch_parallel(
    self,
    requests: List[BatchRequest]
) -> List[BatchResult]
```

Process batch requests in parallel with rate limiting.

**Parameters:**
- `requests`: List of batch requests to process

**Returns:**
- List of batch results

**Raises:**
- `RateLimitError`: If rate limits are exceeded
- `NetworkError`: If network issues occur

##### adjust_concurrency

```python
def adjust_concurrency(self, rate_limit_remaining: int) -> None
```

Dynamically adjust concurrency based on rate limits.

**Parameters:**
- `rate_limit_remaining`: Number of remaining API requests

---

## Module: batch_strategy_manager

### Class: BatchStrategyManager

Manages intelligent batching strategies and optimizations.

#### Constructor

```python
BatchStrategyManager()
```

#### Methods

##### calculate_optimal_batch_size

```python
def calculate_optimal_batch_size(
    self,
    files: List[FileInfo],
    rate_limit_remaining: int,
    network_conditions: NetworkConditions
) -> int
```

Calculate optimal batch size based on multiple factors.

**Parameters:**
- `files`: List of file information objects
- `rate_limit_remaining`: Remaining API rate limit
- `network_conditions`: Current network conditions

**Returns:**
- Optimal batch size as integer

##### prioritize_files

```python
def prioritize_files(
    self,
    files: List[str]
) -> List[PrioritizedFile]
```

Prioritize files based on security importance.

**Parameters:**
- `files`: List of file paths

**Returns:**
- List of prioritized files with scores

##### identify_cross_repo_opportunities

```python
def identify_cross_repo_opportunities(
    self,
    repositories: List[Repository]
) -> List[CrossRepoBatch]
```

Identify opportunities for cross-repository batching.

**Parameters:**
- `repositories`: List of repositories to analyze

**Returns:**
- List of cross-repository batch opportunities

##### adapt_strategy

```python
def adapt_strategy(
    self,
    performance_metrics: BatchMetrics
) -> BatchStrategy
```

Adapt batching strategy based on performance data.

**Parameters:**
- `performance_metrics`: Current performance metrics

**Returns:**
- Recommended batch strategy

---

## Module: async_github_client

### Class: AsyncGitHubClient

Extended GitHub client with advanced batch capabilities.

#### Constructor

```python
AsyncGitHubClient(
    token: str,
    base_url: str = "https://api.github.com",
    timeout: int = 30
)
```

**Parameters:**
- `token`: GitHub API token
- `base_url`: GitHub API base URL
- `timeout`: Request timeout in seconds

#### Methods

##### get_multiple_file_contents_parallel

```python
async def get_multiple_file_contents_parallel(
    self,
    repo: Repository,
    file_paths: List[str],
    max_concurrent: int = 5
) -> Dict[str, FileContent]
```

Get multiple file contents with parallel processing.

**Parameters:**
- `repo`: Repository object
- `file_paths`: List of file paths to retrieve
- `max_concurrent`: Maximum concurrent requests

**Returns:**
- Dictionary mapping file paths to contents

**Raises:**
- `GitHubAPIError`: If API requests fail
- `RateLimitError`: If rate limits are exceeded

##### get_cross_repo_file_contents

```python
async def get_cross_repo_file_contents(
    self,
    repo_files: Dict[Repository, List[str]]
) -> Dict[str, Dict[str, FileContent]]
```

Get file contents across multiple repositories.

**Parameters:**
- `repo_files`: Dictionary mapping repositories to file lists

**Returns:**
- Nested dictionary with repository and file contents

##### stream_large_file_content

```python
async def stream_large_file_content(
    self,
    repo: Repository,
    file_path: str,
    chunk_size: int = 8192
) -> AsyncIterator[str]
```

Stream large file content to avoid memory issues.

**Parameters:**
- `repo`: Repository object
- `file_path`: Path to the file
- `chunk_size`: Size of each chunk in bytes

**Yields:**
- String chunks of file content

---

## Module: batch_models

### Class: BatchRequest

Represents a single request in a batch operation.

#### Attributes

```python
@dataclass
class BatchRequest:
    repo: Repository
    file_path: str
    priority: int = 0
    estimated_size: int = 0
    cache_key: Optional[str] = None
```

**Attributes:**
- `repo`: Repository object
- `file_path`: Path to the file
- `priority`: Priority score (higher = more important)
- `estimated_size`: Estimated file size in bytes
- `cache_key`: Optional cache key for the request

### Class: BatchResult

Contains the result of a batch request.

#### Attributes

```python
@dataclass
class BatchResult:
    request: BatchRequest
    content: Optional[FileContent] = None
    error: Optional[Exception] = None
    from_cache: bool = False
    processing_time: float = 0.0
```

**Attributes:**
- `request`: Original batch request
- `content`: File content if successful
- `error`: Exception if request failed
- `from_cache`: Whether result came from cache
- `processing_time`: Time taken to process request

### Class: BatchMetrics

Performance metrics for batch operations.

#### Attributes

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

**Attributes:**
- `total_requests`: Total number of requests processed
- `successful_requests`: Number of successful requests
- `cache_hits`: Number of cache hits
- `average_batch_size`: Average size of batches
- `total_processing_time`: Total time spent processing
- `api_calls_saved`: Number of API calls saved through optimization
- `parallel_efficiency`: Efficiency of parallel processing (0.0-1.0)

### Class: BatchConfig

Comprehensive configuration for batch processing.

#### Attributes

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
    stream_large_files_threshold: int = 1024 * 1024
    
    # Strategy settings
    default_strategy: BatchStrategy = BatchStrategy.ADAPTIVE
    enable_cross_repo_batching: bool = True
    enable_file_prioritization: bool = True
    
    # Monitoring settings
    enable_performance_monitoring: bool = True
    log_batch_metrics: bool = False
```

### Enum: BatchStrategy

Available batching strategies.

```python
class BatchStrategy(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"
```

**Values:**
- `SEQUENTIAL`: Process requests one by one
- `PARALLEL`: Process requests in parallel
- `ADAPTIVE`: Adapt strategy based on conditions
- `AGGRESSIVE`: Maximize parallelism and throughput
- `CONSERVATIVE`: Minimize resource usage and risk

---

## Module: batch_error_handler

### Class: BatchErrorHandler

Sophisticated error handling with recovery strategies.

#### Constructor

```python
BatchErrorHandler()
```

#### Methods

##### handle_batch_failure

```python
def handle_batch_failure(
    self,
    failed_batch: List[BatchRequest],
    error: Exception
) -> BatchRecoveryPlan
```

Create recovery plan for failed batch.

**Parameters:**
- `failed_batch`: List of requests that failed
- `error`: Exception that caused the failure

**Returns:**
- Recovery plan with retry strategy

##### handle_partial_failure

```python
def handle_partial_failure(
    self,
    successful_results: List[BatchResult],
    failed_requests: List[BatchRequest]
) -> List[BatchRequest]
```

Handle partial batch failures.

**Parameters:**
- `successful_results`: Results that succeeded
- `failed_requests`: Requests that failed

**Returns:**
- List of requests to retry

##### should_retry_request

```python
def should_retry_request(
    self,
    request: BatchRequest,
    error: Exception,
    attempt: int
) -> bool
```

Determine if a request should be retried.

**Parameters:**
- `request`: The batch request
- `error`: Exception that occurred
- `attempt`: Current attempt number

**Returns:**
- True if request should be retried

---

## Module: batch_metrics_collector

### Class: BatchMetricsCollector

Collects and analyzes batch performance metrics.

#### Constructor

```python
BatchMetricsCollector()
```

#### Methods

##### record_batch_operation

```python
def record_batch_operation(
    self,
    operation_type: str,
    duration: float,
    batch_size: int,
    success_count: int,
    cache_hits: int
) -> None
```

Record metrics for a batch operation.

**Parameters:**
- `operation_type`: Type of operation (e.g., "file_batch")
- `duration`: Time taken in seconds
- `batch_size`: Size of the batch
- `success_count`: Number of successful requests
- `cache_hits`: Number of cache hits

##### get_performance_summary

```python
def get_performance_summary(self) -> Dict[str, Any]
```

Get summary of batch performance.

**Returns:**
- Dictionary with performance summary statistics

##### identify_optimization_opportunities

```python
def identify_optimization_opportunities(self) -> List[str]
```

Identify areas for further optimization.

**Returns:**
- List of optimization recommendations

---

## Module: resource_manager

### Class: ResourceManager

Manages memory usage and resource cleanup.

#### Constructor

```python
ResourceManager(
    max_memory_mb: int = 500,
    cleanup_threshold: float = 0.8
)
```

**Parameters:**
- `max_memory_mb`: Maximum memory usage in MB
- `cleanup_threshold`: Memory threshold for cleanup (0.0-1.0)

#### Methods

##### should_reduce_batch_size

```python
def should_reduce_batch_size(self) -> bool
```

Determine if batch size should be reduced due to memory pressure.

**Returns:**
- True if batch size should be reduced

##### cleanup_batch_resources

```python
def cleanup_batch_resources(self, batch_results: List[BatchResult]) -> None
```

Clean up resources from batch results.

**Parameters:**
- `batch_results`: List of batch results to clean up

##### get_memory_usage

```python
def get_memory_usage(self) -> float
```

Get current memory usage in MB.

**Returns:**
- Current memory usage in megabytes

---

## Module: streaming_batch_processor

### Class: StreamingBatchProcessor

Memory-efficient processing for large batches.

#### Constructor

```python
StreamingBatchProcessor(
    chunk_size: int = 10,
    max_memory_mb: int = 300
)
```

**Parameters:**
- `chunk_size`: Size of each processing chunk
- `max_memory_mb`: Maximum memory usage in MB

#### Methods

##### process_large_batch_streaming

```python
async def process_large_batch_streaming(
    self,
    requests: List[BatchRequest]
) -> AsyncIterator[List[BatchResult]]
```

Process large batches with streaming to minimize memory usage.

**Parameters:**
- `requests`: List of batch requests to process

**Yields:**
- Lists of batch results as they become available

---

## Exceptions

### BatchProcessingError

Base exception for batch processing errors.

```python
class BatchProcessingError(Exception):
    """Base exception for batch processing errors."""
    pass
```

### RateLimitError

Exception raised when rate limits are exceeded.

```python
class RateLimitError(BatchProcessingError):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message: str, reset_time: int):
        super().__init__(message)
        self.reset_time = reset_time
```

### NetworkError

Exception raised for network-related errors.

```python
class NetworkError(BatchProcessingError):
    """Exception raised for network-related errors."""
    pass
```

### GitHubAPIError

Exception raised for GitHub API errors.

```python
class GitHubAPIError(BatchProcessingError):
    """Exception raised for GitHub API errors."""
    
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code
```

---

## Type Definitions

### Repository

```python
@dataclass
class Repository:
    name: str
    full_name: str
    owner: str
    default_branch: str = "main"
    private: bool = False
```

### FileContent

```python
@dataclass
class FileContent:
    path: str
    content: str
    size: int
    sha: str
    encoding: str = "utf-8"
```

### FileInfo

```python
@dataclass
class FileInfo:
    path: str
    size: int
    type: str
    sha: str
```

### NetworkConditions

```python
@dataclass
class NetworkConditions:
    latency_ms: float
    bandwidth_mbps: float
    error_rate: float
```

### PrioritizedFile

```python
@dataclass
class PrioritizedFile:
    path: str
    priority: int
    file_type: str
    estimated_size: int
    security_importance: float
```

### CrossRepoBatch

```python
@dataclass
class CrossRepoBatch:
    repositories: List[Repository]
    common_files: List[str]
    estimated_savings: float
```

### IOCMatch

```python
@dataclass
class IOCMatch:
    package_name: str
    version: str
    file_path: str
    line_number: int
    ioc_source: str
```

---

## Usage Examples

### Basic Usage

```python
import asyncio
from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy

async def main():
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
        # Process repositories
        results = await coordinator.process_repositories_batch(
            repositories=repo_list
        )
        
        # Get metrics
        metrics = coordinator.get_batch_metrics()
        print(f"Processed {metrics.total_requests} requests")
        
    finally:
        await coordinator.cleanup()

asyncio.run(main())
```

### Advanced Usage with Custom Configuration

```python
import asyncio
from github_ioc_scanner.batch_coordinator import BatchCoordinator
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector

async def advanced_batch_processing():
    # Advanced configuration
    config = BatchConfig(
        max_concurrent_requests=20,
        max_concurrent_repos=5,
        default_batch_size=15,
        rate_limit_buffer=0.9,
        retry_attempts=5,
        max_memory_usage_mb=1000,
        default_strategy=BatchStrategy.AGGRESSIVE,
        enable_cross_repo_batching=True,
        enable_file_prioritization=True,
        enable_performance_monitoring=True
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
            priority_files=["package.json", "requirements.txt"]
        )
        
        # Analyze performance
        summary = metrics_collector.get_performance_summary()
        optimizations = metrics_collector.identify_optimization_opportunities()
        
        return results, summary, optimizations
        
    finally:
        await coordinator.cleanup()

# Run advanced processing
results, summary, optimizations = asyncio.run(advanced_batch_processing())
```