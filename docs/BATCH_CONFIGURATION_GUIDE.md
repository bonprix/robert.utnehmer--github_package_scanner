# Batch Processing Configuration Guide

## Overview

This guide provides detailed information on configuring the GitHub IOC Scanner's batch processing system for optimal performance across different use cases and environments.

## Configuration Methods

### 1. Programmatic Configuration

Configure batch processing directly in your code:

```python
from github_ioc_scanner.batch_models import BatchConfig, BatchStrategy

# Basic configuration
config = BatchConfig(
    max_concurrent_requests=10,
    default_batch_size=15,
    default_strategy=BatchStrategy.ADAPTIVE
)

# Advanced configuration
config = BatchConfig(
    # Concurrency settings
    max_concurrent_requests=20,
    max_concurrent_repos=5,
    
    # Batch size settings
    default_batch_size=12,
    max_batch_size=60,
    min_batch_size=2,
    
    # Performance settings
    rate_limit_buffer=0.85,
    retry_attempts=4,
    retry_delay_base=1.5,
    
    # Memory settings
    max_memory_usage_mb=750,
    stream_large_files_threshold=2 * 1024 * 1024,  # 2MB
    
    # Strategy settings
    default_strategy=BatchStrategy.ADAPTIVE,
    enable_cross_repo_batching=True,
    enable_file_prioritization=True,
    
    # Monitoring settings
    enable_performance_monitoring=True,
    log_batch_metrics=True
)
```

### 2. Configuration Files

#### YAML Configuration

Create a `batch_config.yaml` file:

```yaml
batch:
  concurrency:
    max_concurrent_requests: 15
    max_concurrent_repos: 3
  
  batch_sizes:
    default: 12
    max: 50
    min: 1
  
  performance:
    rate_limit_buffer: 0.8
    retry_attempts: 3
    retry_delay_base: 1.0
  
  memory:
    max_usage_mb: 500
    stream_threshold_bytes: 1048576  # 1MB
  
  strategy:
    default: "adaptive"
    enable_cross_repo_batching: true
    enable_file_prioritization: true
  
  monitoring:
    enable_performance_monitoring: true
    log_batch_metrics: false
```

#### JSON Configuration

Create a `batch_config.json` file:

```json
{
  "batch": {
    "concurrency": {
      "max_concurrent_requests": 15,
      "max_concurrent_repos": 3
    },
    "batch_sizes": {
      "default": 12,
      "max": 50,
      "min": 1
    },
    "performance": {
      "rate_limit_buffer": 0.8,
      "retry_attempts": 3,
      "retry_delay_base": 1.0
    },
    "memory": {
      "max_usage_mb": 500,
      "stream_threshold_bytes": 1048576
    },
    "strategy": {
      "default": "adaptive",
      "enable_cross_repo_batching": true,
      "enable_file_prioritization": true
    },
    "monitoring": {
      "enable_performance_monitoring": true,
      "log_batch_metrics": false
    }
  }
}
```

### 3. Environment Variables

Configure batch processing using environment variables:

```bash
# Concurrency settings
export GITHUB_IOC_SCANNER_MAX_CONCURRENT_REQUESTS=15
export GITHUB_IOC_SCANNER_MAX_CONCURRENT_REPOS=3

# Batch size settings
export GITHUB_IOC_SCANNER_DEFAULT_BATCH_SIZE=12
export GITHUB_IOC_SCANNER_MAX_BATCH_SIZE=50

# Performance settings
export GITHUB_IOC_SCANNER_RATE_LIMIT_BUFFER=0.8
export GITHUB_IOC_SCANNER_RETRY_ATTEMPTS=3

# Memory settings
export GITHUB_IOC_SCANNER_MAX_MEMORY_MB=500
export GITHUB_IOC_SCANNER_STREAM_THRESHOLD_BYTES=1048576

# Strategy settings
export GITHUB_IOC_SCANNER_BATCH_STRATEGY=adaptive
export GITHUB_IOC_SCANNER_ENABLE_CROSS_REPO_BATCHING=true
export GITHUB_IOC_SCANNER_ENABLE_FILE_PRIORITIZATION=true

# Monitoring settings
export GITHUB_IOC_SCANNER_ENABLE_PERFORMANCE_MONITORING=true
export GITHUB_IOC_SCANNER_LOG_BATCH_METRICS=false
```

