
#import ply.lex as lex
from enum import Enum
import re

class TokenType(Enum):
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
    NOT = 20

matchers = {
    TokenType.TRUE : r'true',
    TokenType.FALSE : r'false',
    TokenType.NIL : r'nil',
    TokenType.DEF : r'def',
    TokenType.AND : r'and',
    TokenType.OR : r'or',
    TokenType.NOT : r'not',
    TokenType.L_PAREN : r'\(',
    TokenType.R_PAREN : r'\)',
    TokenType.ASSIGN : r'=',
    TokenType.IDENTIFIER : r'[a-zA-Z_][a-zA-Z0-9_]*',
    TokenType.COMMENT : r'#.*',
    TokenType.INTEGER : r'\d+',
    TokenType.FLOAT : r'\d+\.\d+',
    TokenType.PLUS : r'\+',
    TokenType.MINUS : r'\-',
    TokenType.MULTIPLY : r'\*',
    TokenType.DIVIDE : r'\/',
    TokenType.NEWLINE : r'\n',
    TokenType.IGNORE : r' '
}

class Token():

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        if self.value == '\n':
            return "(%s, \\n)" % str(self.kind)
        return "(%s, %s)" % (str(self.kind), self.value)


class Scanner():

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.matchers = {}
        for tokenType in TokenType:
            self.matchers[tokenType] = re.compile("(%s)" % matchers[tokenType])

    def run(self):
        while self.text != '':
            found_match = False
            for tokenType in TokenType:
                match = self.matchers[tokenType].match(self.text)
                if match != None:
                    self.tokens.append(Token(tokenType, match.group(0)))
                    self.text = self.text[len(match.group(0)):]
                    found_match = True
                    break
            if not found_match:
                print("illegal character", text[0], file=sys.stderr)
                exit(1)

    def remove_ignore_tokens(self):
        self.tokens = list(filter(lambda x: x.kind != TokenType.IGNORE, self.tokens))
        




    
