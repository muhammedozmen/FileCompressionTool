#!/usr/bin/env python3
import os
import time
import sys
import random
from compressor import Compressor
from algorithms import RLE, HuffmanCoding, LZW

def generate_test_data(size, pattern_type="random"):
    """Generate test data for benchmarking"""
    if pattern_type == "random":
        # Random bytes
        return bytes([random.randint(0, 255) for _ in range(size)])
    
    elif pattern_type == "repeated":
        # Repeated pattern (highly compressible)
        pattern = b"ABC" * 10
        repeats = size // len(pattern) + 1
        return (pattern * repeats)[:size]
    
    elif pattern_type == "sequential":
        # Sequential bytes
        return bytes([i % 256 for i in range(size)])
    
    else:
        raise ValueError(f"Unknown pattern type: {pattern_type}")

def benchmark_algorithm(algorithm_class, data, name):
    """Benchmark compression and decompression for an algorithm"""
    algorithm = algorithm_class()
    
    # Compression
    start_time = time.time()
    compressed = algorithm.compress(data)
    compress_time = time.time() - start_time
    
    # Decompression
    start_time = time.time()
    decompressed = algorithm.decompress(compressed)
    decompress_time = time.time() - start_time
    
    # Verify
    assert data == decompressed, "Decompressed data does not match original"
    
    # Calculate compression ratio
    original_size = len(data)
    compressed_size = len(compressed)
    ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    
    return {
        "algorithm": name,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "ratio": ratio,
        "compress_time": compress_time,
        "decompress_time": decompress_time
    }

def benchmark_file(file_path):
    """Benchmark compression algorithms on a file"""
    # Read file data
    with open(file_path, "rb") as f:
        data = f.read()
    
    print(f"Benchmarking file: {file_path}")
    print(f"File size: {len(data)} bytes")
    print("-" * 80)
    
    # Run benchmarks
    algorithms = [
        (RLE, "RLE"),
        (HuffmanCoding, "Huffman"),
        (LZW, "LZW")
    ]
    
    results = []
    for algo_class, name in algorithms:
        print(f"Running benchmark for {name}...")
        result = benchmark_algorithm(algo_class, data, name)
        results.append(result)
    
    # Print results
    print("\nResults:")
    print("-" * 80)
    print(f"{'Algorithm':<10} {'Original':<10} {'Compressed':<10} {'Ratio':<10} {'Compress':<10} {'Decompress':<10}")
    print(f"{'':^10} {'(bytes)':<10} {'(bytes)':<10} {'(%)':<10} {'(sec)':<10} {'(sec)':<10}")
    print("-" * 80)
    
    for result in results:
        print(
            f"{result['algorithm']:<10} "
            f"{result['original_size']:<10} "
            f"{result['compressed_size']:<10} "
            f"{result['ratio']:.2f}%{'':<5} "
            f"{result['compress_time']:.4f}{'':<4} "
            f"{result['decompress_time']:.4f}"
        )

def benchmark_generated_data():
    """Benchmark compression algorithms on generated test data"""
    data_types = {
        "random": "Random data (incompressible)",
        "repeated": "Repeated patterns (highly compressible)",
        "sequential": "Sequential data (moderately compressible)"
    }
    
    size = 1_000_000  # 1MB
    
    for data_type, description in data_types.items():
        print(f"\nBenchmarking {description}")
        print(f"Data size: {size} bytes")
        print("-" * 80)
        
        data = generate_test_data(size, data_type)
        
        # Run benchmarks
        algorithms = [
            (RLE, "RLE"),
            (HuffmanCoding, "Huffman"),
            (LZW, "LZW")
        ]
        
        results = []
        for algo_class, name in algorithms:
            print(f"Running benchmark for {name}...")
            result = benchmark_algorithm(algo_class, data, name)
            results.append(result)
        
        # Print results
        print("\nResults:")
        print("-" * 80)
        print(f"{'Algorithm':<10} {'Original':<10} {'Compressed':<10} {'Ratio':<10} {'Compress':<10} {'Decompress':<10}")
        print(f"{'':^10} {'(bytes)':<10} {'(bytes)':<10} {'(%)':<10} {'(sec)':<10} {'(sec)':<10}")
        print("-" * 80)
        
        for result in results:
            print(
                f"{result['algorithm']:<10} "
                f"{result['original_size']:<10} "
                f"{result['compressed_size']:<10} "
                f"{result['ratio']:.2f}%{'':<5} "
                f"{result['compress_time']:.4f}{'':<4} "
                f"{result['decompress_time']:.4f}"
            )

def main():
    # Check if a file is provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        
        benchmark_file(file_path)
    else:
        # Run benchmarks on generated data
        benchmark_generated_data()

if __name__ == "__main__":
    main() 