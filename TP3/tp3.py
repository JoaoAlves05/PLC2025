import ply.lex as lex
import sys
import re

# Tokens
tokens = [
    'VARIABLE', # Variável
    'PREFIXED_NAME', # Nome com prefixo
    'STRING', # String
    'NUMBER', # Número
    'BRACE_OPEN', # Chave de abertura
    'BRACE_CLOSE', # Chave de fechamento
    'DOT', # Ponto
    'SELECT', # Selecionar
    'WHERE', # Onde
    'LIMIT', # Limitar
    'A', # palavra-chave 'a'
]

# Expressões regulares

t_BRACE_OPEN    = r'\{' # Chaveta de abertura
t_BRACE_CLOSE   = r'\}' # Chave de fechamento
t_DOT           = r'\.' # Ponto
t_VARIABLE      = r'\?[a-zA-Z_][a-zA-Z0-9_]*' # Variável
t_PREFIXED_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z_][a-zA-Z0-9_]*' # Nome com prefixo
t_STRING        = r'"([^"\\]|\\.)*"(?:@[a-zA-Z]+)?' # String
t_NUMBER        = r'\d+' # Número
t_ignore        = ' \t' # Ignorar espaços e tabs

# Comentários
def t_COMMENT(t):
    r'\#.*'
    pass

# Palavras-chave case-insensitive
def t_KEYWORD(t):
    r'\b(select|where|limit|a)\b'
    t.type = t.value.upper()
    return t

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro
def t_error(t):
    print(f"ERRO: Caracter ilegal {t.value[0]!r} na linha {t.lexer.lineno}", file=sys.stderr)
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex(reflags=re.IGNORECASE)

# Ler do stdin
input_text = sys.stdin.read()
lexer.input(input_text)

# Iterar sobre tokens e imprimir
for tok in lexer:
    print((tok.type, tok.value))
