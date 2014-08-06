
from enum import Enum
import re, sys

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
    WHILE = 15
    FOR = 16
    CLASS = 17
    STATIC = 18
    INSTANCE = 19
    IN = 20
    BREAK = 21
    CONTINUE = 22
    RETURN = 23
    # symbols
    COLON = 24
    COMMA = 25
    L_PAREN = 26
    R_PAREN = 27
    L_BRACKET = 28
    R_BRACKET = 29
    L_BRACE = 30
    R_BRACE = 31
    EXPONENT = 32
    PLUS = 33
    MINUS = 34
    MULTIPLY = 35
    DIVIDE = 36
    MOD = 37
    EQUAL = 38
    NOT_EQUAL = 39
    LESS_THAN_EQUAL = 40
    GREATER_THAN_EQUAL = 41
    LESS_THAN = 42
    GREATER_THAN = 43
    ASSIGN = 44
    CLASS_VAR = 45
    INSTANCE_VAR = 46
    ATTRIBUTE_ACCESSOR = 47
    # built ins
    IDENTIFIER = 48
    INTEGER = 49
    FLOAT = 50
    STRING = 51
    # whitespace
    IGNORE = 52

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
    TokenType.IGNORE: r' ',
    TokenType.EQUAL: r'==', 
    TokenType.NOT_EQUAL: r'!=', 
    TokenType.LESS_THAN: r'<', 
    TokenType.LESS_THAN_EQUAL: r'<=', 
    TokenType.GREATER_THAN: r'>', 
    TokenType.GREATER_THAN_EQUAL: r'>=',
    TokenType.WHILE: r'while', 
    TokenType.FOR: r'for', 
    TokenType.CLASS: r'class', 
    TokenType.STATIC: r'static', 
    TokenType.INSTANCE: r'instance', 
    TokenType.IN: r'in', 
    TokenType.BREAK: r'break', 
    TokenType.CONTINUE: r'continue', 
    TokenType.L_BRACKET: r'\[', 
    TokenType.R_BRACKET: r'\]', 
    TokenType.L_BRACE: r'\{', 
    TokenType.R_BRACE: r'\}', 
    TokenType.EXPONENT: r'\*\*', 
    TokenType.MOD: r'%',
    TokenType.RETURN: r'return',
    TokenType.COMMA: r'\,',
    TokenType.STRING: r'".*?"',
    TokenType.CLASS_VAR: r'@@',
    TokenType.INSTANCE_VAR: r'@',
    TokenType.ATTRIBUTE_ACCESSOR: r'\.'
}

class Token():

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        if self.value == '\n':
            return "(%s, \\n)" % str(self.kind)
        return "(%s, %s)" % (str(self.kind), self.value)

class IllegalCharacterException(Exception):

    def __init__(self, value):
        self.value = value

class Scanner():

    def __init__(self):
        self.text = None
        self.tokens = []
        self.matchers = {}
        self.indent_level = 0
        for tokenType in TokenType:
            if tokenType in [TokenType.INDENT, TokenType.DEDENT]:
                continue
            self.matchers[tokenType] = re.compile("(%s)" % matchers[tokenType])

    # TODO refactor into multiple functions for better readibility
    # should count line numbers
    def scan(self, text):
        self.text = text
        self.tokens = []
        self.indent_level = 0
        while self.text != '':
            found_match = False
            for tokenType in TokenType:
                if tokenType in [TokenType.INDENT, TokenType.DEDENT]:
                    continue
                match = self.matchers[tokenType].match(self.text)
                if match != None:
                    found_match = True
                    self._add_token(tokenType, match.group(0))
                    if tokenType == TokenType.COMMENT:
                        self.tokens[-1] = Token(TokenType.COMMENT, "\n")
                    # check for INDENT or DEDENT
                    self._check_new_indentation(tokenType)
                    break
            if not found_match:
                raise IllegalCharacterException(self.text[0])
        self._remove_ignore_tokens()

    def _add_token(self, token_type, text):
        self.tokens.append(Token(token_type, text))
        self.text = self.text[len(text):]

    def _check_new_indentation(self, tokenType):
        indent_regex = re.compile("((?:  )*)")
        if tokenType == TokenType.NEWLINE: 
            match = indent_regex.match(self.text)
            new_indent_level = len(match.group(0)) / INDENT_AMOUNT
            self.text = self.text[len(match.group(0)):]
            while self.indent_level < new_indent_level:
                self.tokens.append(Token(TokenType.INDENT, '  '))
                self.indent_level += 1
            while self.indent_level > new_indent_level:
                self.tokens.append(Token(TokenType.DEDENT, '  '))
                self.indent_level -= 1

    def _remove_ignore_tokens(self):
        self.tokens = list(filter(lambda x: x.kind not in [TokenType.IGNORE, TokenType.COMMENT], self.tokens))

        
        




    
