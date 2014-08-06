
import sys
from parser.scope import *
from parser.nodes import *

class SymbolNotDeclaredException(Exception):

    def __init__(self, value):
        self.value = value
        

class SymbolTable:

    def __init__(self):
        self.current_scope = None
        self.global_scope = GlobalScope()


    def harvest_symbols(self, node):
        self.current_scope = self.global_scope
        node.scope = self.current_scope
        print("global scope")
        for child in node.children:
            try:
                self.traverse(child)
            except SymbolNotDeclaredException as e:
                print(e.value, "was not given a type before use", file=sys.stderr)
        print("closing global scope")
        # debug
        self.print_table(node)

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
            self.call_node(node)
        elif type(node) == ClassNode:
            self.class_node(node)
        elif type(node) == ClassBlockNode:
            self.class_block_node(node)
        elif type(node) == ClassVarNode:
            self.class_var_node(node)
        else:
            for child in node.children:
                self.traverse(child)

    def call_node(self, node):
        for child in node.children:
            if type(child) == IDNode:
                self.id_node(child)

    def block_node(self, node):
        self.current_scope = LocalScope(self.current_scope)
        print("new local scope")
        for child in node.children:
            self.traverse(child)
        node.scope = self.current_scope
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
            if type(node.children[0]) == IDNode:
                self.id_node(node.children[0])
            elif type(node.children[0]) == ClassVarNode:
                self.class_var_node(node.children[0])
        self.traverse(node.children[-1])

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
        node.scope = self.current_scope
        self.current_scope = self.current_scope.parent

    def class_node(self, node):
        print("class scope", node.children[0].data) 
        symbol = ClassSymbol(node.children[0].data, self.current_scope, None) # TODO should change None to parent class once inheritence is supported
        self.current_scope.define(symbol)
        self.current_scope = symbol
        self.traverse(node.children[-1])
        print("closing class scope")
        node.scope = self.current_scope
        #print(str(self.current_scope))
        self.current_scope = self.current_scope.parent

    def class_block_node(self, node):
        for child in node.children:
            if type(child) == FieldNode:
                self.field_node(child)
            elif type(child) in [StaticNode, InstanceNode]:
                self.traverse(child)

    def class_var_node(self, node):
        ref = self.current_scope.class_resolve(node.data)
        if ref == None:
            self.not_declared(node.data)
        print("symbol %s referenced" % node.data)
    

    def field_node(self, node):
        type_ = node.children[1].data
        field_name = node.children[0].data
        self.id_node(node.children[1])
        if type(node.children[0] == ClassVarNode):
            field_symbol = ClassVariableSymbol(field_name, type_)
            print("adding class variable symbol", field_name)
        else:
            field_symbol = InstanceVariableSymbol(field_name, type_)
            print("adding instance variable symbol", field_name)
        self.current_scope.define(field_symbol)
                    

    def not_declared(self, name):
        raise SymbolNotDeclaredException(name)
            
    def print_table(self, node):
        if node.scope != None:
            node.scope.print_scope()
        for child in node.children:
            self.print_table(child)

