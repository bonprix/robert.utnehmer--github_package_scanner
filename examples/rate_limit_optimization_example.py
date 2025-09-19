#!/usr/bin/env python3
"""
Rate Limit Optimization Example

This example demonstrates the improved rate limiting features and shows
how to optimize scanning for large organizations.
"""

import asyncio
import os
import sys
import time
from datetime import datetime

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.improved_rate_limiting import get_rate_limiter
from github_ioc_scanner.batch_models import BatchConfig
from github_ioc_scanner.logging_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def demonstrate_rate_limit_monitoring():
    """Demonstrate rate limit monitoring and adaptive delays."""
    print("🔍 Rate Limit Monitoring Demonstration")
    print("=" * 45)
    
    try:
        # Initialize GitHub client
        github_client = GitHubClient()
        
        # Get current rate limit status
        response = github_client._make_request("GET", "/rate_limit")
        
        if response.data:
            rate_limit_info = response.data
            core_limits = rate_limit_info.get('resources', {}).get('core', {})
            search_limits = rate_limit_info.get('resources', {}).get('search', {})
            
            print("Current Rate Limit Status:")
            print(f"  Core API:")
            print(f"    Limit: {core_limits.get('limit', 'Unknown')}")
            print(f"    Remaining: {core_limits.get('remaining', 'Unknown')}")
            print(f"    Reset: {datetime.fromtimestamp(core_limits.get('reset', 0))}")
            
            print(f"  Search API:")
            print(f"    Limit: {search_limits.get('limit', 'Unknown')}")
            print(f"    Remaining: {search_limits.get('remaining', 'Unknown')}")
            print(f"    Reset: {datetime.fromtimestamp(search_limits.get('reset', 0))}")
            
            # Demonstrate rate limiter recommendations
            rate_limiter = get_rate_limiter()
            core_remaining = core_limits.get('remaining', 0)
            core_reset = core_limits.get('reset', 0)
            
            recommended_delay = rate_limiter.get_recommended_delay(core_remaining, core_reset)
            print(f"\nRecommended delay for next request: {recommended_delay:.2f}s")
            
        else:
            print("❌ Could not fetch rate limit information")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def demonstrate_optimized_batch_config():
    """Demonstrate optimized batch configuration for rate limiting."""
    print("\n⚙️  Optimized Batch Configuration")
    print("=" * 35)
    
    # Conservative configuration for rate limit sensitive scanning
    conservative_config = BatchConfig(
        max_concurrent_requests=3,
        max_concurrent_repos=1,
        default_batch_size=5,
        rate_limit_buffer=0.5,  # Use only 50% of rate limit
        retry_delay_base=3.0,
        enable_proactive_rate_limiting=True,
        rate_limit_safety_margin=200,
        adaptive_delay_enabled=True
    )
    
    # Balanced configuration for normal scanning
    balanced_config = BatchConfig(
        max_concurrent_requests=5,
        max_concurrent_repos=2,
        default_batch_size=10,
        rate_limit_buffer=0.6,  # Use 60% of rate limit
        retry_delay_base=2.0,
        enable_proactive_rate_limiting=True,
        rate_limit_safety_margin=100,
        adaptive_delay_enabled=True
    )
    
    # Aggressive configuration for small scans
    aggressive_config = BatchConfig(
        max_concurrent_requests=8,
        max_concurrent_repos=3,
        default_batch_size=15,
        rate_limit_buffer=0.8,  # Use 80% of rate limit
        retry_delay_base=1.0,
        enable_proactive_rate_limiting=True,
        rate_limit_safety_margin=50,
        adaptive_delay_enabled=True
    )
    
    configs = [
        ("Conservative (Large Orgs)", conservative_config),
        ("Balanced (Medium Orgs)", balanced_config),
        ("Aggressive (Small Orgs)", aggressive_config)
    ]
    
    for name, config in configs:
        print(f"\n{name}:")
        print(f"  Max Concurrent Requests: {config.max_concurrent_requests}")
        print(f"  Max Concurrent Repos: {config.max_concurrent_repos}")
        print(f"  Batch Size: {config.default_batch_size}")
        print(f"  Rate Limit Buffer: {config.rate_limit_buffer * 100:.0f}%")
        print(f"  Safety Margin: {config.rate_limit_safety_margin} requests")
        print(f"  Base Retry Delay: {config.retry_delay_base}s")


