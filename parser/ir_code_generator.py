
from parser.nodes import *

LEFT = 0
RIGHT = 1

class IRCodeGenerator():
    '''generates intermediate code for a stack based vm'''

    def __init__(self):
        self.output_file = None

    def generate(self, ast, output_file_prefix):
        self.output_file = open("%s.s" % output_file_prefix, 'w')
        self.traverse(ast.root)
        self.output_file.close()

    def traverse(self, node, label_prefix="@Global"):
        if type(node) == IDNode:
            self.id_node(node, label_prefix)
        elif type(node) == IntNode:
            print("push", node.data, file=self.output_file)
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
        else:
            for child in node.children:
                self.traverse(child, label_prefix)

    def id_node(self, node, label_prefix):
        print("push %s%s" % (str(node.data), label_prefix), file=self.output_file)

    def def_node(self, node, label_prefix):
        arity = len(node.scope.symbols.keys())
        locals_ = len(node.children[-1].scope.symbols.keys())
        print("def", node.scope.name, arity, locals_, file=self.output_file)
        self.traverse(node.children[-1], "@%s" % node.scope.name + label_prefix )
        
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

