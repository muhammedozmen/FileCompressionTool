import os
import pickle
import heapq
from collections import Counter, defaultdict

class CompressionAlgorithm:
    """Base class for compression algorithms"""
    
    def compress(self, data):
        """Compress the data"""
        raise NotImplementedError("Subclasses must implement compress method")
    
    def decompress(self, compressed_data):
        """Decompress the data"""
        raise NotImplementedError("Subclasses must implement decompress method")


class RLE(CompressionAlgorithm):
    """Run-Length Encoding compression algorithm"""
    
    def compress(self, data):
        if not data:
            return b''
        
        compressed = bytearray()
        count = 1
        current = data[0]
        
        for byte in data[1:]:
            if byte == current and count < 255:
                count += 1
            else:
                compressed.extend([count, current])
                count = 1
                current = byte
        
        compressed.extend([count, current])
        return bytes(compressed)
    
    def decompress(self, compressed_data):
        if not compressed_data:
            return b''
        
        decompressed = bytearray()
        for i in range(0, len(compressed_data), 2):
            if i + 1 < len(compressed_data):
                count = compressed_data[i]
                value = compressed_data[i + 1]
                decompressed.extend([value] * count)
        
        return bytes(decompressed)


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding(CompressionAlgorithm):
    """Huffman Coding compression algorithm"""
    
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
    
    def _make_frequency_dict(self, data):
        return Counter(data)
    
    def _make_heap(self, frequency):
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(self.heap, node)
    
    def _merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(self.heap, merged)
    
    def _make_codes(self, root, current_code):
        if root is None:
            return
        
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
        
        self._make_codes(root.left, current_code + "0")
        self._make_codes(root.right, current_code + "1")
    
    def _get_encoded_text(self, data):
        encoded_text = ""
        for char in data:
            encoded_text += self.codes[char]
        return encoded_text
    
    def _pad_encoded_text(self, encoded_text):
        padding = 8 - (len(encoded_text) % 8)
        if padding == 8:
            padding = 0
        
        padded_text = encoded_text + "0" * padding
        padded_info = format(padding, "08b")
        
        return padded_info + padded_text
    
    def _bytes_to_binary(self, data):
        binary = ""
        for byte in data:
            binary += format(byte, "08b")
        return binary
    
    def compress(self, data):
        if not data:
            return pickle.dumps((b'', {}))
        
        frequency = self._make_frequency_dict(data)
        self._make_heap(frequency)
        self._merge_nodes()
        root = heapq.heappop(self.heap)
        self._make_codes(root, "")
        
        encoded_text = self._get_encoded_text(data)
        padded_encoded_text = self._pad_encoded_text(encoded_text)
        
        # Convert the padded encoded text to bytes
        byte_array = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            byte_array.append(int(byte, 2))
        
        # Store the compressed data and the codes dict for decompression
        return pickle.dumps((bytes(byte_array), self.reverse_mapping))
    
    def _remove_padding(self, bit_string):
        padding_info = bit_string[:8]
        padding = int(padding_info, 2)
        
        bit_string = bit_string[8:]
        if padding > 0:
            bit_string = bit_string[:-padding]
        
        return bit_string
    
    def _decode_text(self, encoded_text, reverse_mapping):
        current_code = ""
        decoded_text = bytearray()
        
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_mapping:
                decoded_text.append(reverse_mapping[current_code])
                current_code = ""
        
        return bytes(decoded_text)
    
    def decompress(self, compressed_data):
        # Extract the byte array and the codes dict
        byte_array, reverse_mapping = pickle.loads(compressed_data)
        
        if not byte_array:
            return b''
        
        # Convert bytes to binary string
        bit_string = self._bytes_to_binary(byte_array)
        
        # Remove padding
        encoded_text = self._remove_padding(bit_string)
        
        # Decode text
        return self._decode_text(encoded_text, reverse_mapping)


class LZW(CompressionAlgorithm):
    """Lempel-Ziv-Welch compression algorithm"""
    
    def compress(self, data):
        if not data:
            return pickle.dumps([])
        
        # Build the dictionary
        dict_size = 256
        dictionary = {bytes([i]): i for i in range(dict_size)}
        
        result = []
        w = bytes([data[0]])
        
        for c in data[1:]:
            wc = w + bytes([c])
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = dict_size
                dict_size += 1
                w = bytes([c])
        
        if w:
            result.append(dictionary[w])
        
        return pickle.dumps(result)
    
    def decompress(self, compressed_data):
        compressed = pickle.loads(compressed_data)
        
        if not compressed:
            return b''
        
        # Build the dictionary
        dict_size = 256
        dictionary = {i: bytes([i]) for i in range(dict_size)}
        
        result = bytearray(dictionary[compressed[0]])
        w = dictionary[compressed[0]]
        
        for k in compressed[1:]:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + bytes([w[0]])
            else:
                raise ValueError("Bad compressed k: %s" % k)
            
            result.extend(entry)
            
            dictionary[dict_size] = w + bytes([entry[0]])
            dict_size += 1
            
            w = entry
        
        return bytes(result)


def get_algorithm(name):
    """Get compression algorithm by name"""
    algorithms = {
        'rle': RLE(),
        'huffman': HuffmanCoding(),
        'lzw': LZW()
    }
    
    if name.lower() not in algorithms:
        raise ValueError(f"Unknown algorithm: {name}")
    
    return algorithms[name.lower()] 