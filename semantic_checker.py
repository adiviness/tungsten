
import sys

from symbol_table import SymbolTable
from nodes import *

class SemanticChecker:
    '''scans ast for semantic errors'''

    def __init__(self):
        self.symbol_table = SymbolTable()

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
                    self.symbol_table.enter_symbol(id_node.data, type_node.data, value_node) #TODO not sure what to do with value
                    print("added symbol", id_node.data)
            else:
                id_node = node.children[0]
                if self.symbol_table.retrieve_symbol(id_node.data) == None:
                    print("Must declare type for", id_node.data, file=sys.stderr)
                    exit(1)
                type_ = self.symbol_table.get_type(id_node.data)
                value_node = node.children[1]
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
            


    def type_check_tree(self, root):
        NotImplemented
        
