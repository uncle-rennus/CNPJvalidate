"""
Encoding detection utilities for CSV files.
"""

import chardet
from typing import Tuple, List
import csv

def detect_encoding(file_path: str, sample_size: int = 10000) -> Tuple[str, List[str]]:
    """
    Detect the encoding of a CSV file by analyzing a sample.
    Also returns the first row to validate the header.

    Args:
        file_path: Path to the CSV file
        sample_size: Number of bytes to sample

    Returns:
        Tuple[str, List[str]]: Detected encoding and first row
    """
    # Read sample bytes
    with open(file_path, 'rb') as f:
        sample = f.read(sample_size)
    
    # Check for non-ASCII bytes first
    has_non_ascii = any(b > 127 for b in sample)
    
    # If we have non-ASCII bytes, try UTF-8 first
    if has_non_ascii:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';', quotechar='"')
                first_row = next(reader)
                print("Successfully validated with utf-8")
                return 'utf-8', first_row
        except Exception as e:
            print(f"Failed to validate with utf-8: {str(e)}")
    
    # Use chardet for encoding detection
    result = chardet.detect(sample)
    detected_encoding = result['encoding']
    confidence = result['confidence']
    
    # If ASCII is detected but we have non-ASCII bytes, force UTF-8
    if detected_encoding == 'ascii' and has_non_ascii:
        detected_encoding = 'utf-8'
        confidence = 0.8
    
    print(f"Detected encoding: {detected_encoding} (confidence: {confidence:.2f})")
    print(f"Non-ASCII bytes found: {has_non_ascii}")
    
    # Try to read first row to validate
    encodings_to_try = [detected_encoding, 'latin-1', 'cp1252']
    
    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                reader = csv.reader(f, delimiter=';', quotechar='"')
                first_row = next(reader)
                print(f"Successfully validated with {enc}")
                return enc, first_row
        except Exception as e:
            print(f"Failed to validate with {enc}: {str(e)}")
            continue
    
    # If all else fails, return latin-1
    return 'latin-1', []

def validate_encoding(file_path: str, encoding: str, num_rows: int = 5) -> bool:
    """
    Validate the encoding by trying to read a few rows.

    Args:
        file_path: Path to the CSV file
        encoding: Encoding to validate
        num_rows: Number of rows to try reading

    Returns:
        bool: True if encoding is valid
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            for _ in range(num_rows):
                next(reader)
        return True
    except Exception as e:
        print(f"Encoding validation failed: {str(e)}")
        return False 