def demonstrate_rate_limit_strategies():
    """Demonstrate different rate limiting strategies."""
    print("\n🚦 Rate Limiting Strategies")
    print("=" * 30)
    
    strategies = [
        {
            "name": "Reactive Only",
            "description": "Wait only when rate limit is exceeded",
            "pros": ["Fast when limits available", "Simple implementation"],
            "cons": ["Frequent rate limit hits", "Unpredictable delays"],
            "use_case": "Small, infrequent scans"
        },
        {
            "name": "Proactive",
            "description": "Slow down as rate limit approaches",
            "pros": ["Prevents rate limit hits", "Smoother operation"],
            "cons": ["Slightly slower overall", "More complex"],
            "use_case": "Regular, automated scans"
        },
        {
            "name": "Adaptive",
            "description": "Learn from rate limit patterns and adjust",
            "pros": ["Optimal performance", "Self-tuning"],
            "cons": ["Complex implementation", "Learning period"],
            "use_case": "Large-scale, continuous scanning"
        }
    ]
    
    for strategy in strategies:
        print(f"\n{strategy['name']} Strategy:")
        print(f"  Description: {strategy['description']}")
        print(f"  Pros: {', '.join(strategy['pros'])}")
        print(f"  Cons: {', '.join(strategy['cons'])}")
        print(f"  Best for: {strategy['use_case']}")


def demonstrate_cli_optimizations():
    """Demonstrate CLI optimizations for rate limiting."""
    print("\n💡 CLI Optimization Tips")
    print("=" * 25)
    
    tips = [
        {
            "scenario": "Large Organization (1000+ repos)",
            "command": "github-ioc-scan --org large-org --batch-strategy conservative --max-concurrent 3",
            "explanation": "Use conservative settings to avoid rate limits"
        },
        {
            "scenario": "Medium Organization (100-1000 repos)",
            "command": "github-ioc-scan --org medium-org --batch-strategy adaptive --max-concurrent 5",
            "explanation": "Balanced approach with adaptive rate limiting"
        },
        {
            "scenario": "Small Organization (<100 repos)",
            "command": "github-ioc-scan --org small-org --batch-strategy aggressive --max-concurrent 8",
            "explanation": "Faster scanning with higher concurrency"
        },
        {
            "scenario": "Rate Limit Issues",
            "command": "github-ioc-scan --org any-org --batch-size 5 --max-concurrent 2 --enable-cross-repo-batching",
            "explanation": "Minimal concurrency with intelligent batching"
        },
        {
            "scenario": "Fast Mode for Quick Check",
            "command": "github-ioc-scan --org any-org --fast --sbom-only",
            "explanation": "Scan only root-level SBOM files for quick assessment"
        }
    ]
    
    for tip in tips:
        print(f"\n{tip['scenario']}:")
        print(f"  Command: {tip['command']}")
        print(f"  Why: {tip['explanation']}")


def demonstrate_monitoring_and_alerts():
    """Demonstrate rate limit monitoring and alerting."""
    print("\n📊 Rate Limit Monitoring")
    print("=" * 25)
    
    print("The improved rate limiter provides several monitoring features:")
    print()
    print("1. Real-time Rate Limit Status:")
    print("   🚨 Critical (≤3 remaining): Long delays, urgent warnings")
    print("   🐌 Very Low (≤10 remaining): Significant delays")
    print("   ⏳ Low (≤25 remaining): Moderate delays")
    print("   ⚠️  Moderate (≤50 remaining): Small delays")
    print("   ✅ Good (>50 remaining): Minimal delays")
    print()
    print("2. Adaptive Learning:")
    print("   - Tracks consecutive low-limit periods")
    print("   - Adjusts delays based on patterns")
    print("   - Gradually recovers when limits improve")
    print()
    print("3. Logging Levels:")
    print("   - ERROR: Rate limit exceeded")
    print("   - WARNING: Critical rate limit status")
    print("   - INFO: Very low rate limits")
    print("   - DEBUG: Low/moderate rate limits")


def main():
    """Main demonstration function."""
    print("🛡️  GitHub IOC Scanner - Rate Limit Optimization")
    print("=" * 55)
    print("This example demonstrates improved rate limiting features")
    print("and optimization strategies for large-scale scanning.")
    print()
    
    try:
        demonstrate_rate_limit_monitoring()
        demonstrate_optimized_batch_config()
        demonstrate_rate_limit_strategies()
        demonstrate_cli_optimizations()
        demonstrate_monitoring_and_alerts()
        
        print("\n" + "=" * 55)
        print("✅ Rate Limit Optimization Demonstration Complete!")
        print()
        print("Key Improvements:")
        print("  • Proactive rate limiting prevents API exhaustion")
        print("  • Adaptive delays learn from usage patterns")
        print("  • Conservative batch configurations for large orgs")
        print("  • Enhanced monitoring and logging")
        print("  • Separate handling for Code Search API limits")
        
        print("\nRecommended Settings for Your Scan:")
        print("  # For large organizations (like yours with 6000+ repos)")
        print("  github-ioc-scan --org your-org \\")
        print("    --batch-strategy conservative \\")
        print("    --max-concurrent 2 \\")
        print("    --batch-size 5 \\")
        print("    --enable-cross-repo-batching")
        
    except Exception as e:
        logger.error(f"Demonstration failed: {e}")
        raise


if __name__ == "__main__":
    main()