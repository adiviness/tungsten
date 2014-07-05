
import sys

from scanner import Scanner, TokenType
from nodes import *

def parse():
    input_text = ''
    for line in sys.stdin:
        input_text += line
    scanner = Scanner(input_text)
    scanner.run()
    scanner.remove_ignore_tokens()
    parser = Parser()
    parser.parse(scanner.tokens)
    return parser.root_node

class Parser:
    '''recursive descent parser'''

    def __init__(self):
        self.tokens = None
        self.root_node = None
        self.line_number = 1

    def match(self, *tokenTypes):
        return self.tokens[0].kind in tokenTypes

    def consume(self, tokenType):
        if tokenType != self.tokens[0].kind:
            self.error(tokenType)
        return self.pop_token()

    def pop_token(self):
        token = self.tokens[0]
        self.tokens = self.tokens[1:]
        return token 

    def error(self, tokenType):
            print("parse error on line %d" % self.line_number, file=sys.stderr)
            print("expected", tokenType, "but received", self.tokens[0].kind, "with value:", self.tokens[0].value, file=sys.stderr)
            exit(1)

    def parse(self, tokens):
        self.line_number = 1 # reset line number
        self.tokens = tokens
        self.root_node = self.block()

    def block(self):
        block_node = BlockNode()
        for node in self.statements():
            block_node.give_child(node)
        return block_node
        
    def statements(self):
        statement_nodes = []
        while True:
            while self.tokens != [] and self.match(TokenType.NEWLINE):
                self.consume(TokenType.NEWLINE)
                self.line_number += 1
            if self.tokens == []:
                break
            if self.match(TokenType.DEDENT):
                break
            statement_nodes.append(self.statement())
        return statement_nodes

    def statement(self):
        print(self.tokens[0])
        if self.match(TokenType.IF):
            self.consume(TokenType.IF)
            node = IfNode()
            exp_node = self.expression()
            self.consume(TokenType.COLON)
            self.consume(TokenType.NEWLINE)
            self.line_number += 1
            self.consume(TokenType.INDENT)
            block_node = self.block()
            self.consume(TokenType.DEDENT)
            node.give_child(exp_node)
            node.give_child(block_node)
        else:
            node = self.declaration()
        # newline
        if self.match(TokenType.NEWLINE):
            self.consume(TokenType.NEWLINE)
            self.line_number += 1
        return node
        
    def declaration(self):
        var_name_node = IDNode(self.consume(TokenType.IDENTIFIER).value)
        assign_node = AssignNode()
        assign_node.give_child(var_name_node)
        if self.match(TokenType.ASSIGN):
            self.consume(TokenType.ASSIGN)
        else:
            type_name_node = IDNode(self.consume(TokenType.IDENTIFIER).value)
            assign_node.give_child(type_name_node)
            self.consume(TokenType.ASSIGN)
        assign_node.give_child(self.expression())
        return assign_node

    def expression(self):
        if self.match(TokenType.INTEGER,
                      TokenType.FLOAT,
                      TokenType.TRUE,
                      TokenType.FALSE,
                      TokenType.IDENTIFIER):
            node = self.val()
        else: 
            node = self.unary_op()
            node.give_child(self.val())
        if self.match(TokenType.PLUS,
                      TokenType.MINUS,
                      TokenType.MULTIPLY,
                      TokenType.DIVIDE,
                      TokenType.OR,
                      TokenType.AND):
            binary_op_node = self.binary_op()
            binary_op_node.give_child(node)
            exp_node = self.expression()
            binary_op_node.give_child(exp_node)
            return binary_op_node
        else:
            return node

    def val(self):
        print(self.tokens[0])
        if self.match(TokenType.INTEGER):
            token = self.consume(TokenType.INTEGER)
            return IntNode(token.value)
        elif self.match(TokenType.FLOAT):
            token = self.consume(TokenType.FLOAT)
            return FloatNode(token.value)
        elif self.match(TokenType.TRUE):
            token = self.consume(TokenType.TRUE)
            return BoolNode(token.value)
        elif self.match(TokenType.FALSE):
            token = self.consume(TokenType.FALSE)
            return BoolNode(token.value)
        elif self.match(TokenType.IDENTIFIER):
            token = self.consume(TokenType.IDENTIFIER)
            return IDNode(token.value)

    def unary_op(self):
        print("unary_op", self.tokens[0])
        if self.match(TokenType.MINUS):
            token = self.consume(TokenType.MINUS)
            return MinusNode()
        elif self.match(TokenType.NOT):
            token = self.consume(TokenType.NOT)
            return NotNode()

    def binary_op(self):
        print(self.tokens[0])
        if self.match(TokenType.PLUS):
            token = self.consume(TokenType.PLUS)
            return PlusNode()
        elif self.match(TokenType.MINUS):
            token = self.consume(TokenType.MINUS)
            return MinusNode()
        elif self.match(TokenType.MULTIPLY):
            token = self.consume(TokenType.MULTIPLY)
            return MultiplyNode()
        elif self.match(TokenType.DIVIDE):
            token = self.consume(TokenType.DIVIDE)
            return DivideNode()
        elif self.match(TokenType.AND):
            token = self.consume(TokenType.AND)
            return AndNode()
        
    







            
