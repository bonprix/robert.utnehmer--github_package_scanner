#!/usr/bin/env python3
"""
Example demonstrating the batch performance monitoring and analysis system.

This example shows how to use the BatchMetricsCollector, BatchProgressMonitor,
and BatchPerformanceAnalyzer together to monitor and optimize batch operations.
"""

import asyncio
import time
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector
from src.github_ioc_scanner.batch_progress_monitor import BatchProgressMonitor
from src.github_ioc_scanner.batch_performance_analyzer import BatchPerformanceAnalyzer
from src.github_ioc_scanner.batch_models import BatchStrategy


async def simulate_batch_operations():
    """Simulate batch operations with monitoring and analysis."""
    
    print("🚀 Starting Batch Performance Monitoring Example")
    print("=" * 60)
    
    # Initialize monitoring components
    metrics_collector = BatchMetricsCollector(enable_detailed_tracking=True)
    progress_monitor = BatchProgressMonitor(enable_verbose_logging=False)
    performance_analyzer = BatchPerformanceAnalyzer()
    
    # Start monitoring
    total_operations = 50
    progress_monitor.start_monitoring(total_operations, "example_batch_scan")
    
    print(f"📊 Monitoring {total_operations} batch operations...")
    
    # Simulate batch operations with varying performance
    completed = 0
    success_count = 0
    failure_count = 0
    
    for batch_num in range(10):  # 10 batches of 5 operations each
        batch_size = 5
        batch_start_time = time.time()
        
        # Simulate different performance characteristics
        if batch_num < 3:
            # Early batches: slower, some failures
            await asyncio.sleep(0.8)  # Slower processing
            batch_success = 4  # 1 failure per batch
            batch_failures = 1
            cache_hits = 2  # Low cache hit rate
        elif batch_num < 7:
            # Middle batches: improving performance
            await asyncio.sleep(0.5)  # Faster processing
            batch_success = 5  # No failures
            batch_failures = 0
            cache_hits = 3  # Better cache hit rate
        else:
            # Later batches: optimal performance
            await asyncio.sleep(0.3)  # Fast processing
            batch_success = 5  # No failures
            batch_failures = 0
            cache_hits = 4  # High cache hit rate
        
        batch_duration = time.time() - batch_start_time
        
        # Update counters
        completed += batch_size
        success_count += batch_success
        failure_count += batch_failures
        
        # Record metrics
        strategy = BatchStrategy.PARALLEL if batch_num >= 5 else BatchStrategy.SEQUENTIAL
        metrics_collector.record_batch_operation(
            operation_type="file_batch",
            duration=batch_duration,
            batch_size=batch_size,
            success_count=batch_success,
            total_count=batch_size,
            cache_hits=cache_hits,
            strategy=strategy
        )
        
        # Update progress
        progress_monitor.update_progress(
            completed=completed,
            success_count=success_count,
            failure_count=failure_count,
            current_batch_size=batch_size
        )
        
        # Show progress
        eta = progress_monitor.calculate_eta()
        eta_str = eta.estimated_time_remaining_str if eta else "calculating..."
        print(f"  Batch {batch_num + 1}/10: {completed}/{total_operations} ops, "
              f"success rate: {(success_count/completed)*100:.1f}%, ETA: {eta_str}")
    
    # Finish monitoring
    final_stats = progress_monitor.finish_monitoring()
    
    print("\n📈 Final Statistics:")
    print(f"  Total Duration: {final_stats['total_duration_seconds']:.1f}s")
    print(f"  Success Rate: {final_stats['success_rate']:.1f}%")
    print(f"  Processing Rate: {final_stats['average_operations_per_second']:.1f} ops/sec")
    
    # Get performance summary
    print("\n📊 Performance Metrics:")
    performance_summary = metrics_collector.get_performance_summary()
    efficiency_metrics = metrics_collector.get_efficiency_metrics()
    
    print(f"  Cache Efficiency: {efficiency_metrics['cache_efficiency']:.1f}%")
    print(f"  Batch Efficiency: {efficiency_metrics['batch_efficiency']:.1f}%")
    print(f"  Time Efficiency: {efficiency_metrics['time_efficiency']:.1f} ops/sec")
    print(f"  Overall Efficiency: {efficiency_metrics['overall_efficiency']:.1f}%")
    
    # Perform comprehensive analysis
    print("\n🔍 Performance Analysis:")
    analysis = performance_analyzer.analyze_performance(metrics_collector, progress_monitor)
    
    print(f"  Overall Score: {analysis.overall_score:.1f}/100")
    
    if analysis.bottlenecks:
        print("  Bottlenecks Identified:")
        for bottleneck in analysis.bottlenecks:
            print(f"    • {bottleneck}")
    else:
        print("  No significant bottlenecks identified")
    
    print(f"\n💡 Optimization Recommendations ({len(analysis.recommendations)} found):")
    for i, rec in enumerate(analysis.recommendations[:3], 1):  # Show top 3
        print(f"  {i}. [{rec.priority.value.upper()}] {rec.title}")
        print(f"     {rec.description}")
        if rec.expected_improvement:
            print(f"     Expected: {rec.expected_improvement}")
        print()
    
    # Show trend analysis if available
    if analysis.trend_analysis:
        print("📈 Performance Trends:")
        for op_type, trend_info in analysis.trend_analysis.items():
            status = "improving" if trend_info['is_improving'] else "stable/degrading"
            print(f"  {op_type}: {status} (avg: {trend_info['recent_average']:.2f}s)")
    
    # Demonstrate alerts using BatchMetrics
    print("\n🚨 Performance Alerts:")
    from src.github_ioc_scanner.batch_models import BatchMetrics
    
    # Create a BatchMetrics object for alert testing
    test_metrics = BatchMetrics(
        total_requests=completed,
        successful_requests=success_count,
        failed_requests=failure_count,
        cache_hits=sum(metrics_collector.operation_metrics[op].cache_hits 
                      for op in metrics_collector.operation_metrics),
        cache_misses=completed - sum(metrics_collector.operation_metrics[op].cache_hits 
                                   for op in metrics_collector.operation_metrics)
    )
    test_metrics.finish()
    
    alerts = progress_monitor.alert_on_performance_issues(test_metrics)
    if alerts:
        for alert in alerts:
            print(f"  ⚠️  {alert}")
    else:
        print("  ✅ No performance issues detected")
    
    print("\n" + "=" * 60)
    print("✨ Batch Performance Monitoring Example Complete!")
    
    return analysis


