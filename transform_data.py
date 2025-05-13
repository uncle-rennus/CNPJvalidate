import pandas as pd
from datetime import datetime
import argparse
import chardet
import sys
import re

def load_municipality_codes():
    """Load municipality codes from CSV into a dictionary"""
    try:
        df = pd.read_csv('municipios.csv', encoding='utf-8', header=None, names=['codigo', 'nome'], sep=';', quoting=1, dtype=str)
        # Convert to string and remove quotes
        df['codigo'] = df['codigo'].astype(str).str.strip('"')
        df['nome'] = df['nome'].astype(str).str.strip('"')
        return dict(zip(df['codigo'], df['nome']))
    except Exception as e:
        print(f"Warning: Could not load municipality codes: {e}")
        return {}

# Load municipality codes at module level
MUNICIPALITY_CODES = load_municipality_codes()

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def validate_required_columns(df):
    required_columns = [
        'NOME_FANTASIA', 'CNPJ_BASICO', 'CNPJ_ORDEM', 'CNPJ_DV',
        'LOGRADOURO', 'MUNICIPIO', 'UF', 'PAIS', 'CEP'
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {', '.join(missing_columns)}")
        sys.exit(1)

def format_phone(ddd, phone):
    if pd.isna(ddd) or pd.isna(phone) or str(ddd).strip() == '' or str(phone).strip() == '':
        return None
    try:
        return f"{int(ddd)}{int(phone)}"
    except:
        return None

def extract_domain_from_email(email):
    """Extract domain from email address using regex"""
    if not email:
        return None
    match = re.search(r'@(.+)$', email)
    return f"{match.group(1)}" if match else None

def process_row(row):
    """Process a single row of data and return a dictionary of Hubspot properties"""
    # First strip all fields
    stripped_row = {k: str(v).strip() if pd.notna(v) else '' for k, v in row.items()}
    
    result = {}
    
    # Basic company info
    result['name'] = stripped_row['NOME_FANTASIA']
    result['cnpj'] = stripped_row['CNPJ_BASICO'].zfill(8) + stripped_row['CNPJ_ORDEM'].zfill(4) + stripped_row['CNPJ_DV'].zfill(2)
    
    # Website URL from email domain
    email = stripped_row['CORREIO_ELETRONICO']
    result['website'] = extract_domain_from_email(email)
    
    # Address info
    tipo_logradouro = stripped_row['TIPO_LOGRADOURO']
    logradouro = stripped_row['LOGRADOURO']
    result['address'] = f"{tipo_logradouro} {logradouro}".strip()
    
    result['address2'] = stripped_row['COMPLEMENTO'] if stripped_row['COMPLEMENTO'] else None
    result['numero'] = stripped_row['NUMERO'] if stripped_row['NUMERO'] else None
    result['bairro'] = stripped_row['BAIRRO'] if stripped_row['BAIRRO'] else None
    
    # Convert municipality code to name
    municipio_code = stripped_row['MUNICIPIO']
    result['city'] = MUNICIPALITY_CODES.get(municipio_code, municipio_code) if municipio_code else None
    
    result['state'] = stripped_row['UF']
    result['zip'] = stripped_row['CEP']
    
    # Phone numbers
    phones = []
    
    # Primary phone
    if stripped_row['DDD_1'] and stripped_row['TELEFONE_1']:
        phone1 = format_phone(stripped_row['DDD_1'], stripped_row['TELEFONE_1'])
        if phone1:
            phones.append(phone1)
            result['phone'] = phone1
    
    # Secondary phone
    if stripped_row['DDD_2'] and stripped_row['TELEFONE_2']:
        phone2 = format_phone(stripped_row['DDD_2'], stripped_row['TELEFONE_2'])
        if phone2:
            phones.append(phone2)
    
    # Fax
    if stripped_row['DDD_FAX'] and stripped_row['FAX']:
        fax = format_phone(stripped_row['DDD_FAX'], stripped_row['FAX'])
        if fax:
            phones.append(fax)
    
    # Join all phones with semicolon
    result['telefones_principais'] = ';'.join(phones) if phones else None
    result['todos_os_telefones'] = result['telefones_principais']
    
    # Email
    result['todos_os_e_mails'] = stripped_row['CORREIO_ELETRONICO'] if stripped_row['CORREIO_ELETRONICO'] else None
    
    return result

def transform_to_hubspot_format(input_file, output_file):
    # Detect file encoding
    encoding = detect_encoding(input_file)
    
    # Read the input CSV with semicolon separator and explicit dtype for all columns
    dtypes = {
        'CNPJ_BASICO': str, 'CNPJ_ORDEM': str, 'CNPJ_DV': str,
        'DDD_1': str, 'TELEFONE_1': str, 'DDD_2': str, 'TELEFONE_2': str,
        'DDD_FAX': str, 'FAX': str, 'CEP': str, 'MUNICIPIO': str
    }
    
    # Read input with semicolon separator
    df = pd.read_csv(
        input_file, 
        encoding=encoding, 
        sep=';', 
        quoting=0,
        dtype=dtypes,
        na_values=['', 'nan', 'NaN', 'NULL', 'null', 'None', 'none'],
        keep_default_na=True
    )
    
    # Validate required columns
    validate_required_columns(df)
    
    # Process each row
    processed_rows = []
    for _, row in df.iterrows():
        processed_row = process_row(row)
        processed_rows.append(processed_row)
    
    # Create DataFrame from processed rows
    hubspot_df = pd.DataFrame(processed_rows)
    
    # Save to CSV with comma separator
    hubspot_df.to_csv(
        output_file, 
        index=False, 
        encoding='utf-8',
        sep=',',
        quoting=1  # Quote all fields
    )
    return hubspot_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform company data to Hubspot format')
    parser.add_argument('input_file', help='Path to input CSV file')
    parser.add_argument('output_file', help='Path to output CSV file')
    
    args = parser.parse_args()
    
    transformed_df = transform_to_hubspot_format(args.input_file, args.output_file)
    print(f"Transformed {len(transformed_df)} companies") 