#!/usr/bin/env python3
"""
Run all tests for the File Compression Tool.
"""
import os
import sys
import unittest
import subprocess

def run_unit_tests():
    """Run unit tests for the compression algorithms"""
    print("Running unit tests...")
    print("=" * 80)
    unittest.main(module='test_compression', argv=['first-arg-is-ignored'], exit=False)
    print("=" * 80)

def run_benchmark_tests():
    """Run benchmark tests"""
    print("\nRunning benchmark tests on generated data...")
    print("=" * 80)
    subprocess.run([sys.executable, "benchmark.py"])
    print("=" * 80)

def run_benchmark_on_test_file():
    """Run benchmark tests on the test file"""
    if os.path.exists("test_file.txt"):
        print("\nRunning benchmark tests on test_file.txt...")
        print("=" * 80)
        subprocess.run([sys.executable, "benchmark.py", "test_file.txt"])
        print("=" * 80)
    else:
        print("test_file.txt not found. Skipping benchmark on test file.")

def main():
    print("File Compression Tool - Test Runner")
    print("=" * 80)
    
    try:
        run_unit_tests()
        run_benchmark_tests()
        run_benchmark_on_test_file()
        
        print("\nAll tests completed.")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 