def demonstrate_historical_analysis():
    """Demonstrate historical analysis capabilities."""
    print("\n📚 Historical Analysis Demo:")
    
    analyzer = BatchPerformanceAnalyzer()
    
    # Set baseline metrics
    baseline = {
        'cache_efficiency': 40.0,
        'batch_efficiency': 85.0,
        'time_efficiency': 3.0,
        'overall_efficiency': 60.0
    }
    analyzer.set_baseline_metrics(baseline)
    print("  Baseline metrics set for comparison")
    
    # Simulate multiple analyses over time
    for i in range(3):
        # Create mock metrics collector
        collector = BatchMetricsCollector()
        
        # Simulate improving performance over time
        cache_eff = 40.0 + (i * 15)  # Improving cache
        batch_eff = 85.0 + (i * 5)   # Improving batch success
        time_eff = 3.0 + (i * 2)     # Improving speed
        
        # Record some operations
        for j in range(5):
            collector.record_batch_operation(
                f"test_op_{i}",
                duration=2.0 - (i * 0.3),  # Getting faster
                batch_size=10,
                success_count=9 + i,  # Getting more successful
                total_count=10,
                cache_hits=4 + (i * 2)  # Better cache hits
            )
        
        # Analyze performance
        analysis = analyzer.analyze_performance(collector)
        print(f"  Analysis {i+1}: Score {analysis.overall_score:.1f}/100")
    
    # Get performance summary
    summary = analyzer.get_performance_summary()
    print(f"  Performance trend: {summary['score_trend']}")
    print(f"  Average score: {summary['average_score']:.1f}")
    
    if summary['common_bottlenecks']:
        print(f"  Common issues: {', '.join(summary['common_bottlenecks'])}")


if __name__ == "__main__":
    # Run the example
    asyncio.run(simulate_batch_operations())
    
    # Demonstrate historical analysis
    demonstrate_historical_analysis()