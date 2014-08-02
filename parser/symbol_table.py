
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
            self.block_node(node)
        elif type(node) == AssignNode:
            self.assign_node(node)
            print("adding symbol", node.children[0].data)
        elif type(node) == IDNode:
            self.id_node(node)
        elif type(node) == IntNode:
            pass
        elif type(node) == DefNode:
            self.def_node(node)
        elif type(node) == ReturnNode:
            self.traverse(node.children[0])
        elif type(node) == CallNode:
            for child in node.children:
                self.id_node(child)
        else:
            for child in node.children:
                self.traverse(child)

    def block_node(self, node):
        self.current_scope = LocalScope(self.current_scope)
        print("new local scope")
        for child in node.children:
            self.traverse(child)
        # close scope
        if self.current_scope != self.global_scope:
            self.current_scope = self.current_scope.parent
            print("closing local scope")

    def assign_node(self, node):
        if len(node.children) == 3:
            self.id_node(node.children[1])
            symbol = VariableSymbol(node.children[0].data, node.children[1].data)
            self.current_scope.define(symbol)
        else:
            self.id_node(node.children[0].data)
        for child in node.children[-1].children:
            self.traverse(child)

    def id_node(self, node):
        ref = self.current_scope.resolve(node.data)
        if ref == None:
            self.not_declared(node.data)
        print("symbol %s referenced" % node.data)

    def def_node(self, node):
        args = []
        print("function scope", node.children[0].data)
        for index in range(1, len(node.children)-2, 2):
            args.append(VariableSymbol(node.children[index].data, node.children[index+1].data))
            print("adding symbol", node.children[index].data)
            self.id_node(node.children[index+1])
        self.id_node(node.children[-2])
        symbol = FunctionSymbol(node.children[0].data, node.children[-2].data, args, self.current_scope)
        self.current_scope.define(symbol)
        self.current_scope = symbol
        self.traverse(node.children[-1])
        print("closing function scope")

    def not_declared(self, name):
        print(name, "was not given a type before use", file=sys.stderr)
        exit(1)
            

