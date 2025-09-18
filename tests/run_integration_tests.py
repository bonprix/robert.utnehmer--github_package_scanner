#!/usr/bin/env python3
"""
Integration test runner for the GitHub IOC Scanner.

This script runs all integration tests and provides a summary of results.
It can be used to verify that all integration test scenarios are working correctly.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_test_suite(test_file: str, description: str) -> tuple[bool, float, str]:
    """Run a test suite and return results."""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED ({duration:.2f}s)")
            return True, duration, result.stdout
        else:
            print(f"❌ {description} - FAILED ({duration:.2f}s)")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, duration, result.stderr
            
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print(f"⏰ {description} - TIMEOUT ({duration:.2f}s)")
        return False, duration, "Test suite timed out"
    except Exception as e:
        duration = time.time() - start_time
        print(f"💥 {description} - ERROR ({duration:.2f}s): {e}")
        return False, duration, str(e)


def main():
    """Run all integration test suites."""
    print("GitHub IOC Scanner - Integration Test Runner")
    print("=" * 60)
    
    # Define test suites
    test_suites = [
        ("tests/test_integration.py", "End-to-End Integration Tests"),
        ("tests/test_e2e_cli.py", "CLI Integration Tests"),
        ("tests/test_error_recovery.py", "Error Handling & Recovery Tests"),
        ("tests/test_performance.py", "Performance Tests"),
    ]
    
    # Track results
    results = []
    total_start_time = time.time()
    
    # Run each test suite
    for test_file, description in test_suites:
        if not Path(test_file).exists():
            print(f"⚠️  Skipping {description} - file not found: {test_file}")
            results.append((description, False, 0, "File not found"))
            continue
            
        success, duration, output = run_test_suite(test_file, description)
        results.append((description, success, duration, output))
    
    total_duration = time.time() - total_start_time
    
    # Print summary
    print(f"\n{'='*60}")
    print("INTEGRATION TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success, _, _ in results if success)
    total = len(results)
    
    print(f"Total test suites: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Total duration: {total_duration:.2f}s")
    
    print(f"\nDetailed Results:")
    print("-" * 60)
    
    for description, success, duration, output in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {description:<35} | {duration:>6.2f}s")
    
    # Print recommendations
    print(f"\n{'='*60}")
    print("RECOMMENDATIONS")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        print("✅ The GitHub IOC Scanner integration is working correctly.")
        print("✅ All scanning workflows are functional.")
        print("✅ Error handling and recovery mechanisms are working.")
        print("✅ Performance characteristics are within acceptable limits.")
    else:
        print("⚠️  Some integration tests failed.")
        print("🔍 Review the failed test output above for details.")
        print("🛠️  Fix any issues before deploying to production.")
        
        failed_suites = [desc for desc, success, _, _ in results if not success]
        print(f"📋 Failed test suites: {', '.join(failed_suites)}")
    
    # Performance insights
    performance_results = [
        (desc, duration) for desc, success, duration, _ in results 
        if success and "Performance" in desc
    ]
    
    if performance_results:
        print(f"\n📊 Performance Insights:")
        for desc, duration in performance_results:
            if duration > 60:
                print(f"⚠️  {desc} took {duration:.2f}s (consider optimization)")
            else:
                print(f"✅ {desc} completed in {duration:.2f}s")
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()