
import ply.lex as lex

reserved = {
    'true':'TRUE',
    'false': 'FALSE',
    'nil': 'NIL',
    'def': 'DEFINE',
    'and': 'AND',
    'or': 'OR'
}

tokens = [
    "L_PAREN",
    "R_PAREN",
    "ASSIGN",
    "IDENTIFIER",
    "COMMENT",
    "INTEGER",
    "FLOAT",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE"
]

tokens += list(reserved.values())

t_ignore = ' \t\r\n'

t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_ASSIGN = r'='
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print("illegal character", t.value[0])
    print(t.value)
    t.lexer.skip(1)
    
lexer = lex.lex()





    
