"""
Test file for debugging filter function and CSV parsing.
"""

import csv
from config import columns, filter_obj
from filter_toolkit import filter_row

def test_filter_row(row, columns, filter_obj):
    """
    Test filter_row function with detailed output.
    
    Args:
        row: List of values from the CSV row
        columns: List of column names
        filter_obj: Filter object defining the conditions
    """
    print("\nTesting row:")
    print(f"Row values: {row}")
    
    # Print relevant fields
    cnae_principal_idx = columns.index("CNAE_FISCAL_PRINCIPAL")
    cnae_secundaria_idx = columns.index("CNAE_FISCAL_SECUNDARIA")
    
    print(f"CNAE_FISCAL_PRINCIPAL: {row[cnae_principal_idx]}")
    print(f"CNAE_FISCAL_SECUNDARIA: {row[cnae_secundaria_idx]}")
    
    # Test filter
    result = filter_row(row, columns, filter_obj)
    print(f"Filter result: {result}")
    return result

def test_csv_file(file_path, filter_obj, max_rows=5):
    """
    Test CSV file processing with detailed output.
    
    Args:
        file_path: Path to the CSV file
        filter_obj: Filter object defining the conditions
        max_rows: Maximum number of rows to test
    """
    print(f"\nTesting file: {file_path}")
    print(f"Filter object: {filter_obj}")
    print(f"Using columns from config: {columns}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        csv_header = next(reader)  # Skip header
        print(f"\nCSV Header: {csv_header}")
        
        matches = 0
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
                
            print(f"\nRow {i+1}:")
            if test_filter_row(row, columns, filter_obj):
                matches += 1
                print("*** MATCH FOUND ***")
    
    print(f"\nTotal matches: {matches}")

if __name__ == "__main__":
    # Test with a single row
    test_row = [
        "26891925", "0001", "63", "1", "KISPERQUE EMPRESARIAL", "08", "20170203", "01",
        "", "", "20170118", "8599604", "", "RUA", "MAJOR INACIO GOMES DA COSTA", "177",
        "CASA", "UBERABA", "81570150", "PR", "7535", "41", "95322741", "", "", "", "",
        "rodrigokispergue@yahoo.com.br", "", ""
    ]
    
    print("Testing single row:")
    test_filter_row(test_row, columns, filter_obj)
    
    # Test with CSV file
    print("\nTesting CSV file:")
    test_csv_file("test.csv", filter_obj, max_rows=5) 