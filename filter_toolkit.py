"""
filter_toolkit.py

A reusable library for filtering CSV rows based on complex logical conditions.
Supports operations like AND, OR, NOT, and various field operations (eq, ne, contains, regex, etc.).

Example usage:
    from filter_toolkit import AND, OR, NOT, eq, contains, regex, date_gt, custom, filter_row

    # Define the filter
    filter_obj = AND(
        {"field": "CORREIO_ELETRONICO", "op": "contains", "value": "@domain.com"},
        OR(
            {"field": "CNPJ_BASICO", "op": "regex", "value": r"^[0-9]{8}$"},
            NOT({"field": "SITUACAO_CADASTRAL", "op": "eq", "value": "ATIVA"})
        )
    )

    # Example row and columns
    row = ["12345678", "0001", "00", "1", "Company", "ATIVA", "2020-01-01", "", "", "", "2020-01-01", "1234", "", "Rua", "123", "", "Centro", "12345", "SP", "São Paulo", "11", "12345678", "", "", "", "", "email@domain.com", "", ""]
    columns = ["CNPJ_BASICO", "CNPJ_ORDEM", "CNPJ_DV", "IDENTIFICADOR_MATRIZ_FILIAL", "NOME_FANTASIA", "SITUACAO_CADASTRAL", "DATA_SITUACAO_CADASTRAL", "MOTIVO_SITUACAO_CADASTRAL", "NOME_CIDADE_EXTERIOR", "PAIS", "DATA_INICIO_ATIVIDADE", "CNAE_FISCAL_PRINCIPAL", "CNAE_FISCAL_SECUNDARIA", "TIPO_LOGRADOURO", "LOGRADOURO", "NUMERO", "COMPLEMENTO", "BAIRRO", "CEP", "UF", "MUNICIPIO", "DDD_1", "TELEFONE_1", "DDD_2", "TELEFONE_2", "DDD_FAX", "FAX", "CORREIO_ELETRONICO", "SITUACAO_ESPECIAL", "DATA_SITUACAO_ESPECIAL"]

    # Apply the filter
    result = filter_row(row, columns, filter_obj)
    print(result)  # True or False
"""

import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Union


def AND(*conditions: Dict[str, Any]) -> Dict[str, Any]:
    """
    Logical AND operation. Returns True if all conditions are True.

    Args:
        *conditions: Variable number of condition dictionaries.

    Returns:
        Dict[str, Any]: A dictionary representing the AND operation.
    """
    return {"op": "AND", "conditions": conditions}


def OR(*conditions: Dict[str, Any]) -> Dict[str, Any]:
    """
    Logical OR operation. Returns True if any condition is True.

    Args:
        *conditions: Variable number of condition dictionaries.

    Returns:
        Dict[str, Any]: A dictionary representing the OR operation.
    """
    return {"op": "OR", "conditions": conditions}


def NOT(condition: Dict[str, Any]) -> Dict[str, Any]:
    """
    Logical NOT operation. Returns True if the condition is False.

    Args:
        condition: A condition dictionary.

    Returns:
        Dict[str, Any]: A dictionary representing the NOT operation.
    """
    return {"op": "NOT", "condition": condition}


def eq(field: str, value: Any) -> Dict[str, Any]:
    """
    Equality operation. Returns True if the field value equals the specified value.

    Args:
        field: The field name.
        value: The value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the equality condition.
    """
    return {"field": field, "op": "eq", "value": value}


def ne(field: str, value: Any) -> Dict[str, Any]:
    """
    Not equal operation. Returns True if the field value does not equal the specified value.

    Args:
        field: The field name.
        value: The value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the not equal condition.
    """
    return {"field": field, "op": "ne", "value": value}


def contains(field: str, value: str) -> Dict[str, Any]:
    """
    Contains operation. Returns True if the field value contains the specified substring.

    Args:
        field: The field name.
        value: The substring to search for.

    Returns:
        Dict[str, Any]: A dictionary representing the contains condition.
    """
    return {"field": field, "op": "contains", "value": value}


