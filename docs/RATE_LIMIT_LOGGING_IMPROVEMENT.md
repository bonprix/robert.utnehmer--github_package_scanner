# Rate Limit Logging Improvement

## Problem

Bisher wurden Rate Limit Informationen bei jeder API-Anfrage geloggt, auch wenn das Rate Limit noch hoch war. Das führte zu unnötigem Rauschen in den Logs während normaler Operationen.

## Solution

Die `log_rate_limit` Funktion wurde angepasst, um Rate Limit Informationen nur dann zu loggen, wenn sie tatsächlich relevant sind.

## Implementation

### Modified Function (`src/github_ioc_scanner/logging_config.py`)

```python
def log_rate_limit(logger: logging.Logger, remaining: int, reset_time: int) -> None:
    """
    Log GitHub API rate limit information only when relevant (low or exhausted).
    
    Args:
        logger: Logger instance to use
        remaining: Number of requests remaining
        reset_time: Unix timestamp when rate limit resets
    """
    from datetime import datetime
    
    # Only log rate limit info when it's getting low or critical
    if remaining <= 0:
        # Rate limit exhausted - critical warning
        reset_datetime = datetime.fromtimestamp(reset_time)
        logger.warning(f"⚠️  Rate limit exhausted! Resets at {reset_datetime}")
    elif remaining <= 100:
        # Rate limit getting low - warning
        reset_datetime = datetime.fromtimestamp(reset_time)
        logger.warning(f"⚠️  Rate limit low: {remaining} requests remaining, resets at {reset_datetime}")
    elif remaining <= 500:
        # Rate limit moderately low - info only in verbose mode
        reset_datetime = datetime.fromtimestamp(reset_time)
        logger.info(f"Rate limit: {remaining} requests remaining, resets at {reset_datetime}")
    # For remaining > 500, don't log anything (normal operation)
```

## Logging Behavior

### ✅ New Behavior (Smart Logging)

| Rate Limit Remaining | Log Level | Visibility | Message |
|---------------------|-----------|------------|---------|
| > 500 | None | Silent | No logging (normal operation) |
| 100-500 | INFO | Verbose only | `Rate limit: X requests remaining, resets at Y` |
| 1-100 | WARNING | Always visible | `⚠️ Rate limit low: X requests remaining, resets at Y` |
| 0 | WARNING | Always visible | `⚠️ Rate limit exhausted! Resets at Y` |

### ❌ Old Behavior (Noisy Logging)

- **Every API call**: `Rate limit: X requests remaining, resets at Y`
- **Result**: Log spam during normal operations with high rate limits

## Benefits

### 🔇 Reduced Log Noise
- No more rate limit spam during normal operations
- Logs are cleaner and more focused on actual issues

### ⚠️ Important Warnings Still Visible
- Critical rate limit situations are still prominently displayed
- Users get warned when they need to slow down

### 📊 Verbose Mode Support
- Moderately low rate limits (100-500) still logged in verbose mode
- Debugging information available when needed

### 🎯 Better User Experience
- Users only see rate limit info when it matters
- Less distraction during normal scanning operations

## Testing

### Test Results
```bash
python test_rate_limit_logging.py
```

**Output demonstrates:**
- ✅ High limits (2000, 1000): Silent operation
- ✅ Moderate limits (400-500): INFO level only
- ✅ Low limits (5-100): WARNING level with emoji
- ✅ Exhausted (0): CRITICAL WARNING with emoji

### Integration Points

The `log_rate_limit` function is called from:
- `src/github_ioc_scanner/github_client.py` (sync client)
- `src/github_ioc_scanner/async_github_client.py` (async client)

Both clients automatically benefit from the improved logging behavior.

## Backward Compatibility

- ✅ No breaking changes to API
- ✅ Existing code continues to work unchanged
- ✅ Only logging behavior is modified
- ✅ All rate limit functionality preserved

## Usage Examples

### Normal Operation (Silent)
```bash
# High rate limit - no rate limit logs shown
github-ioc-scan --org myorg
# Output: Only scan progress and results, no rate limit noise
```

### Verbose Mode (Detailed)
```bash
# Shows moderate rate limit info when verbose
github-ioc-scan --org myorg --verbose
# Output: Includes rate limit info when it gets moderately low (100-500)
```

### Low Rate Limit (Automatic Warning)
```bash
# Automatically warns when rate limit gets low
github-ioc-scan --org myorg
# Output: ⚠️ Rate limit low: 50 requests remaining, resets at 2025-09-18 10:30:00
```

## Configuration

No configuration needed - the behavior is automatically applied based on rate limit thresholds:

- **Silent threshold**: > 500 remaining
- **Info threshold**: 100-500 remaining  
- **Warning threshold**: < 100 remaining
- **Critical threshold**: 0 remaining

## Future Enhancements

1. **Configurable Thresholds**: Allow users to customize warning thresholds
2. **Rate Limit Prediction**: Predict when rate limit will be exhausted
3. **Multiple Token Support**: Automatic switching between tokens when limits are low
4. **Rate Limit Dashboard**: Real-time rate limit monitoring interface

## Conclusion

Rate limit logging ist jetzt viel benutzerfreundlicher:
- **Stille Operation** bei normalen Rate Limits
- **Automatische Warnungen** bei kritischen Situationen  
- **Verbose Details** bei Bedarf verfügbar
- **Keine Breaking Changes** für bestehenden Code

Das Ergebnis: Saubere Logs während normaler Operationen, aber wichtige Warnungen werden weiterhin angezeigt! 🎉