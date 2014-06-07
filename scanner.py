
import ply.lex as lex

reserved = {
    'true':'TRUE',
    'false': 'FALSE',
    'nil': 'NIL',
    'def': 'DEFINE'
}

tokens = [
    "L_PAREN",
    "R_PAREN",
    "ASSIGN",
    "IDENTIFIER",
    "COMMENT",
    "INTEGER",
    "FLOAT"
]

tokens += list(reserved.values())

t_ignore = ' \t\r\n'

t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_ASSIGN = r'='
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_INTEGER = r'\d+'
t_FLOAT = r'\d+\.\d+'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print("illegal character", t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()





    