def startswith(field: str, value: str) -> Dict[str, Any]:
    """
    Starts with operation. Returns True if the field value starts with the specified substring.

    Args:
        field: The field name.
        value: The substring to check.

    Returns:
        Dict[str, Any]: A dictionary representing the starts with condition.
    """
    return {"field": field, "op": "startswith", "value": value}


def endswith(field: str, value: str) -> Dict[str, Any]:
    """
    Ends with operation. Returns True if the field value ends with the specified substring.

    Args:
        field: The field name.
        value: The substring to check.

    Returns:
        Dict[str, Any]: A dictionary representing the ends with condition.
    """
    return {"field": field, "op": "endswith", "value": value}


def regex(field: str, value: str) -> Dict[str, Any]:
    """
    Regex operation. Returns True if the field value matches the specified regex pattern.

    Args:
        field: The field name.
        value: The regex pattern.

    Returns:
        Dict[str, Any]: A dictionary representing the regex condition.
    """
    return {"field": field, "op": "regex", "value": value}


def gt(field: str, value: Union[int, float]) -> Dict[str, Any]:
    """
    Greater than operation. Returns True if the field value is greater than the specified value.

    Args:
        field: The field name.
        value: The value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the greater than condition.
    """
    return {"field": field, "op": "gt", "value": value}


def lt(field: str, value: Union[int, float]) -> Dict[str, Any]:
    """
    Less than operation. Returns True if the field value is less than the specified value.

    Args:
        field: The field name.
        value: The value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the less than condition.
    """
    return {"field": field, "op": "lt", "value": value}


def ge(field: str, value: Union[int, float]) -> Dict[str, Any]:
    """
    Greater than or equal operation. Returns True if the field value is greater than or equal to the specified value.

    Args:
        field: The field name.
        value: The value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the greater than or equal condition.
    """
    return {"field": field, "op": "ge", "value": value}


def le(field: str, value: Union[int, float]) -> Dict[str, Any]:
    """
    Less than or equal operation. Returns True if the field value is less than or equal to the specified value.

    Args:
        field: The field name.
        value: The value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the less than or equal condition.
    """
    return {"field": field, "op": "le", "value": value}


def date_eq(field: str, value: str) -> Dict[str, Any]:
    """
    Date equality operation. Returns True if the field value equals the specified date.

    Args:
        field: The field name.
        value: The date string to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the date equality condition.
    """
    return {"field": field, "op": "date_eq", "value": value}


def date_ne(field: str, value: str) -> Dict[str, Any]:
    """
    Date not equal operation. Returns True if the field value does not equal the specified date.

    Args:
        field: The field name.
        value: The date string to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the date not equal condition.
    """
    return {"field": field, "op": "date_ne", "value": value}


def date_gt(field: str, value: str) -> Dict[str, Any]:
    """
    Date greater than operation. Returns True if the field value is greater than the specified date.

    Args:
        field: The field name.
        value: The date string to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the date greater than condition.
    """
    return {"field": field, "op": "date_gt", "value": value}


def date_lt(field: str, value: str) -> Dict[str, Any]:
    """
    Date less than operation. Returns True if the field value is less than the specified date.

    Args:
        field: The field name.
        value: The date string to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the date less than condition.
    """
    return {"field": field, "op": "date_lt", "value": value}


def date_ge(field: str, value: str) -> Dict[str, Any]:
    """
    Date greater than or equal operation. Returns True if the field value is greater than or equal to the specified date.

    Args:
        field: The field name.
        value: The date string to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the date greater than or equal condition.
    """
    return {"field": field, "op": "date_ge", "value": value}


def date_le(field: str, value: str) -> Dict[str, Any]:
    """
    Date less than or equal operation. Returns True if the field value is less than or equal to the specified date.

    Args:
        field: The field name.
        value: The date string to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the date less than or equal condition.
    """
    return {"field": field, "op": "date_le", "value": value}


