
import sys

from scanner import Scanner, TokenType
from nodes import *

def parse():
    input_text = ''
    if len(sys.argv) > 1:
        fp = open(sys.argv[1], 'r')
        for line in fp:
            input_text += line
        fp.close()
    else:
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
        if self.tokens == []:
            return False
        return self.tokens[0].kind in tokenTypes

    def matchN(self, tokenType, n):
        if len(self.tokens) > n:
            return self.tokens[n].kind == tokenType
        return False

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
        #print(self.tokens[0])
        if self.match(TokenType.IF):
            node = self.if_()
        elif self.match(TokenType.WHILE):
            node = self.while_()
        elif self.match(TokenType.IDENTIFIER) and self.matchN(TokenType.L_PAREN, 1):
            node = self.function()
        elif self.match(TokenType.DEF):
            node = self.function_define()
        elif self.match(TokenType.RETURN):
            node = self.return_()
        else:
            node = self.declaration()
        # newline
        if self.match(TokenType.NEWLINE):
            self.consume(TokenType.NEWLINE)
            self.line_number += 1
        return node

    def if_(self):
        # if statement
        self.consume(TokenType.IF)
        node = IfNode()
        top_node = node
        exp_node = self.expression()
        self.consume(TokenType.COLON)
        self.consume(TokenType.NEWLINE)
        self.line_number += 1
        self.consume(TokenType.INDENT)
        block_node = self.block()
        self.consume(TokenType.DEDENT)
        node.give_child(exp_node)
        node.give_child(block_node)
        # possible elif statements
        while self.match(TokenType.ELIF):
            self.consume(TokenType.ELIF)
            elif_node = IfNode()
            exp_node = self.expression()
            self.consume(TokenType.COLON)
            self.consume(TokenType.NEWLINE)
            self.line_number += 1
            self.consume(TokenType.INDENT)
            block_node = self.block()
            self.consume(TokenType.DEDENT)
            elif_node.give_child(exp_node)
            elif_node.give_child(block_node)
            node.give_child(elif_node)
            node = elif_node
        # possible else statement
        if self.match(TokenType.ELSE):
            self.consume(TokenType.ELSE)
            self.consume(TokenType.COLON)
            self.consume(TokenType.NEWLINE)
            self.line_number += 1
            self.consume(TokenType.INDENT)
            block_node = self.block()
            self.consume(TokenType.DEDENT)
            node.give_child(block_node)
        return top_node

    def while_(self):
        # while statement
        self.consume(TokenType.WHILE)
        node = WhileNode()
        exp_node = self.expression()
        self.consume(TokenType.COLON)
        self.consume(TokenType.NEWLINE)
        self.line_number += 1
        self.consume(TokenType.INDENT)
        block_node = self.block()
        self.consume(TokenType.DEDENT)
        node.give_child(exp_node)
        node.give_child(block_node)
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
        # function
        if self.match(TokenType.IDENTIFIER) and self.matchN(TokenType.L_PAREN, 1):
            node = self.function()
        # val
        elif self.match(TokenType.INTEGER,
                      TokenType.FLOAT,
                      TokenType.TRUE,
                      TokenType.FALSE,
                      TokenType.STRING,
                      TokenType.IDENTIFIER):
            node = self.val()
        else: 
            node = self.unary_op()
            node.give_child(self.val())
        if self.match(TokenType.PLUS,
                      TokenType.MINUS,
                      TokenType.MULTIPLY,
                      TokenType.DIVIDE,
                      TokenType.MOD,
                      TokenType.EXPONENT,
                      TokenType.OR,
                      TokenType.AND,
                      TokenType.EQUAL,
                      TokenType.NOT_EQUAL,
                      TokenType.LESS_THAN,
                      TokenType.LESS_THAN_EQUAL,
                      TokenType.GREATER_THAN,
                      TokenType.GREATER_THAN_EQUAL):
            binary_op_node = self.binary_op()
            binary_op_node.give_child(node)
            exp_node = self.expression()
            binary_op_node.give_child(exp_node)
            return binary_op_node
        else:
            return node

    def function(self):
        node = CallNode()
        node.give_child(self.val())
        self.consume(TokenType.L_PAREN)
        if not self.match(TokenType.R_PAREN):
            args = self.arg_list()
            for arg_node in args:
                node.give_child(arg_node)
        self.consume(TokenType.R_PAREN)
        return node
            
    def arg_list(self):
        args = [self.expression()]
        while self.match(TokenType.COMMA):
            self.consume(TokenType.COMMA)
            args.append(self.expression())
        return args

    def function_define(self):
        self.consume(TokenType.DEF)
        node = DefNode()
        node.give_child(IDNode(self.consume(TokenType.IDENTIFIER).value))
        self.consume(TokenType.L_PAREN)
        if not self.match(TokenType.R_PAREN):
            param_nodes = self.param_list()
            for param_node in param_nodes:
                node.give_child(param_node)
        self.consume(TokenType.R_PAREN)
        node.give_child(IDNode(self.consume(TokenType.IDENTIFIER).value))
        self.consume(TokenType.COLON)
        self.consume(TokenType.NEWLINE)
        self.line_number += 1
        self.consume(TokenType.INDENT)
        node.give_child(self.block())
        self.consume(TokenType.DEDENT)
        return node

    def param_list(self):
        params = [IDNode(self.consume(TokenType.IDENTIFIER).value),
                  IDNode(self.consume(TokenType.IDENTIFIER).value)]
        while self.match(TokenType.COMMA):
            self.consume(TokenType.COMMA)
            params.append(IDNode(self.consume(TokenType.IDENTIFIER).value))
            params.append(IDNode(self.consume(TokenType.IDENTIFIER).value))
        return params
    def return_(self):
        node = ReturnNode()
        self.consume(TokenType.RETURN)
        node.give_child(self.expression())
        return node

    def val(self):
        #print(self.tokens[0])
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
        elif self.match(TokenType.STRING):
            token = self.consume(TokenType.STRING)
            return StringNode(token.value)
        elif self.match(TokenType.IDENTIFIER):
            token = self.consume(TokenType.IDENTIFIER)
            return IDNode(token.value)

    def unary_op(self):
        #print("unary_op", self.tokens[0])
        if self.match(TokenType.MINUS):
            token = self.consume(TokenType.MINUS)
            return MinusNode()
        elif self.match(TokenType.NOT):
            token = self.consume(TokenType.NOT)
            return NotNode()

    def binary_op(self):
        #print(self.tokens[0])
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
        elif self.match(TokenType.MOD):
            token = self.consume(TokenType.MOD)
            return ModNode()
        elif self.match(TokenType.EXPONENT):
            token = self.consume(TokenType.EXPONENT)
            return ExponentNode()
        elif self.match(TokenType.AND):
            token = self.consume(TokenType.AND)
            return AndNode()
        elif self.match(TokenType.OR):
            token = self.consume(TokenType.OR)
            return OrNode()
        elif self.match(TokenType.EQUAL):
            token = self.consume(TokenType.EQUAL)
            return EqualNode()
        elif self.match(TokenType.NOT_EQUAL):
            token = self.consume(TokenType.NOT_EQUAL)
            return NotEqualNode()
        elif self.match(TokenType.LESS_THAN):
            token = self.consume(TokenType.LESS_THAN)
            return LessThanNode()
        elif self.match(TokenType.LESS_THAN_EQUAL):
            token = self.consume(TokenType.LESS_THAN_EQUAL)
            return LessThanEqualNode()
        elif self.match(TokenType.GREATER_THAN):
            token = self.consume(TokenType.GREATER_THAN)
            return GreaterThanNode()
        elif self.match(TokenType.GREATER_THAN_EQUAL):
            token = self.consume(TokenType.GREATER_THAN_EQUAL)
            return GreaterThanEqualNode()
            
        
    







            
