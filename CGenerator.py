
from nodes import *

OP_NODES = [
    PlusNode,
    MinusNode,
    MultiplyNode,
    DivideNode,
    ModNode,
    OrNode,
    AndNode,
    NotNode,
    EqualNode,
    NotEqualNode,
    LessThanNode,
    LessThanEqualNode,
    GreaterThanNode,
    GreaterThanEqualNode
]

OP_NODE_SYMBOL = {
    PlusNode: '+',
    MinusNode: '-',
    MultiplyNode: '*',
    DivideNode: '/',
    ModNode: '%',
    OrNode: '||' ,
    AndNode: '&&',
    NotNode: '!',
    EqualNode: '==',
    NotEqualNode: '!=',
    LessThanNode: '<',
    LessThanEqualNode: '<=',
    GreaterThanNode: '>',
    GreaterThanEqualNode: '>='
}
    

class CGenerator:
    '''generates C code from AST'''

    def __init__(self, root_node, output_file_prefix):
        self.root_node = root_node
        self.output_file_prefix = output_file_prefix
        self.blocks = 1

    def generate(self):
        output_file = open("%s.c" % self.output_file_prefix, 'w')
        print("#include <stdbool.h>", file=output_file)
        print("#include <math.h>", file=output_file)
        print("typedef int Int;", file=output_file)
        print("typedef bool Bool;", file=output_file)
        print("typedef char* String;", file=output_file)
        print("int main()", end='', file=output_file)
        self.traverse(self.root_node, output_file, 0)
        output_file.close()

    def traverse(self, node, output_file, depth):
        if type(node) == BlockNode:
            #print("    "*depth, "{", sep='', file=output_file)
            print(" {", file=output_file)
            for child in node.children:
                self.traverse(child, output_file, depth+1)
        elif type(node) == AssignNode:
            if len(node.children) == 3:
                print("    "*depth, "%s %s = " % (node.children[1].data, node.children[0].data), sep='', end='', file=output_file)
            else:
                print("    "*depth, "%s = " % node.children[0].data, sep='', end='', file=output_file)
            self.traverse(node.children[-1], output_file, depth+1)
            print(";", file=output_file)

        elif type(node) in OP_NODES:
            if len(node.children) == 1:
                print(OP_NODE_SYMBOL[type(node)], end='', file=output_file)
                self.traverse(node.children[0], output_file, depth+1)
            else:
                self.traverse(node.children[0], output_file, depth+1)
                print(OP_NODE_SYMBOL[type(node)], end='', file=output_file)
                self.traverse(node.children[1], output_file, depth+1)
        elif type(node) == ExponentNode:
            print("pow(", end='', file=output_file)
            self.traverse(node.children[0], output_file, depth+1)
            print(", ", end='', file=output_file)
            self.traverse(node.children[1], output_file, depth+1)
            print(")", end='', file=output_file)

        elif type(node) == IfNode:
            print("    "*depth, "if (", sep='', end='', file=output_file)
            self.traverse(node.children[0], output_file, depth)
            print(")", end='', file=output_file)
            self.traverse(node.children[1], output_file, depth)
            # possible else statement
            if len(node.children) == 3:
                print("    "*depth, "else", sep='', end='', file=output_file)
                self.traverse(node.children[2], output_file, depth)

        elif type(node) == WhileNode:
            print("    "*depth, "while (", sep='', end='', file=output_file)
            self.traverse(node.children[0], output_file, depth)
            print(")", end='', file=output_file)
            self.traverse(node.children[1], output_file, depth)

        else:
            print(node.data, end='', file=output_file)

        if type(node) == BlockNode:
            if depth == 0:
                print("    return 0;", file=output_file)
            print("    "*(depth), "}", sep='', file=output_file)
