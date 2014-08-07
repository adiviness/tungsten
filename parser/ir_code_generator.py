
from parser.nodes import *

class IRCodeGenerator():
    '''generates intermediate code for a stack based vm'''

    def __init__(self):
        self.output_file = None

    def generate(self, ast, output_file_prefix):
        self.output_file = open("%s.s" % output_file_prefix, 'w')
        self.traverse(ast.root)
        self.output_file.close()

    def traverse(self, node, label_prefix=''):
        if type(node) == IDNode:
            print("push %s_%s" % (label_prefix, str(node.data)), file=self.output_file)
        elif type(node) == IntNode:
            print("push", node.data, file=self.output_file)
        elif type(node) == AssignNode:
            self.assign_node(node, label_prefix)
        else:
            for child in node.children:
                self.traverse(child, label_prefix)
        

    def assign_node(self, node, label_prefix):
        if len(node.children) == 3:
            print("name %s_%s" % (label_prefix, str(node.children[0].data)), file=self.output_file)
        self.traverse(node.children[-1], label_prefix)
        print("store %s_%s"% (label_prefix, str(node.children[0].data)), file=self.output_file)

