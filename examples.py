#!/usr/bin/env python3
"""
Examples for using the File Compression Tool API programmatically.
"""
import os
from compressor import Compressor

def example_compress_text_file():
    """Example: Compress a text file using different algorithms"""
    print("Example: Compressing text file with different algorithms")
    print("-" * 80)
    
    # Create a sample text file if it doesn't exist
    sample_file = "sample.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write("This is a sample text file to demonstrate compression.\n" * 100)
        print(f"Created sample text file: {sample_file}")
    
    # Compress with different algorithms
    algorithms = ["rle", "huffman", "lzw"]
    results = []
    
    for algo in algorithms:
        print(f"\nCompressing with {algo.upper()}:")
        compressor = Compressor(algo)
        output_file = f"sample_{algo}.cmp"
        
        # Compress the file
        size, ratio, time_taken = compressor.compress_file(sample_file, output_file)
        
        results.append({
            "algorithm": algo.upper(),
            "output_file": output_file,
            "original_size": os.path.getsize(sample_file),
            "compressed_size": size,
            "ratio": ratio,
            "time": time_taken
        })
    
    # Compare results
    print("\nCompression Results Comparison:")
    print("-" * 80)
    print(f"{'Algorithm':<10} {'Original':<10} {'Compressed':<10} {'Ratio':<10} {'Time':<10}")
    print(f"{'':^10} {'(bytes)':<10} {'(bytes)':<10} {'(%)':<10} {'(sec)':<10}")
    print("-" * 80)
    
    for result in results:
        print(
            f"{result['algorithm']:<10} "
            f"{result['original_size']:<10} "
            f"{result['compressed_size']:<10} "
            f"{result['ratio']:.2f}%{'':<5} "
            f"{result['time']:.4f}{'':<4} "
        )

def example_decompress_file():
    """Example: Decompress a compressed file"""
    print("\nExample: Decompressing a file")
    print("-" * 80)
    
    # Check if there's a compressed file to decompress
    compressed_files = [f for f in os.listdir(".") if f.endswith(".cmp")]
    
    if not compressed_files:
        print("No compressed files found. Run example_compress_text_file() first.")
        return
    
    # Use the first compressed file
    compressed_file = compressed_files[0]
    print(f"Decompressing file: {compressed_file}")
    
    # Create a compressor
    compressor = Compressor()
    
    # Decompress the file
    output_file = f"decompressed_{os.path.basename(compressed_file)}.txt"
    size, time_taken = compressor.decompress_file(compressed_file, output_file)
    
    print(f"File decompressed successfully: {output_file}")
    print(f"Decompressed size: {size} bytes")
    print(f"Time taken: {time_taken:.4f} seconds")
    
    # Verify content matches original
    original_file = "sample.txt"
    if os.path.exists(original_file):
        with open(original_file, "rb") as f1, open(output_file, "rb") as f2:
            original_data = f1.read()
            decompressed_data = f2.read()
        
        if original_data == decompressed_data:
            print("Verification: Decompressed file matches the original file.")
        else:
            print("Verification: Decompressed file does NOT match the original file!")

def example_compress_binary_file():
    """Example: Compress a binary file"""
    print("\nExample: Compressing a binary file")
    print("-" * 80)
    
    # Create a sample binary file if it doesn't exist
    sample_binary = "sample.bin"
    if not os.path.exists(sample_binary):
        with open(sample_binary, "wb") as f:
            # Write some random binary data
            for i in range(10000):
                f.write(bytes([i % 256]))
        print(f"Created sample binary file: {sample_binary}")
    
    # Compress with LZW algorithm
    compressor = Compressor("lzw")
    output_file = "sample_binary.cmp"
    
    # Compress the file
    size, ratio, time_taken = compressor.compress_file(sample_binary, output_file)
    
    print(f"Original size: {os.path.getsize(sample_binary)} bytes")
    print(f"Compressed size: {size} bytes")
    print(f"Compression ratio: {ratio:.2f}%")
    print(f"Time taken: {time_taken:.4f} seconds")

def cleanup():
    """Clean up sample files"""
    files_to_remove = [
        "sample.txt", 
        "sample.bin",
        "sample_rle.cmp", 
        "sample_huffman.cmp", 
        "sample_lzw.cmp",
        "sample_binary.cmp"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")
    
    # Remove any decompressed files
    for file in [f for f in os.listdir(".") if f.startswith("decompressed_")]:
        os.remove(file)
        print(f"Removed: {file}")

def main():
    print("File Compression Tool - Examples")
    print("=" * 80)
    print("This script demonstrates how to use the File Compression Tool API.")
    print("=" * 80)
    
    try:
        example_compress_text_file()
        example_decompress_file()
        example_compress_binary_file()
        
        # Ask if user wants to clean up files
        response = input("\nDo you want to clean up sample files? (y/n): ")
        if response.lower() in ("y", "yes"):
            cleanup()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 