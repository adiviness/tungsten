
#import ply.lex as lex
from enum import Enum
import re



t_ignore = ' \t\r\n'


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
    
#lexer = lex.lex()


class TokenTypes(Enum):
    TRUE = 1
    FALSE = 2
    NIL = 3
    DEF = 4
    AND = 5
    OR = 6
    L_PAREN = 7
    R_PAREN = 8
    ASSIGN = 9
    IDENTIFIER = 10
    COMMENT = 11
    INTEGER = 12
    FLOAT = 13
    PLUS = 14
    MINUS = 15
    MULTIPLY = 16
    DIVIDE = 17
    NEWLINE = 18
    IGNORE = 19

matchers = {
    TokenTypes.TRUE : r'true',
    TokenTypes.FALSE : r'false',
    TokenTypes.NIL : r'nil',
    TokenTypes.DEF : r'def',
    TokenTypes.AND : r'and',
    TokenTypes.OR : r'or',
    TokenTypes.L_PAREN : r'\(',
    TokenTypes.R_PAREN : r'\)',
    TokenTypes.ASSIGN : r'=',
    TokenTypes.IDENTIFIER : r'[a-zA-Z_][a-zA-Z0-9_]*',
    TokenTypes.COMMENT : r'#.*',
    TokenTypes.INTEGER : r'\d+',
    TokenTypes.FLOAT : r'\d+\.\d+',
    TokenTypes.PLUS : r'\+',
    TokenTypes.MINUS : r'\-',
    TokenTypes.MULTIPLY : r'\*',
    TokenTypes.DIVIDE : r'\/',
    TokenTypes.NEWLINE : r'\n',
    TokenTypes.IGNORE : r' '
}

class Token():

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return "(%s, %s)" % (str(self.kind), self.value)


class Scanner():

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.matchers = {}
        for tokenType in TokenTypes:
            self.matchers[tokenType] = re.compile("(%s)" % matchers[tokenType])

    def run(self):
        while self.text != '':
            for tokenType in TokenTypes:
                match = self.matchers[tokenType].match(self.text)
                if match != None:
                    self.tokens.append(Token(tokenType, match.group(0)))
                    self.text = self.text[len(match.group(0)):]
                    break
        print(self.tokens)
        




    
