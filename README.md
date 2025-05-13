# CNPJ CSV Filter

A Python tool for processing large CNPJ CSV files with complex filtering conditions. Built to handle large files efficiently with proper encoding detection and memory management.

## Features

- Processes large CSV files in chunks
- Automatic encoding detection
- Complex filtering with logical operations (AND, OR, NOT)
- Progress bar with tqdm
- Memory-efficient processing
- Configurable filters via config.py

## Installation

1. Clone the repository:
```bash
git clone https://github.com/uncle-rennus/CNPJvalidate
cd CNPJvalidate
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Configure your filter in `config.py`:
```python
filter_obj = AND(
    OR(
        contains("CNAE_FISCAL_PRINCIPAL", "8599604"),
        # ... more conditions
    ),
    NOT(
        OR(
            contains("CORREIO_ELETRONICO", "@gmail"),
            # ... more email exclusions
        )
    ),
    OR(
        ne("TELEFONE_1", ""),
        ne("TELEFONE_2", "")
    )
)
```

2. Run the script:
```bash
python main.py input.csv --output filtered.csv --chunk_size 1000
```

## Command Line Arguments

- `input_file`: Path to input CSV file (required)
- `--output`, `-o`: Output file path (default: output.csv)
- `--chunk_size`, `-c`: Number of rows to process at once (default: 1000)

## Project Structure

- `main.py`: Main processing script
- `config.py`: Filter configuration
- `filter_toolkit.py`: Core filtering library
- `encoding_detector.py`: Encoding detection utilities
- `test_filter.py`: Test script for filter debugging

## Filter Toolkit (filter_toolkit.py)

A powerful library for building complex CSV row filters with logical operations. Supports:

- Logical operators: AND, OR, NOT
- String operations: contains, startswith, endswith, regex
- Numeric comparisons: gt, lt, ge, le, eq, ne
- Date comparisons: date_eq, date_ne, date_gt, date_lt, date_ge, date_le
- Boolean operations: bool_eq, bool_ne
- Custom functions via custom() operator

Example:
```python
filter_obj = AND(
    OR(
        contains("CNAE_FISCAL_PRINCIPAL", "8599604"),
        regex("CNPJ_BASICO", r"^[0-9]{8}$")
    ),
    NOT(
        contains("CORREIO_ELETRONICO", "@gmail")
    )
)
```

## Data Transformation (transform_data.py)

Handles the transformation of CNPJ data into Hubspot-compatible format. Features:

- Automatic encoding detection
- Municipality code to name mapping
- Phone number formatting and consolidation
- Address standardization
- Required field validation
- Memory-efficient processing

Key transformations:
- CNPJ formatting (combines basic, order, and DV)
- Address formatting (combines type and street)
- Phone consolidation (primary, secondary, fax)
- Municipality code to name conversion
- Email standardization

Usage:
```bash
python transform_data.py input.csv output.csv
```

## Filter Operations

See [Filter Toolkit Documentation](README_filter_toolkit.md) for detailed information about available filter operations.

## License

This project is licensed under the MIT License. 