## Configuration Parameters

### Concurrency Settings

#### max_concurrent_requests
- **Type**: Integer
- **Default**: 10
- **Range**: 1-50
- **Description**: Maximum number of concurrent API requests
- **Recommendations**:
  - Start with 10 for most use cases
  - Increase to 15-20 for high-performance scenarios
  - Reduce to 5-8 for rate-limited tokens or unstable networks

#### max_concurrent_repos
- **Type**: Integer
- **Default**: 3
- **Range**: 1-10
- **Description**: Maximum number of repositories processed concurrently
- **Recommendations**:
  - Use 3-5 for organization scans
  - Use 1-2 for memory-constrained environments
  - Increase to 5-10 for high-performance batch processing

### Batch Size Settings

#### default_batch_size
- **Type**: Integer
- **Default**: 10
- **Range**: 1-100
- **Description**: Default number of files processed in each batch
- **Recommendations**:
  - Use 10-15 for mixed file sizes
  - Use 20-30 for small files (< 100KB)
  - Use 5-10 for large files (> 1MB)

#### max_batch_size
- **Type**: Integer
- **Default**: 50
- **Range**: 1-200
- **Description**: Maximum allowed batch size
- **Recommendations**:
  - Set to 50-75 for most scenarios
  - Increase to 100+ for small files and high rate limits
  - Reduce to 20-30 for large files or limited memory

#### min_batch_size
- **Type**: Integer
- **Default**: 1
- **Range**: 1-10
- **Description**: Minimum batch size (fallback for optimization)
- **Recommendations**:
  - Keep at 1 for maximum flexibility
  - Set to 2-3 if you want to avoid single-file batches

### Performance Settings

#### rate_limit_buffer
- **Type**: Float
- **Default**: 0.8
- **Range**: 0.1-1.0
- **Description**: Percentage of rate limit to use (0.8 = 80%)
- **Recommendations**:
  - Use 0.8 for balanced performance and safety
  - Increase to 0.9-0.95 for aggressive performance
  - Reduce to 0.6-0.7 for conservative usage

#### retry_attempts
- **Type**: Integer
- **Default**: 3
- **Range**: 0-10
- **Description**: Number of retry attempts for failed requests
- **Recommendations**:
  - Use 3-5 for most scenarios
  - Increase to 5-8 for unreliable networks
  - Reduce to 1-2 for fast-fail scenarios

#### retry_delay_base
- **Type**: Float
- **Default**: 1.0
- **Range**: 0.1-10.0
- **Description**: Base delay in seconds for exponential backoff
- **Recommendations**:
  - Use 1.0-2.0 for most scenarios
  - Increase to 3.0-5.0 for rate-limited environments
  - Reduce to 0.5-1.0 for fast retry scenarios

### Memory Settings

#### max_memory_usage_mb
- **Type**: Integer
- **Default**: 500
- **Range**: 100-5000
- **Description**: Maximum memory usage in megabytes
- **Recommendations**:
  - Use 500-1000MB for typical workstations
  - Increase to 2000-5000MB for high-performance servers
  - Reduce to 100-300MB for resource-constrained environments

#### stream_large_files_threshold
- **Type**: Integer
- **Default**: 1048576 (1MB)
- **Range**: 10240-10485760 (10KB-10MB)
- **Description**: File size threshold for streaming processing
- **Recommendations**:
  - Use 1-2MB for balanced performance
  - Increase to 5-10MB for high-memory environments
  - Reduce to 100-500KB for memory-constrained scenarios

### Strategy Settings

#### default_strategy
- **Type**: BatchStrategy enum
- **Default**: ADAPTIVE
- **Options**: SEQUENTIAL, PARALLEL, ADAPTIVE, AGGRESSIVE, CONSERVATIVE
- **Description**: Default batching strategy
- **Recommendations**:
  - **ADAPTIVE**: Best for most use cases, automatically adjusts
  - **PARALLEL**: Use with high rate limits and stable networks
  - **AGGRESSIVE**: Use for time-critical scans with abundant resources
  - **CONSERVATIVE**: Use with limited resources or unreliable networks
  - **SEQUENTIAL**: Use for debugging or very limited resources

