
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
   '''
   p[0] = p[1]
   
def p_val(p):
    '''
    val : INTEGER
        | FLOAT
    '''
    if type(p[1]) == int:
        p[0] = IntNode(p[1])
    else:
        print("error", type(p[1]))


def parse():
    parser = yacc.yacc()
    input_text = ''
    for line in sys.stdin:
        input_text += line
    root_node = parser.parse(input_text)
    return root_node
