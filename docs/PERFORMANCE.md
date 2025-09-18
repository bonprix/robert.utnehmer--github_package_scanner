# Performance Optimization Guide

This guide provides strategies and best practices for optimizing the performance of GitHub IOC Scanner, especially when scanning large organizations or repositories.

## Understanding Performance Factors

### Primary Performance Bottlenecks

1. **GitHub API Rate Limits**: 5,000 requests/hour for authenticated users
2. **Network Latency**: Time to fetch file contents from GitHub
3. **File Parsing**: CPU time to parse package manager files
4. **IOC Matching**: Time to compare packages against IOC definitions
5. **Cache Operations**: Database read/write operations

### Performance Metrics

The tool provides cache statistics after each scan:
```
Cache Statistics:
  Hits: 245, Misses: 23, Time Saved: 45.7s
  API Calls Saved: 245, Cache Hit Rate: 91.4%
```

## Optimization Strategies

### 1. Leverage Caching Effectively

#### Cache Warm-up Strategy
```bash
# First scan builds comprehensive cache (slower)
github-ioc-scan --org myorg

# Subsequent scans are much faster
github-ioc-scan --org myorg  # Near-instant results
```

#### Cache Location and Management
```bash
# Check cache size and location
# Linux/macOS
du -sh ~/.cache/github-ioc-scan/
ls -la ~/.cache/github-ioc-scan/

# Windows
dir %LOCALAPPDATA%\github-ioc-scan\ /s
```

#### Cache Optimization Tips
- **Keep cache intact**: Don't clear cache unless necessary
- **Monitor cache hit rates**: Aim for >90% hit rate on repeated scans
- **Use incremental scanning**: Scan specific repos after initial org scan

### 2. Use Fast Mode for Quick Assessments

Fast mode significantly reduces scan time by only checking root-level files:

```bash
# Fast mode: 10x faster for large repositories
github-ioc-scan --org myorg --fast

# Regular mode: Comprehensive but slower
github-ioc-scan --org myorg
```

**Fast Mode Benefits**:
- Scans only root-level package files
- Skips deep directory traversal
- Reduces API calls by ~80%
- Ideal for initial security assessments

**Fast Mode Limitations**:
- May miss package files in subdirectories
- Less comprehensive coverage
- Not suitable for thorough security audits

### 3. Optimize Scanning Scope

#### Progressive Scanning Strategy
```bash
# 1. Start with fast org-wide scan
github-ioc-scan --org myorg --fast

# 2. Deep scan specific high-risk repositories
github-ioc-scan --org myorg --repo critical-app

# 3. Team-based scanning for focused audits
github-ioc-scan --org myorg --team security-team
```

#### Repository Filtering
```bash
# Exclude archived repositories (default behavior)
github-ioc-scan --org myorg

# Include archived only when necessary
github-ioc-scan --org myorg --include-archived
```

### 4. GitHub API Optimization

#### Authentication Setup
```bash
# Use personal access token for higher rate limits
export GITHUB_TOKEN="your_token_here"

# Verify token has appropriate scopes
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

#### Rate Limit Management
The tool automatically handles rate limits, but you can optimize:

- **Use authenticated requests**: 5,000/hour vs 60/hour for unauthenticated
- **Monitor rate limit status**: Tool displays remaining requests
- **Schedule scans**: Run during off-peak hours for better performance

#### Conditional Requests
The tool uses ETags for efficient API usage:
```bash
# First request fetches data and ETag
# Subsequent requests use If-None-Match header
# 304 Not Modified responses save bandwidth and quota
```

### 5. IOC Definition Optimization

#### Efficient IOC Structure
```python
# Optimized: Use specific versions when possible
IOC_PACKAGES = {
    "malicious-package": ["1.0.0", "1.0.1"],  # Specific versions
}

# Less efficient: Wildcard matching requires more processing
IOC_PACKAGES = {
    "suspicious-package": None,  # Any version
}
```

#### IOC File Organization
```python
# Group related IOCs in separate files for better maintainability
# issues/npm_attacks.py - npm-specific IOCs
# issues/python_attacks.py - Python-specific IOCs
# issues/critical_cves.py - High-priority vulnerabilities
```

### 6. System-Level Optimizations

#### Hardware Considerations
- **SSD Storage**: Faster cache database operations
- **Network Bandwidth**: Reduces file download times
- **CPU**: Faster parsing of large package files
- **RAM**: Better caching of parsed data

#### Operating System Optimizations
```bash
# Linux: Increase file descriptor limits
ulimit -n 4096

# macOS: Similar file descriptor optimization
ulimit -n 4096

# Windows: Ensure adequate virtual memory
```

## Performance Monitoring

### Built-in Metrics
The tool provides detailed performance information:

```bash
github-ioc-scan --org myorg
# Output includes:
# - Scan duration
# - Cache hit/miss statistics
# - API calls made/saved
# - Files processed
# - IOCs found
```

### Custom Performance Monitoring
```bash
# Time the scan
time github-ioc-scan --org myorg

# Monitor API rate limit usage
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

