# File Compression Tool

A lightweight and efficient file compression tool that reduces file sizes while maintaining data integrity.

## Features

- Compresses and decompresses files using multiple algorithms
- Supports common file formats (.txt, .zip, .png, etc.)
- Command line interface for quick operations
- GUI interface for ease of use
- Maintains data integrity during compression/decompression

## Installation

### Setting up a Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

#### On Windows

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

#### On Linux/macOS

1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

After activating the virtual environment, run:

```
python compress.py compress <input_file> <output_file> [--algorithm <algorithm>]
python compress.py decompress <input_file> <output_file>
```

Example:
```
python compress.py compress test_file.txt test_file.cmp --algorithm lzw
python compress.py decompress test_file.cmp test_file_restored.txt
```

### GUI Interface

After activating the virtual environment, run:

```
python gui.py
```

## Supported Algorithms

- **Run-Length Encoding (RLE)**: Simple compression that replaces sequences of the same data values with a count and a single value. Good for files with many repeated bytes.
- **Huffman Coding**: Variable-length encoding that assigns shorter codes to frequently occurring characters. Good for text files.
- **LZW (Lempel-Ziv-Welch)**: Dictionary-based algorithm that builds a dictionary of substrings. Generally the most effective overall compression algorithm in this tool.

## Running Tests

Run unit tests and benchmarks to verify functionality:
```
python run_tests.py
```

## Examples

Run the examples script to see the tool in action:
```
python examples.py
```

## Benchmarking

Compare the performance of different compression algorithms:
```
python benchmark.py [file_to_benchmark]