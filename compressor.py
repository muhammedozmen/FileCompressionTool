import os
import time
import struct
from tqdm import tqdm
from algorithms import get_algorithm

# Magic bytes to identify our compressed files
MAGIC = b'CMPR'
VERSION = 1

class Compressor:
    """Main compression class that handles file operations and uses algorithms"""
    
    def __init__(self, algorithm_name='lzw'):
        self.algorithm = get_algorithm(algorithm_name)
        self.algorithm_name = algorithm_name.lower()
    
    def compress_file(self, input_file, output_file=None):
        """Compress a file and save it to output_file"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # If output file not specified, use the input file name with .cmp extension
        if output_file is None:
            output_file = input_file + '.cmp'
        
        start_time = time.time()
        
        # Get file size for progress bar
        file_size = os.path.getsize(input_file)
        
        # Read the input file
        with open(input_file, 'rb') as f:
            data = f.read()
        
        print(f"Original size: {file_size} bytes")
        
        # Compress the data
        print(f"Compressing with {self.algorithm_name.upper()}...")
        compressed_data = self.algorithm.compress(data)
        
        # Write the compressed data to the output file
        with open(output_file, 'wb') as f:
            # Write magic bytes, version, and algorithm name
            f.write(MAGIC)
            f.write(struct.pack('B', VERSION))
            algo_bytes = self.algorithm_name.encode('utf-8')
            f.write(struct.pack('B', len(algo_bytes)))
            f.write(algo_bytes)
            
            # Write original file extension
            ext = os.path.splitext(input_file)[1].encode('utf-8')
            f.write(struct.pack('B', len(ext)))
            f.write(ext)
            
            # Write the compressed data
            f.write(compressed_data)
        
        compressed_size = os.path.getsize(output_file)
        end_time = time.time()
        
        # Calculate compression statistics
        compression_ratio = (1 - compressed_size / file_size) * 100 if file_size > 0 else 0
        time_taken = end_time - start_time
        
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}%")
        print(f"Time taken: {time_taken:.2f} seconds")
        
        return compressed_size, compression_ratio, time_taken
    
    def decompress_file(self, input_file, output_file=None):
        """Decompress a file and save it to output_file"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        start_time = time.time()
        
        # Read the compressed file
        with open(input_file, 'rb') as f:
            # Read magic bytes and version
            magic = f.read(4)
            if magic != MAGIC:
                raise ValueError("Not a valid compressed file (invalid magic bytes)")
            
            version = struct.unpack('B', f.read(1))[0]
            if version != VERSION:
                raise ValueError(f"Unsupported version: {version}")
            
            # Read algorithm name
            algo_len = struct.unpack('B', f.read(1))[0]
            algorithm_name = f.read(algo_len).decode('utf-8')
            
            # Read original file extension
            ext_len = struct.unpack('B', f.read(1))[0]
            ext = f.read(ext_len).decode('utf-8')
            
            # Read the compressed data
            compressed_data = f.read()
        
        # If output file not specified, use the input file name without .cmp extension
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            if ext:
                output_file = base_name + ext
            else:
                output_file = base_name + ".decompressed"
        
        # Use the correct algorithm for decompression
        algorithm = get_algorithm(algorithm_name)
        
        # Decompress the data
        print(f"Decompressing with {algorithm_name.upper()}...")
        decompressed_data = algorithm.decompress(compressed_data)
        
        # Write the decompressed data to the output file
        with open(output_file, 'wb') as f:
            f.write(decompressed_data)
        
        decompressed_size = len(decompressed_data)
        end_time = time.time()
        
        # Calculate decompression statistics
        time_taken = end_time - start_time
        
        print(f"Decompressed size: {decompressed_size} bytes")
        print(f"Time taken: {time_taken:.2f} seconds")
        
        return decompressed_size, time_taken 