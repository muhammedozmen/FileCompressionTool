#!/usr/bin/env python3
import os
import time
import unittest
from algorithms import RLE, HuffmanCoding, LZW
from compressor import Compressor

class TestCompressionAlgorithms(unittest.TestCase):
    
    def setUp(self):
        # Create test data
        self.test_data = b"This is a test string with some repetition. AAAAAAAAABBBBBBBCCCCC"
        self.binary_data = bytes([i % 256 for i in range(1000)])
        
        # Create a test file
        self.test_file = "test_temp.txt"
        with open(self.test_file, "wb") as f:
            f.write(self.test_data)
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        if os.path.exists(self.test_file + ".cmp"):
            os.remove(self.test_file + ".cmp")
        
        if os.path.exists(self.test_file + ".decompressed"):
            os.remove(self.test_file + ".decompressed")
    
    def test_rle_compression(self):
        # Test RLE compression/decompression
        rle = RLE()
        compressed = rle.compress(self.test_data)
        decompressed = rle.decompress(compressed)
        
        self.assertEqual(self.test_data, decompressed)
        
        # Test with binary data
        compressed = rle.compress(self.binary_data)
        decompressed = rle.decompress(compressed)
        
        self.assertEqual(self.binary_data, decompressed)
    
    def test_huffman_compression(self):
        # Test Huffman compression/decompression
        huffman = HuffmanCoding()
        compressed = huffman.compress(self.test_data)
        decompressed = huffman.decompress(compressed)
        
        self.assertEqual(self.test_data, decompressed)
        
        # Test with binary data
        compressed = huffman.compress(self.binary_data)
        decompressed = huffman.decompress(compressed)
        
        self.assertEqual(self.binary_data, decompressed)
    
    def test_lzw_compression(self):
        # Test LZW compression/decompression
        lzw = LZW()
        compressed = lzw.compress(self.test_data)
        decompressed = lzw.decompress(compressed)
        
        self.assertEqual(self.test_data, decompressed)
        
        # Test with binary data
        compressed = lzw.compress(self.binary_data)
        decompressed = lzw.decompress(compressed)
        
        self.assertEqual(self.binary_data, decompressed)
    
    def test_compressor_workflow(self):
        # Test the full compression workflow with all algorithms
        for algo in ["rle", "huffman", "lzw"]:
            # Initialize compressor with algorithm
            compressor = Compressor(algo)
            
            # Compress the file
            compressor.compress_file(self.test_file, self.test_file + ".cmp")
            
            # Verify the compressed file exists
            self.assertTrue(os.path.exists(self.test_file + ".cmp"))
            
            # Decompress the file
            compressor.decompress_file(self.test_file + ".cmp", self.test_file + ".decompressed")
            
            # Verify the decompressed file exists
            self.assertTrue(os.path.exists(self.test_file + ".decompressed"))
            
            # Verify the content matches the original
            with open(self.test_file + ".decompressed", "rb") as f:
                decompressed_data = f.read()
            
            self.assertEqual(self.test_data, decompressed_data)
            
            # Clean up test files for next algorithm
            os.remove(self.test_file + ".cmp")
            os.remove(self.test_file + ".decompressed")
    
    def test_empty_file(self):
        # Test compression/decompression of empty files
        empty_data = b""
        
        for algorithm in [RLE(), HuffmanCoding(), LZW()]:
            compressed = algorithm.compress(empty_data)
            decompressed = algorithm.decompress(compressed)
            self.assertEqual(empty_data, decompressed)

if __name__ == "__main__":
    unittest.main() 