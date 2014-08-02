
import sys
from parser.scope import *
from parser.nodes import *

class SymbolTable:

    def __init__(self):
        self.current_scope = None
        self.global_scope = GlobalScope()


    def harvest_symbols(self, node):
        self.current_scope = self.global_scope
        print("global scope")
        for child in node.children:
            self.traverse(child)
        print("closing global scope")

    def traverse(self, node):
        if type(node) == BlockNode:
            self.current_scope = LocalScope(self.current_scope)
            print("new local scope")
        elif type(node) == AssignNode:
            self.assign_node(node)
            print("adding symbol", node.children[0].data)
            return
        elif type(node) == IDNode:
            self.id_node(node)
            print("symbol %s referenced" % node.data)
            return
        elif type(node) == IntNode:
            return

        # check children
        for child in node.children:
            self.traverse(child)
        # close scope
        if self.current_scope != self.global_scope:
            self.current_scope = self.current_scope.parent
            print("closing local scope")


    def assign_node(self, node):
        if len(node.children) == 3:
            symbol = VariableSymbol(node.children[0].data, node.children[1].data)
            self.current_scope.define(symbol)
        else:
            self.id_node(node.children[0].data)
        for child in node.children[-1].children:
            self.traverse(child)

    def id_node(self, node):
        ref = self.current_scope.resolve(node.data)
        if ref == None:
            self.not_declared(node)

    def not_declared(self, name):
        print(name, "was not given a type before use", file=sys.stderr)
        exit(1)
            