#### enable_cross_repo_batching
- **Type**: Boolean
- **Default**: True
- **Description**: Enable batching across multiple repositories
- **Recommendations**:
  - Enable for organization-wide scans
  - Disable for single-repository focused scans
  - Disable if repositories have very different characteristics

#### enable_file_prioritization
- **Type**: Boolean
- **Default**: True
- **Description**: Enable intelligent file prioritization
- **Recommendations**:
  - Enable for security-focused scans
  - Enable when you need results for critical files first
  - Disable for uniform processing requirements

### Monitoring Settings

#### enable_performance_monitoring
- **Type**: Boolean
- **Default**: True
- **Description**: Enable detailed performance monitoring
- **Recommendations**:
  - Enable for optimization and troubleshooting
  - Disable only if performance overhead is critical
  - Always enable during initial configuration tuning

#### log_batch_metrics
- **Type**: Boolean
- **Default**: False
- **Description**: Log detailed batch metrics to console/logs
- **Recommendations**:
  - Enable for debugging and optimization
  - Disable for production to reduce log volume
  - Enable temporarily when investigating performance issues

## Use Case Configurations

### 1. High-Performance Server

Optimized for maximum throughput with abundant resources:

```yaml
batch:
  concurrency:
    max_concurrent_requests: 25
    max_concurrent_repos: 8
  
  batch_sizes:
    default: 20
    max: 100
    min: 5
  
  performance:
    rate_limit_buffer: 0.95
    retry_attempts: 5
    retry_delay_base: 1.0
  
  memory:
    max_usage_mb: 2000
    stream_threshold_bytes: 5242880  # 5MB
  
  strategy:
    default: "aggressive"
    enable_cross_repo_batching: true
    enable_file_prioritization: true
  
  monitoring:
    enable_performance_monitoring: true
    log_batch_metrics: true
```

### 2. Resource-Constrained Environment

Optimized for minimal resource usage:

```yaml
batch:
  concurrency:
    max_concurrent_requests: 5
    max_concurrent_repos: 2
  
  batch_sizes:
    default: 5
    max: 20
    min: 1
  
  performance:
    rate_limit_buffer: 0.6
    retry_attempts: 2
    retry_delay_base: 2.0
  
  memory:
    max_usage_mb: 200
    stream_threshold_bytes: 524288  # 512KB
  
  strategy:
    default: "conservative"
    enable_cross_repo_batching: false
    enable_file_prioritization: true
  
  monitoring:
    enable_performance_monitoring: true
    log_batch_metrics: false
```

### 3. Rate-Limited Token

Optimized for tokens with low rate limits:

```yaml
batch:
  concurrency:
    max_concurrent_requests: 3
    max_concurrent_repos: 1
  
  batch_sizes:
    default: 8
    max: 25
    min: 1
  
  performance:
    rate_limit_buffer: 0.5
    retry_attempts: 6
    retry_delay_base: 3.0
  
  memory:
    max_usage_mb: 500
    stream_threshold_bytes: 1048576  # 1MB
  
  strategy:
    default: "conservative"
    enable_cross_repo_batching: true
    enable_file_prioritization: true
  
  monitoring:
    enable_performance_monitoring: true
    log_batch_metrics: false
```

### 4. Development/Testing

Optimized for development and testing scenarios:

```yaml
batch:
  concurrency:
    max_concurrent_requests: 8
    max_concurrent_repos: 2
  
  batch_sizes:
    default: 6
    max: 30
    min: 1
  
  performance:
    rate_limit_buffer: 0.7
    retry_attempts: 2
    retry_delay_base: 1.0
  
  memory:
    max_usage_mb: 300
    stream_threshold_bytes: 1048576  # 1MB
  
  strategy:
    default: "adaptive"
    enable_cross_repo_batching: true
    enable_file_prioritization: true
  
  monitoring:
    enable_performance_monitoring: true
    log_batch_metrics: true
```

## Performance Tuning

### 1. Monitoring Performance

Enable performance monitoring to gather baseline metrics:

```python
from github_ioc_scanner.batch_models import BatchConfig
from github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector

# Enable monitoring
config = BatchConfig(
    enable_performance_monitoring=True,
    log_batch_metrics=True
)

# Collect metrics
metrics_collector = BatchMetricsCollector()

# After running scans, analyze performance
summary = metrics_collector.get_performance_summary()
optimizations = metrics_collector.identify_optimization_opportunities()
```

