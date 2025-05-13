from filter_toolkit import (
    AND, OR, NOT, eq, ne, contains, startswith, endswith,
    regex, gt, lt, ge, le, date_eq, date_ne, date_gt,
    date_lt, date_ge, date_le, bool_eq, bool_ne, custom
)

# CSV header
columns = [
    "CNPJ_BASICO", "CNPJ_ORDEM", "CNPJ_DV", "IDENTIFICADOR_MATRIZ_FILIAL", "NOME_FANTASIA",
    "SITUACAO_CADASTRAL", "DATA_SITUACAO_CADASTRAL", "MOTIVO_SITUACAO_CADASTRAL", "NOME_CIDADE_EXTERIOR",
    "PAIS", "DATA_INICIO_ATIVIDADE", "CNAE_FISCAL_PRINCIPAL", "CNAE_FISCAL_SECUNDARIA", "TIPO_LOGRADOURO",
    "LOGRADOURO", "NUMERO", "COMPLEMENTO", "BAIRRO", "CEP", "UF", "MUNICIPIO", "DDD_1", "TELEFONE_1",
    "DDD_2", "TELEFONE_2", "DDD_FAX", "FAX", "CORREIO_ELETRONICO", "SITUACAO_ESPECIAL", "DATA_SITUACAO_ESPECIAL"
]

# Define the filter
filter_obj = AND(
    OR(
        contains("CNAE_FISCAL_PRINCIPAL", "7911200"),
        contains("CNAE_FISCAL_PRINCIPAL", "7912100"),
        contains("CNAE_FISCAL_PRINCIPAL", "7990200"),
        #contains("CNAE_FISCAL_SECUNDARIA", "7911200"),
        #contains("CNAE_FISCAL_SECUNDARIA", "7912900"),
        #contains("CNAE_FISCAL_SECUNDARIA", "7990200")
    ),
        NOT(
        OR(
            contains("CORREIO_ELETRONICO", "@gmail"),
            contains("CORREIO_ELETRONICO", "@gamil"),
            contains("CORREIO_ELETRONICO", "@hotmail"),
            contains("CORREIO_ELETRONICO", "@yahoo"),
            contains("CORREIO_ELETRONICO", "@icloud"),
            contains("CORREIO_ELETRONICO", "@outlook"),
            contains("CORREIO_ELETRONICO", "@live"),
            contains("CORREIO_ELETRONICO", "@msn"),
            contains("CORREIO_ELETRONICO", "@aol"),
            contains("CORREIO_ELETRONICO", "@protonmail"),
            contains("CORREIO_ELETRONICO", "@zoho"),
            contains("CORREIO_ELETRONICO", "@mail"),
            contains("CORREIO_ELETRONICO", "@me"),
            contains("CORREIO_ELETRONICO", "@mac"),
            contains("CORREIO_ELETRONICO", "@rocketmail"),
            contains("CORREIO_ELETRONICO", "@bol.com.br"),
            contains("CORREIO_ELETRONICO", "@terra.com.br"),
            contains("CORREIO_ELETRONICO", "@ig.com.br"),
            contains("CORREIO_ELETRONICO", "@uol.com.br"),
            contains("CORREIO_ELETRONICO", "@yahoo.com.br"),
            contains("CORREIO_ELETRONICO", "@hotmail.com.br"),
            contains("CORREIO_ELETRONICO", "@gmail.com"),
            contains("CORREIO_ELETRONICO", "@ymail")
        )
    ),
    contains("SITUACAO_CADASTRAL", "02"),
    ne("NOME_FANTASIA", ""),
    eq("UF", "MG"),
    OR(
        ne("TELEFONE_1", ""),
        ne("TELEFONE_2", "")
    )
)

"""     NOT(
        OR(
            contains("CORREIO_ELETRONICO", "@gmail"),
            contains("CORREIO_ELETRONICO", "@hotmail"),
            contains("CORREIO_ELETRONICO", "@yahoo"),
            contains("CORREIO_ELETRONICO", "@icloud"),
            contains("CORREIO_ELETRONICO", "@outlook"),
            contains("CORREIO_ELETRONICO", "@live"),
            contains("CORREIO_ELETRONICO", "@msn"),
            contains("CORREIO_ELETRONICO", "@aol"),
            contains("CORREIO_ELETRONICO", "@protonmail"),
            contains("CORREIO_ELETRONICO", "@zoho"),
            contains("CORREIO_ELETRONICO", "@mail"),
            contains("CORREIO_ELETRONICO", "@me"),
            contains("CORREIO_ELETRONICO", "@mac"),
            contains("CORREIO_ELETRONICO", "@rocketmail"),
            contains("CORREIO_ELETRONICO", "@bol.com.br"),
            contains("CORREIO_ELETRONICO", "@terra.com.br"),
            contains("CORREIO_ELETRONICO", "@ig.com.br"),
            contains("CORREIO_ELETRONICO", "@uol.com.br"),
            contains("CORREIO_ELETRONICO", "@yahoo.com.br"),
            contains("CORREIO_ELETRONICO", "@hotmail.com.br"),
            contains("CORREIO_ELETRONICO", "@gmail.com.br"),
            contains("CORREIO_ELETRONICO", "@ymail")
        )
    ), """