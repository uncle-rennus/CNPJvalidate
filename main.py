"""
Main script to process large CSV files with filtering.
"""

import csv
import argparse
from tqdm import tqdm
from config import columns, filter_obj
from filter_toolkit import filter_row
from encoding_detector import detect_encoding, validate_encoding

def count_lines(file_path, encoding='utf-8'):
    """Count total lines in file for progress bar"""
    with open(file_path, 'r', encoding=encoding) as f:
        return sum(1 for _ in f) - 1  # Subtract header

def process_csv(input_file: str, output_file: str, chunk_size: int = 1000):
    """
    Process CSV file in chunks and write matching rows to output file.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        chunk_size: Number of rows to process at once
    """
    print(f"Processing {input_file}")
    print(f"Using columns from config: {columns}")
    print(f"Filter object: {filter_obj}")
    
    # Detect encoding
    detected_encoding, first_row = detect_encoding(input_file)
    print(f"Detected encoding: {detected_encoding}")
    
    # Validate encoding
    if not validate_encoding(input_file, detected_encoding):
        print("Encoding validation failed, falling back to latin-1")
        detected_encoding = 'latin-1'
    
    # Count total lines for progress bar
    try:
        total_lines = count_lines(input_file, detected_encoding)
    except UnicodeDecodeError:
        print("Failed to count lines with detected encoding, trying latin-1")
        detected_encoding = 'latin-1'
        total_lines = count_lines(input_file, detected_encoding)
    
    # Process file
    with open(input_file, 'r', encoding=detected_encoding) as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter=';', quotechar='"')
        writer = csv.writer(outfile, delimiter=';', quotechar='"')
        
        # Write header
        writer.writerow(columns)
        
        # Skip CSV header
        next(reader)
        
        # Process rows
        matches = 0
        with tqdm(total=total_lines, desc=f"Processing rows (using {detected_encoding})") as pbar:
            for row in reader:
                if filter_row(row, columns, filter_obj):
                    writer.writerow(row)
                    matches += 1
                pbar.update(1)
    
    print(f"\nProcessing complete!")
    print(f"Total matches: {matches}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process CSV file with filtering')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('--output', '-o', default='output.csv', help='Output CSV file path')
    parser.add_argument('--chunk_size', '-c', type=int, default=1000, help='Number of rows to process at once')
    
    args = parser.parse_args()
    
    try:
        process_csv(args.input_file, args.output, args.chunk_size)
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
    except Exception as e:
        print(f"\nError processing file: {str(e)}") 