### 2. Iterative Optimization

1. **Start with default settings**
2. **Run representative scans**
3. **Analyze performance metrics**
4. **Adjust one parameter at a time**
5. **Measure impact**
6. **Repeat until optimal**

### 3. Key Performance Indicators

Monitor these metrics for optimization:

- **Throughput**: Files processed per minute
- **Cache Hit Rate**: Percentage of requests served from cache
- **Success Rate**: Percentage of successful requests
- **Parallel Efficiency**: Actual vs theoretical parallel speedup
- **Memory Usage**: Peak memory consumption
- **API Usage**: Rate limit utilization

### 4. Common Optimization Patterns

#### Increase Throughput
1. Increase `max_concurrent_requests`
2. Increase `default_batch_size`
3. Use `AGGRESSIVE` or `PARALLEL` strategy
4. Increase `rate_limit_buffer`

#### Reduce Memory Usage
1. Decrease `max_memory_usage_mb`
2. Decrease `stream_large_files_threshold`
3. Decrease `max_batch_size`
4. Use `CONSERVATIVE` strategy

#### Improve Reliability
1. Increase `retry_attempts`
2. Increase `retry_delay_base`
3. Decrease `rate_limit_buffer`
4. Use `CONSERVATIVE` strategy

#### Balance Performance and Resources
1. Use `ADAPTIVE` strategy
2. Enable performance monitoring
3. Set moderate concurrency levels
4. Use default batch sizes as starting point

## Troubleshooting Configuration Issues

### Common Problems and Solutions

#### 1. High Memory Usage
**Symptoms**: Out of memory errors, system slowdown
**Solutions**:
- Reduce `max_memory_usage_mb`
- Reduce `stream_large_files_threshold`
- Reduce `max_batch_size`
- Enable streaming for large files

#### 2. Rate Limit Errors
**Symptoms**: 403 errors, API rate limit exceeded
**Solutions**:
- Reduce `max_concurrent_requests`
- Reduce `rate_limit_buffer`
- Increase `retry_delay_base`
- Use `CONSERVATIVE` strategy

#### 3. Poor Performance
**Symptoms**: Slow scan times, low throughput
**Solutions**:
- Increase `max_concurrent_requests`
- Increase `default_batch_size`
- Use `AGGRESSIVE` or `PARALLEL` strategy
- Enable cross-repository batching

#### 4. Network Timeouts
**Symptoms**: Connection timeouts, network errors
**Solutions**:
- Reduce `max_concurrent_requests`
- Increase `retry_attempts`
- Increase `retry_delay_base`
- Use `CONSERVATIVE` strategy

### Diagnostic Commands

Enable debug logging for detailed troubleshooting:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('github_ioc_scanner.batch')

# Enable detailed metrics
config = BatchConfig(
    enable_performance_monitoring=True,
    log_batch_metrics=True
)
```

## Best Practices

### 1. Configuration Management
- Use configuration files for production deployments
- Version control your configuration files
- Document configuration changes and their rationale
- Test configuration changes in development first

### 2. Environment-Specific Settings
- Use different configurations for development, staging, and production
- Adjust settings based on available resources
- Consider network conditions and rate limits
- Monitor and adjust based on actual usage patterns

### 3. Security Considerations
- Don't log sensitive information in batch metrics
- Use appropriate rate limiting to avoid API abuse
- Monitor for unusual patterns that might indicate issues
- Implement proper error handling for authentication failures

### 4. Maintenance
- Regularly review and update configurations
- Monitor performance trends over time
- Update configurations when infrastructure changes
- Document configuration decisions for team knowledge

## Migration Guide

### From Basic to Batch Processing

If you're migrating from basic sequential processing to batch processing:

1. **Start Conservative**: Begin with conservative settings
2. **Enable Monitoring**: Turn on performance monitoring
3. **Gradual Increase**: Gradually increase concurrency and batch sizes
4. **Monitor Impact**: Watch for rate limit issues and memory usage
5. **Optimize Iteratively**: Make incremental improvements based on metrics

### Configuration Migration

When updating existing configurations:

1. **Backup Current Settings**: Save working configurations
2. **Test Changes**: Test new settings in development
3. **Monitor Closely**: Watch for issues after deployment
4. **Rollback Plan**: Have a plan to revert if issues occur
5. **Document Changes**: Record what changed and why