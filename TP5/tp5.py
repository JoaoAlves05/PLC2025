import sys
import ply.lex as lex

# Analisador Léxico

tokens = (
    'NUM', 'MAIS', 'MENOS', 'VEZES', 'DIVIDIR', 'APAR', 'FPAR'
    )

t_MAIS     = r'\+'
t_MENOS    = r'-'
t_VEZES    = r'\*'
t_DIVIDIR  = r'/'
t_APAR     = r'\('
t_FPAR     = r'\)'

t_ignore = '\t '

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere desconhecido: {t.value[0]} (linha {t.lexer.lineno})")
    t.lexer.skip(1)

lexer = lex.lex()

# Analisador Sintático

# -------------------------------------------------------
# Gramática:
# Expr  → Termo OprSomSub
# OprSomSub  → (+|-) Termo OprSomSub | ε
# Termo      → Fator OprMultDiv
# OprMultDiv → (*|/) Fator OprMultDiv | ε
# Fator      → NUM | '(' Expr ')'
# -------------------------------------------------------

prox_simb = None

def erro_sintatico(simb):
    print("Erro sintático: token inesperado", simb)

def consome(simb):
    """Consome o token esperado"""
    global prox_simb
    if prox_simb and prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        erro_sintatico(prox_simb)

def rec_Fator():
    global prox_simb
    if prox_simb is None:
        erro_sintatico(prox_simb)
    elif prox_simb.type == 'NUM':
        print("Derivando por Fator → NUM")
        consome('NUM')
        print("Reconheci Fator → NUM")
    elif prox_simb.type == 'APAR':
        print("Derivando por Fator → ( Expressao )")
        consome('APAR')
        rec_Expressao()
        consome('FPAR')
        print("Reconheci Fator → ( Expressao )")
    else:
        erro_sintatico(prox_simb)

def rec_OprMultDiv():
    global prox_simb
    if prox_simb and prox_simb.type == 'VEZES':
        print("Derivando por OprMultDiv → * Fator OprMultDiv")
        consome('VEZES')
        rec_Fator()
        rec_OprMultDiv()
        print("Reconheci OprMultDiv → * Fator OprMultDiv")
    elif prox_simb and prox_simb.type == 'DIVIDIR':
        print("Derivando por OprMultDiv → / Fator OprMultDiv")
        consome('DIVIDIR')
        rec_Fator()
        rec_OprMultDiv()
        print("Reconheci OprMultDiv → / Fator OprMultDiv")
    else:
        print("Derivando por OprMultDiv → ε")
        print("Reconheci OprMultDiv → ε")

def rec_Termo():
    print("Derivando por Termo → Fator OprMultDiv")
    rec_Fator()
    rec_OprMultDiv()
    print("Reconheci Termo → Fator OprMultDiv")

def rec_OprSomSub():
    global prox_simb
    if prox_simb and prox_simb.type == 'MAIS':
        print("Derivando por OprSomSub → + Termo OprSomSub")
        consome('MAIS')
        rec_Termo()
        rec_OprSomSub()
        print("Reconheci OprSomSub → + Termo OprSomSub")
    elif prox_simb and prox_simb.type == 'MENOS':
        print("Derivando por OprSomSub → - Termo OprSomSub")
        consome('MENOS')
        rec_Termo()
        rec_OprSomSub()
        print("Reconheci OprSomSub → - Termo OprSomSub")
    else:
        print("Derivando por OprSomSub → ε")
        print("Reconheci OprSomSub → ε")

def rec_Expressao():
    print("Derivando por Expressao → Termo OprSomSub")
    rec_Termo()
    rec_OprSomSub()
    print("Reconheci Expressao → Termo OprSomSub")

def rec_Parser(texto):
    global prox_simb
    lexer.input(texto)
    prox_simb = lexer.token()
    rec_Expressao()
    if prox_simb is not None:
        print("Tokens não consumidos ->", prox_simb)
    print("That's all folks!")

if __name__ == "__main__":
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha:
            continue
        print(f"\n>>> Expressão: {linha}")
        rec_Parser(linha)

