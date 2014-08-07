
from parser.nodes import *

LEFT = 0
RIGHT = 1

class IRCodeGenerator():
    '''generates intermediate code for a stack based vm'''

    def __init__(self):
        self.output_file = None
        self.scopes = []

    def generate(self, ast, output_file_prefix):
        self.output_file = open("%s.s" % output_file_prefix, 'w')
        self.traverse(ast.root)
        self.output_file.close()

    def traverse(self, node, label_prefix="@Global"):
        if type(node) == BlockNode:
            self.block_node(node, label_prefix)
        elif type(node) == IDNode:
            self.id_node(node, label_prefix)
        elif type(node) == IntNode:
            self.int_node(node, label_prefix)
        elif type(node) == AssignNode:
            self.assign_node(node, label_prefix)
        elif type(node) == PlusNode:
            self.binary_op_node(node, label_prefix, "+", LEFT)
        elif type(node) == MinusNode:
            self.binary_op_node(node, label_prefix, "-", LEFT)
        elif type(node) == DefNode:
            self.def_node(node, label_prefix)
        elif type(node) == ReturnNode:
            print("return", file=self.output_file)
        elif type(node) == CallNode:
            self.call_node(node, label_prefix)
        else:
            for child in node.children:
                self.traverse(child, label_prefix)

    def block_node(self, node, label_prefix):
        self.scopes.append(node.scope)
        for child in node.children:
            self.traverse(child, label_prefix)
        self.scopes.pop()

    def id_node(self, node, label_prefix):
        symbol = self.scopes[-1].resolve(str(node.data))
        if symbol.param_num != None:
            print("push %s%s" % (symbol.param_num, label_prefix), file=self.output_file)
        else:
            print("push %s%s" % (str(node.data), label_prefix), file=self.output_file)

    def int_node(self, node, label_prefix):
        print("push", node.data, file=self.output_file)

    def def_node(self, node, label_prefix):
        arity = len(node.scope.symbols.keys())
        locals_ = len(node.children[-1].scope.symbols.keys())
        print("def", "%s%s" % (node.scope.name, label_prefix), arity, locals_, file=self.output_file)
        self.scopes.append(node.scope)
        self.traverse(node.children[-1], "@%s" % node.scope.name + label_prefix )
        self.scopes.pop()

    def call_node(self, node, label_prefix):
        for child in node.children[1:]:
            self.traverse(child, label_prefix)
        print("call", "%s" % node.children[0].data + label_prefix, file=self.output_file)
        
    def binary_op_node(self, node, label_prefix, operand, associativity):
        if associativity == LEFT:
            self.traverse(node.children[0], label_prefix)
            self.traverse(node.children[1], label_prefix)
        else:
            self.traverse(node.children[1], label_prefix)
            self.traverse(node.children[0], label_prefix)
        print(operand, file=self.output_file)


    def assign_node(self, node, label_prefix):
        if len(node.children) == 3:
            print("name %s%s" % (str(node.children[0].data), label_prefix), file=self.output_file)
        self.traverse(node.children[-1], label_prefix)
        print("store %s%s"% (str(node.children[0].data), label_prefix), file=self.output_file)

