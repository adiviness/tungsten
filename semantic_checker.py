
import sys

from symbol_table import SymbolTable
from type_tree import get_default_type_tree
from nodes import *

class SemanticChecker:
    '''scans ast for semantic errors'''

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.type_tree = get_default_type_tree()

    def build_symbol_table(self, node):
        if type(node) == BlockNode:
            self.symbol_table.open_scope()
        elif type(node) == AssignNode:
            # check if declared more than once
            if len(node.children) == 3:
                id_node = node.children[0]
                type_node = node.children[1]
                value_node = node.children[2]
                if self.symbol_table.declared_locally(id_node.data): 
                    print("Declared", id_node.data, "multiple times", file=sys.stderr)
                    exit(1)
                else:
                    value_type = self.get_type(value_node)
                    self.check_type(type_node.data, value_type)
                    self.symbol_table.enter_symbol(id_node.data, type_node.data, value_node) #TODO not sure what to do with value
                    print("added symbol", id_node.data)
            # assignment doesn't have a type specified
            else:
                id_node = node.children[0]
                if self.symbol_table.retrieve_symbol(id_node.data) == None:
                    print("Must declare type for", id_node.data, file=sys.stderr)
                    exit(1)
                type_ = self.symbol_table.get_type(id_node.data)
                value_node = node.children[1]
                value_type = self.get_type(value_node)
                self.check_type(type_, value_type)
                self.symbol_table.enter_symbol(id_node.data, type_, value_node)
        elif type(node) == IDNode:
            symbol = self.symbol_table.retrieve_symbol(node.data)
            if symbol == None:
                print("Undeclared identifier", node.data, file=sys.stderr)
                exit(1)

        for child in node.children:
            self.build_symbol_table(child)

        if type(node) == BlockNode:
            self.symbol_table.close_scope()
            

    def get_type(self, node):        
        if type(node) == IDNode:
            return self.symbol_table.get_type(node.data)
        elif type(node) == IntNode:
            return "Int"
        elif type(node) in [PlusNode, MinusNode, MultiplyNode, DivideNode]:
            left = self.get_type(node.children[0])
            right = self.get_type(node.children[1])
            if left == right:
                return left
            elif self.type_tree.have_relation(left, right):
                return type_tree.generalize(left, right)
            else:
                print("Type error! cannot convert %s to %s" % (right, left), file=sys.stderr)
                exit(1)

    def check_type(self, one, two):
        if one == two:
            return
        if not self.type_tree.have_relation(one, two):
            print("Type error! %s has no relation to %s" % (two, one), file=sys.stderr)
            exit(1)
        generalized = self.type_tree.generalize(one, two)
        if generalized != one:
            print("Cannot cast %s to %s" % (two, one), file=sys.stderr)
            exit(1)
                
            
