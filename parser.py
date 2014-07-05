
import sys

from scanner import Scanner
from nodes import *

def p_start(p):
    '''
    start : block
    '''
    p[0] = p[1]

def p_block(p):
    '''
    block : statements 
    '''
    p[0] = BlockNode()
    node = p[1]
    while node != None:
        p[0].children.append(node)
        node.parent = p[0]
        node = node.right_sibling

def p_statements(p):
    '''
    statements : statement statements
    statements :
    '''
    if len(p) == 3:
        if p[2] != None:
            p[1].add_right_sibling(p[2])
        p[0] = p[1]

def p_statement(p):
    '''
    statement : declaration
    '''
    p[0] = p[1]

def p_declaration(p):
    '''
    declaration : IDENTIFIER IDENTIFIER ASSIGN expression
        | IDENTIFIER ASSIGN expression
    '''
    if len(p) == 5:
        id_ = IDNode(p[1])
        type_  = TypeNode(p[2])
        p[0] = AssignNode([id_, type_, p[4]])
    elif len(p) == 4:
        id_ = IDNode(p[1])
        p[0] = AssignNode([id_, p[3]])

def p_expression(p):
    '''
    expression : val
    expression : expression binary_op val
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        print(p)
        p[2].children.append(p[1])
        p[1].parent = p[2]
        p[1].add_right_sibling(p[3])
        p[2].children.append(p[3])
        p[0] = p[2]
    else:
        print("error: bad expression")
        exit(1)


def p_binary_op(p):
    '''
    binary_op : PLUS
        | MINUS
        | MULTIPLY
        | DIVIDE
        | AND
        | OR
    '''
    print(p[1])
    if p[1] == '+':
        p[0] = PlusNode()

    elif p[1] == '-':
        p[0] = MinusNode()

    elif p[1] == '*':
        p[0] = MultiplyNode()

    elif p[1] == '/':
        p[0] = DivideNode()

    elif p[1] == 'and':
        print("here and")
        p[0] = AndNode()

    elif p[1] == 'or':
        p[0] = OrNode()
    else:
        print("error: no binary op found", file=sys.stderr)
        exit(1)
   
def p_val(p):
    '''
    val : INTEGER
        | FLOAT
        | TRUE
        | FALSE
        | IDENTIFIER
    '''

    print(p[1])
    if type(p[1]) == int:
        p[0] = IntNode(p[1])

    elif type(p[1]) == float:
        p[0] = FloatNode(p[1])

    elif p[1] == 'true':
        print("here true")
        p[0] = BoolNode(True)

    elif p[1] == 'false':
        p[0] = BoolNode(False)

    else:
        p[0] = IDNode(p[1])

def p_error(p):
    print("Parse Error at %s" % p.value, file=sys.stderr)
    exit(1)

def parse():
    #parser = yacc.yacc()
    input_text = ''
    for line in sys.stdin:
        input_text += line
    #root_node = parser.parse(input_text)
    #return root_node
    scanner = Scanner(input_text)
    scanner.run()
    exit(0)

class Parser:
    '''recursive descent parser'''

    def __init__(self):
        self.root_node = None
        self.tokens = None

    def parse(self, tokens):
        self.tokens = tokens
        self.root_node = BlockNode()
        self.statements()

    def statements(self):
        while self.tokens != []:
            self.statement()

    def statement(self):
        self.declaration()

    def declaration(self):
        NotImplemented
    
