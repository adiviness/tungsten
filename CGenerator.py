
from nodes import *
import os

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
        output_file_name = "%s.c" % self.output_file_prefix
        fp = open(output_file_name, 'w')
        fp.close()
        output_file = open(output_file_name, 'r+')
        print("#include <stdlib.h>", file=output_file)
        print("#include <math.h>", file=output_file)
        print("#include <stdio.h>", file=output_file)
        print('#include "Bool.h"', file=output_file)
        print('#include "Int.h"', file=output_file)
        print("typedef double Float;", file=output_file)
        print("typedef char* String;", file=output_file)
        # generate classes before main
        for child in self.root_node.children:
            if type(child) == ClassNode:
                self.traverse_class_node(child, output_file, 0)
        self.root_node.children = list(filter(lambda x: type(x) != ClassNode, self.root_node.children))
        # generate functions before main
        for child in self.root_node.children:
            if type(child) == DefNode:
                self.traverse(child, output_file, 0)
        self.root_node.children = list(filter(lambda x: type(x) != DefNode, self.root_node.children))
        print("int main()", end='', file=output_file)
        self.traverse(self.root_node, output_file, 0)
        output_file.close()

    def traverse_class_node(self, node, output_file, depth):
        class_name = node.children[0].data
        class_vars = []
        instance_vars = []
        # class block node
        for n in node.children[1].children:
            if type(n) == FieldNode:
                if type(n.children[0]) == InstanceVarNode:
                    instance_vars.append((n.children[0].data, n.children[1].data))
                else:
                    class_vars.append((n.children[0].data, n.children[1].data))
        # class struct
        print("    "*depth, "struct %s_Class_Struct {" % class_name, sep='', file=output_file)
        for class_var in class_vars:
            print("    "*(depth+1), "%s %s;" % (class_var[1], class_var[0]), sep='', file=output_file)
        print("    "*depth, "};", sep='', file=output_file)
        print("    "*depth, "typedef %s_Class_Struct* %s_Class;" % (class_name, class_name), sep='', file=output_file)
        # object struct
        print("    "*depth, "struct %s_Object_Struct {" % class_name, sep='', file=output_file)
        print("    "*(depth+1), "%s_Class class;" % class_name, sep='', file=output_file)
        for instance_var in instance_vars:
            print("    "*(depth+1), "%s %s;" % (instance_var[1], instance_var[0]), sep='', file=output_file)
        print("    "*depth, "};", sep='', file=output_file)
        print("    "*depth, "typedef %s_Object_Struct* %s;" % (class_name, class_name), sep='', file=output_file)
        # generate class methods
        for n in node.children[1].children:
            if type(n) == StaticNode:
                for child in n.children:
                    self.generate_static_class_functions(class_name, child, output_file, depth)
            elif type(n) == InstanceNode:
                for child in n.children:
                    self.generate_instance_class_functions(class_name, child, output_file, depth)

    def generate_static_class_functions(self, class_name, node, output_file, depth):
        function_name = node.children[0].data
        return_type = node.children[1].data
        print("    "*depth, "%s %s_%s(" % (return_type, class_name, function_name), sep='', end='', file=output_file)
        print("%s_Class class" % class_name, end='', file=output_file)
        if len(node.children) > 3:
            print(", ", sep='', end='', file=output_file)
            index = 0
            params = node.children[1:-2:2]
            types = node.children[2:-2:2]
            while index < len(params):
                print(types[index].data, params[index].data, end='', file=output_file)
                if index + 1 < len(params):
                    print(", ", sep='', end='', file=output_file)
                index += 1
        print(")", sep='', end='', file=output_file)
        self.traverse(node.children[-1], output_file, depth)
            

    def generate_instance_class_functions(self, class_name, node, output_file, depth):
        function_name = node.children[0].data
        return_type = node.children[1].data
        print("    "*depth, "%s %s_%s(" % (return_type, class_name, function_name), sep='', end='', file=output_file)
        print("%s self" % class_name, end='', file=output_file)
        if len(node.children) > 3:
            print(", ", sep='', end='', file=output_file)
            index = 0
            params = node.children[1:-2:2]
            types = node.children[2:-2:2]
            while index < len(params):
                print(types[index].data, params[index].data, end='', file=output_file)
                if index + 1 < len(params):
                    print(", ", sep='', end='', file=output_file)
                index += 1
        print(")", sep='', end='', file=output_file)
        self.traverse(node.children[-1], output_file, depth)

    def traverse(self, node, output_file, depth):
        if type(node) == BlockNode:
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
            is_not_elif = self.last_char_written(output_file) == "\n"
            if is_not_elif:
                print("    "*depth, "if (", sep='', end='', file=output_file)
            else:
                print(" if (", sep='', end='', file=output_file)
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

        elif type(node) == CallNode:
            is_statement = self.last_char_written(output_file) == "\n"
            if is_statement:
                print("    "*depth, sep='', end='', file=output_file)
            print("%s(" % node.children[0].data, sep='', end='', file=output_file)
            index = 1
            while index < len(node.children):
                child_node = node.children[index]
                #print(child_node.data, sep='', end='', file=output_file)
                self.traverse(child_node, output_file, depth)
                if index + 1 < len(node.children):
                    print(", ", sep='', end='', file=output_file)
                index += 1
            print(")", sep='', end='', file=output_file)
            if is_statement:
                print(";", file=output_file)

        elif type(node) == DefNode:
            print("    "*depth, node.children[-2].data, sep='', end='', file=output_file)
            print(" ", node.children[0].data, "( ", sep='', end='', file=output_file)
            if len(node.children) > 3:
                index = 0
                params = node.children[1:-2:2]
                types = node.children[2:-2:2]
                while index < len(params):
                    print(types[index].data, params[index].data, end='', file=output_file)
                    if index + 1 < len(params):
                        print(", ", sep='', end='', file=output_file)
                    index += 1
            print(")", sep='', end='', file=output_file)
            self.traverse(node.children[-1], output_file, depth)
        
        elif type(node) == ReturnNode:
            print("    "*depth, "return ", sep='', end='', file=output_file)
            self.traverse(node.children[0], output_file, depth)
            print(";", file=output_file)
        elif type(node) == InstanceVarNode:
            print("self->%s->value" % node.data, end='', file=output_file)
        elif type(node) == ClassVarNode:
            print("class->%s->value" % node.data, end='', file=output_file)
                
                    
            
        else:
            print(node.data, end='', file=output_file)

        if type(node) == BlockNode:
            #if depth == 0:
                #print("    return 0;", file=output_file)
            print("    "*(depth), "}", sep='', file=output_file)


    def last_char_written(self, output_file):
        output_file.seek(output_file.tell() - 1)
        ch = output_file.read(1)
        output_file.seek(0, os.SEEK_END)
        return ch
        
    