### Cache Performance Analysis
```bash
# Check cache database size
ls -lh ~/.cache/github-ioc-scan/cache.sqlite3

# Analyze cache effectiveness
# High hit rate (>90%) indicates good cache performance
# Low hit rate suggests cache issues or frequent file changes
```

## Scaling Strategies

### Large Organization Scanning

#### Parallel Team Scanning
```bash
# Scan multiple teams in parallel (separate terminals/processes)
github-ioc-scan --org myorg --team team1 &
github-ioc-scan --org myorg --team team2 &
github-ioc-scan --org myorg --team team3 &
wait
```

#### Incremental Scanning
```bash
# Daily incremental scans after initial full scan
# Cache ensures only changed repositories are re-scanned
github-ioc-scan --org myorg  # Fast due to caching
```

#### Repository Prioritization
```bash
# Scan critical repositories first
github-ioc-scan --org myorg --repo production-api
github-ioc-scan --org myorg --repo user-frontend
github-ioc-scan --org myorg --repo payment-service

# Then scan remaining repositories
github-ioc-scan --org myorg --fast
```

### Continuous Integration Integration

#### CI/CD Pipeline Optimization
```yaml
# GitHub Actions example
- name: IOC Scan
  run: |
    # Use cache between CI runs
    github-ioc-scan --org ${{ github.repository_owner }} --repo ${{ github.event.repository.name }}
```

#### Scheduled Scanning
```bash
# Cron job for regular organization scans
# Daily at 2 AM (low GitHub API usage time)
0 2 * * * /usr/local/bin/github-ioc-scan --org myorg --fast
```

## Troubleshooting Performance Issues

### Slow Initial Scans

**Symptoms**: First scan takes very long
**Causes**: 
- Large number of repositories
- Many package files per repository
- Network latency

**Solutions**:
```bash
# Use fast mode for initial assessment
github-ioc-scan --org myorg --fast

# Scan specific teams first
github-ioc-scan --org myorg --team critical-team

# Check network connectivity
curl -w "@curl-format.txt" -o /dev/null -s https://api.github.com/
```

### Poor Cache Performance

**Symptoms**: Low cache hit rates on repeated scans
**Causes**:
- Frequently changing files
- Cache corruption
- Insufficient disk space

**Solutions**:
```bash
# Check cache integrity
sqlite3 ~/.cache/github-ioc-scan/cache.sqlite3 "PRAGMA integrity_check;"

# Clear and rebuild cache if corrupted
rm -rf ~/.cache/github-ioc-scan/
github-ioc-scan --org myorg  # Rebuilds cache

# Check disk space
df -h ~/.cache/
```

### Rate Limit Issues

**Symptoms**: Frequent rate limit warnings
**Causes**:
- Unauthenticated requests
- Concurrent tool usage
- Large organization scans

**Solutions**:
```bash
# Verify authentication
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check current rate limit status
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit

# Use fast mode to reduce API calls
github-ioc-scan --org myorg --fast
```

### Memory Usage Issues

**Symptoms**: High memory consumption
**Causes**:
- Large package files
- Many concurrent operations
- Memory leaks

**Solutions**:
```bash
# Monitor memory usage
top -p $(pgrep -f github-ioc-scan)

# Process repositories in smaller batches
github-ioc-scan --org myorg --team small-team

# Restart tool periodically for long-running operations
```

## Performance Benchmarks

### Typical Performance Characteristics

| Scenario | Initial Scan | Cached Scan | API Calls | Time Saved |
|----------|--------------|-------------|-----------|------------|
| Small Org (10 repos) | 30s | 2s | 95% reduction | 93% |
| Medium Org (100 repos) | 5min | 15s | 92% reduction | 95% |
| Large Org (1000 repos) | 45min | 2min | 89% reduction | 96% |

### Fast Mode Performance

| Repository Size | Regular Mode | Fast Mode | Speedup |
|----------------|--------------|-----------|---------|
| Small (<50 files) | 10s | 3s | 3.3x |
| Medium (50-200 files) | 45s | 8s | 5.6x |
| Large (>200 files) | 180s | 15s | 12x |

## Best Practices Summary

### For Regular Use
1. **Always use authentication** for higher rate limits
2. **Let cache warm up** on first scan
3. **Use fast mode** for quick assessments
4. **Scan incrementally** rather than full org scans
5. **Monitor cache hit rates** for performance insights

### For Large Organizations
1. **Start with team-based scanning** to identify high-risk areas
2. **Use progressive scanning strategy** (fast → targeted → comprehensive)
3. **Schedule regular scans** during off-peak hours
4. **Maintain cache integrity** for optimal performance
5. **Consider parallel scanning** for independent teams

### For CI/CD Integration
1. **Cache between runs** when possible
2. **Scan only changed repositories** in CI
3. **Use fast mode** for PR checks
4. **Full scans** for scheduled security audits
5. **Monitor API quota usage** in automated systems

### For Development
1. **Test with small repositories** first
2. **Profile performance** with different IOC sets
3. **Monitor cache behavior** during development
4. **Use appropriate logging levels** for debugging
5. **Benchmark changes** against baseline performance