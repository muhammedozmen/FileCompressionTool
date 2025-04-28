#!/usr/bin/env python3
import os
import sys
import argparse
from compressor import Compressor

def create_parser():
    parser = argparse.ArgumentParser(description="File Compression Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress a file")
    compress_parser.add_argument("input_file", help="Input file to compress")
    compress_parser.add_argument("output_file", nargs="?", help="Output file (default: input_file.cmp)")
    compress_parser.add_argument("--algorithm", "-a", choices=["rle", "huffman", "lzw"], 
                                 default="lzw", help="Compression algorithm to use")
    
    # Decompress command
    decompress_parser = subparsers.add_parser("decompress", help="Decompress a file")
    decompress_parser.add_argument("input_file", help="Input file to decompress")
    decompress_parser.add_argument("output_file", nargs="?", help="Output file (default: auto-detect)")
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "compress":
            compressor = Compressor(args.algorithm)
            compressor.compress_file(args.input_file, args.output_file)
            
        elif args.command == "decompress":
            compressor = Compressor()  # Algorithm will be detected from the file
            compressor.decompress_file(args.input_file, args.output_file)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 