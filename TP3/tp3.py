import ply.lex as lex
import sys

# Lista de tokens
tokens = [
    'VARIABLE',
    'PREFIXED_NAME',
    'STRING',
    'NUMBER',
    'BRACE_OPEN',
    'BRACE_CLOSE',
    'DOT',
]

# Palavras-chave reservadas
reserved = {
    'select': 'SELECT',
    'where': 'WHERE',
    'limit': 'LIMIT',
    'a': 'A',
}

tokens += list(reserved.values())

# Regras de tokens
t_BRACE_OPEN  = r'\{'
t_BRACE_CLOSE = r'\}'
t_DOT         = r'\.'
t_VARIABLE    = r'\?[a-zA-Z_][a-zA-Z0-9_]*'
t_PREFIXED_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING      = r'"([^"\\]|\\.)*"(?:@[a-zA-Z]+)?'
t_NUMBER      = r'\d+'

# Ignorar espaços e tabs
t_ignore = ' \t'

# Comentários
def t_COMMENT(t):
    r'\#.*'
    pass  # ignora

# Detectar palavras-chave
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'PREFIXED_NAME')  # verifica se é keyword
    return t

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro
def t_error(t):
    print(f"Caracter ilegal: {t.value[0]!r} na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

# Teste
query = '''
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
 ?s a dbo:MusicalArtist .
 ?s foaf:name "Chuck Berry"@en .
 ?w dbo:artist ?s .
 ?w foaf:name ?nome .
 ?w dbo:abstract ?desc
} LIMIT 1000
'''

lexer.input(query)

for tok in lexer:
    print(tok)