def bool_eq(field: str, value: bool) -> Dict[str, Any]:
    """
    Boolean equality operation. Returns True if the field value equals the specified boolean.

    Args:
        field: The field name.
        value: The boolean value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the boolean equality condition.
    """
    return {"field": field, "op": "bool_eq", "value": value}


def bool_ne(field: str, value: bool) -> Dict[str, Any]:
    """
    Boolean not equal operation. Returns True if the field value does not equal the specified boolean.

    Args:
        field: The field name.
        value: The boolean value to compare against.

    Returns:
        Dict[str, Any]: A dictionary representing the boolean not equal condition.
    """
    return {"field": field, "op": "bool_ne", "value": value}


def custom(field: str, func: Callable[[Any], bool]) -> Dict[str, Any]:
    """
    Custom operation. Returns True if the custom function returns True for the field value.

    Args:
        field: The field name.
        func: A function that takes a value and returns a boolean.

    Returns:
        Dict[str, Any]: A dictionary representing the custom condition.
    """
    return {"field": field, "op": "custom", "value": func}


def filter_row(row: List[str], columns: List[str], filter_obj: Dict[str, Any]) -> bool:
    """
    Apply a filter object to a row of data.

    Args:
        row: List of values from the CSV row
        columns: List of column names
        filter_obj: Filter object defining the conditions

    Returns:
        bool: True if row matches filter conditions
    """
    def evaluate_condition(condition: Dict[str, Any]) -> bool:
        op = condition.get('op')
        if not op:
            return True

        if op == 'AND':
            return all(evaluate_condition(c) for c in condition.get('conditions', []))
        elif op == 'OR':
            return any(evaluate_condition(c) for c in condition.get('conditions', []))
        elif op == 'NOT':
            return not evaluate_condition(condition.get('condition', {}))
        elif op == 'contains':
            field = condition.get('field')
            value = condition.get('value')
            idx = columns.index(field)
            # Split field value by comma if it's CNAE_FISCAL_SECUNDARIA
            if field == 'CNAE_FISCAL_SECUNDARIA':
                field_values = [v.strip() for v in row[idx].split(',')]
                return any(value.lower() in v.lower() for v in field_values)
            return value.lower() in row[idx].lower()
        elif op == 'eq':
            field = condition.get('field')
            value = condition.get('value')
            idx = columns.index(field)
            # Split field value by comma if it's CNAE_FISCAL_SECUNDARIA
            if field == 'CNAE_FISCAL_SECUNDARIA':
                field_values = [v.strip() for v in row[idx].split(',')]
                return any(value.lower() == v.lower() for v in field_values)
            return row[idx].lower() == value.lower()
        elif op == 'ne':
            field = condition.get('field')
            value = condition.get('value')
            idx = columns.index(field)
            # Split field value by comma if it's CNAE_FISCAL_SECUNDARIA
            if field == 'CNAE_FISCAL_SECUNDARIA':
                field_values = [v.strip() for v in row[idx].split(',')]
                return all(value.lower() != v.lower() for v in field_values)
            return row[idx].lower() != value.lower()
        elif op == 'regex':
            field = condition.get('field')
            pattern = condition.get('value')
            idx = columns.index(field)
            # Split field value by comma if it's CNAE_FISCAL_SECUNDARIA
            if field == 'CNAE_FISCAL_SECUNDARIA':
                field_values = [v.strip() for v in row[idx].split(',')]
                return any(bool(re.search(pattern, v, re.IGNORECASE)) for v in field_values)
            return bool(re.search(pattern, row[idx], re.IGNORECASE))
        return False

    return evaluate_condition(filter_obj)

# Example usage:
if __name__ == "__main__":
    # Example filter object
    filter_example = {
        'op': 'and',
        'conditions': [
            {
                'op': 'equals',
                'column': 'CNAE_FISCAL_PRINCIPAL',
                'value': '6201500'
            },
            {
                'op': 'regex',
                'column': 'CNPJ_BASICO',
                'pattern': r'^[0-9]{8}$'
            }
        ]
    } 