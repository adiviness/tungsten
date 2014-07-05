
#import ply.lex as lex
from enum import Enum
import re

INDENT_AMOUNT = 2

class TokenType(Enum):
    # language features
    COMMENT = 1
    INDENT = 2
    DEDENT = 3
    NEWLINE = 4
    # keywords
    TRUE = 5
    FALSE = 6
    NIL = 7
    DEF = 8
    AND = 9
    OR = 10
    NOT = 11 
    IF = 12
    ELIF = 13
    ELSE = 14
    # symbols
    COLON = 15
    L_PAREN = 16
    R_PAREN = 17
    ASSIGN = 18
    PLUS = 19
    MINUS = 20
    MULTIPLY = 21
    DIVIDE = 22
    # built ins
    IDENTIFIER = 23
    INTEGER = 24
    FLOAT = 25
    # whitespace
    IGNORE = 26

matchers = {
    TokenType.TRUE: r'true',
    TokenType.FALSE: r'false',
    TokenType.NIL: r'nil',
    TokenType.DEF: r'def',
    TokenType.AND: r'and',
    TokenType.OR: r'or',
    TokenType.NOT: r'not',
    TokenType.IF: r'if',
    TokenType.ELIF: r'elif',
    TokenType.ELSE: r'else',
    TokenType.COLON: r':',
    TokenType.L_PAREN: r'\(',
    TokenType.R_PAREN: r'\)',
    TokenType.ASSIGN: r'=',
    TokenType.IDENTIFIER: r'[a-zA-Z_][a-zA-Z0-9_]*',
    TokenType.COMMENT: r'#.*',
    TokenType.INTEGER: r'\d+',
    TokenType.FLOAT: r'\d+\.\d+',
    TokenType.PLUS: r'\+',
    TokenType.MINUS: r'\-',
    TokenType.MULTIPLY: r'\*',
    TokenType.DIVIDE: r'\/',
    TokenType.NEWLINE: r'\n',
    TokenType.IGNORE: r' '
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
            if tokenType in [TokenType.INDENT, TokenType.DEDENT]:
                continue
            self.matchers[tokenType] = re.compile("(%s)" % matchers[tokenType])

    def run(self):
        indent = re.compile("((?:  )*)")
        indent_level = 0
        while self.text != '':
            found_match = False
            for tokenType in TokenType:
                if tokenType in [TokenType.INDENT, TokenType.DEDENT]:
                    continue
                match = self.matchers[tokenType].match(self.text)
                if match != None:
                    self.tokens.append(Token(tokenType, match.group(0)))
                    self.text = self.text[len(match.group(0)):]
                    found_match = True
                    # check for INDENT or DEDENT
                    if tokenType == TokenType.NEWLINE:
                        match = indent.match(self.text)
                        new_indent_level = len(match.group(0)) / INDENT_AMOUNT
                        self.text = self.text[len(match.group(0)):]
                        while indent_level < new_indent_level:
                            self.tokens.append(Token(TokenType.INDENT, '  '))
                            indent_level += 1
                        while indent_level > new_indent_level:
                            self.tokens.append(Token(TokenType.DEDENT, '  '))
                            indent_level -= 1
                    break
            if not found_match:
                print("illegal character", text[0], file=sys.stderr)
                exit(1)

    def remove_ignore_tokens(self):
        self.tokens = list(filter(lambda x: x.kind != TokenType.IGNORE, self.tokens))
        




    
