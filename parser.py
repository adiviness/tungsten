
import ply.yacc as yacc
import sys

from scanner import tokens
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
    '''
    id_ = IDNode(p[1])
    type_  = TypeNode(p[2])
    p[0] = AssignNode([id_, type_, p[4]])

def p_expression(p):
    '''
    expression : val
    expression : expression binary_op val
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[2].children.append(p[1])
        p[1].parent = p[2]
        p[1].add_right_sibling(p[3])
        p[2].children.append(p[3])
        p[0] = p[2]


def p_binary_op(p):
    '''
    binary_op : PLUS
    '''
    if p[1] == '+':
        p[0] = PlusNode()
   
def p_val(p):
    '''
    val : INTEGER
        | FLOAT
        | IDENTIFIER
    '''

    if type(p[1]) == int:
        p[0] = IntNode(p[1])
    else:
        p[0] = IDNode(p[1])

def p_error(p):
    print("Parse Error at %s" % p.value, file=sys.stderr)
    exit(1)

def parse():
    parser = yacc.yacc()
    input_text = ''
    for line in sys.stdin:
        input_text += line
    root_node = parser.parse(input_text)
    return root_node
