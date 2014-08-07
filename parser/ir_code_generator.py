
from parser.nodes import *

LEFT = 0
RIGHT = 1

class IRCodeGenerator():
    '''generates intermediate code for a stack based vm'''

    def __init__(self):
        self.output_file = None
        self.scopes = []
        self.label_count = 0

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
        elif type(node) == BoolNode:
            self.bool_node(node, label_prefix)
        elif type(node) == AssignNode:
            self.assign_node(node, label_prefix)
        elif type(node) == PlusNode:
            self.binary_op_node(node, label_prefix, "+", LEFT)
        elif type(node) == MinusNode:
            self.binary_op_node(node, label_prefix, "-", LEFT)
        elif type(node) == MultiplyNode:
            self.binary_op_node(node, label_prefix, "*", LEFT)
        elif type(node) == DivideNode:
            self.binary_op_node(node, label_prefix, "/", LEFT)
        elif type(node) == ExponentNode:
            self.binary_op_node(node, label_prefix, "**", RIGHT)
        elif type(node) == AndNode:
            self.binary_op_node(node, label_prefix, "and", LEFT)
        elif type(node) == OrNode:
            self.binary_op_node(node, label_prefix, "or", LEFT)
        elif type(node) == NotNode:
            self.unary_op_node(node, label_prefix, "not")
        elif type(node) == EqualNode:
            self.binary_op_node(node, label_prefix, "==", LEFT)
        elif type(node) == NotEqualNode:
            self.binary_op_node(node, label_prefix, "!=", LEFT)
        elif type(node) == LessThanNode:
            self.binary_op_node(node, label_prefix, "<", LEFT)
        elif type(node) == LessThanEqualNode:
            self.binary_op_node(node, label_prefix, "<=", LEFT)
        elif type(node) == GreaterThanNode:
            self.binary_op_node(node, label_prefix, ">", LEFT)
        elif type(node) == GreaterThanEqualNode:
            self.binary_op_node(node, label_prefix, ">=", LEFT)
        elif type(node) == NegNode:
            self.unary_op_node(node, label_prefix, "neg")
        elif type(node) == DefNode:
            self.def_node(node, label_prefix)
        elif type(node) == ReturnNode:
            self.return_node(node, label_prefix)
        elif type(node) == CallNode:
            self.call_node(node, label_prefix)
        elif type(node) == IfNode:
            self.if_node(node, label_prefix)
        elif type(node) == WhileNode:
            self.while_node(node, label_prefix)
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

    def bool_node(self, node, label_prefix):
        if node.data == "true":
            print("push 1", file=self.output_file)
        else:
            print("push 0", file=self.output_file)
            

    def def_node(self, node, label_prefix):
        arity = len(node.scope.symbols.keys())
        locals_ = len(node.children[-1].scope.symbols.keys())
        print("def", "%s%s" % (node.scope.name, label_prefix), arity, locals_, file=self.output_file)
        self.scopes.append(node.scope)
        self.traverse(node.children[-1], "@%s" % node.scope.name + label_prefix)
        self.scopes.pop()
        print("label end_func@%s" % node.scope.name + label_prefix, file=self.output_file)

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
        
    def unary_op_node(self, node, label_prefix, operand):
        self.traverse(node.children[0], label_prefix)
        print(operand, file=self.output_file)

    def return_node(self, node, label_prefix):
        self.traverse(node.children[0], label_prefix)
        print("return", file=self.output_file)

    def assign_node(self, node, label_prefix):
        if len(node.children) == 3:
            print("name %s%s" % (str(node.children[0].data), label_prefix), file=self.output_file)
        self.traverse(node.children[-1], label_prefix)
        print("store %s%s"% (str(node.children[0].data), label_prefix), file=self.output_file)

    def if_node(self, node, label_prefix):
        self.traverse(node.children[0], label_prefix)
        if len(node.children) == 2:
            end_label = "label_%d" % self.label_count
            self.label_count += 1
            print("jne 1", end_label, file=self.output_file)
            self.traverse(node.children[1])
            print("label", end_label, file=self.output_file)
        else:
            else_label = "label_%d" % self.label_count
            self.label_count += 1
            end_label = "label_%d" % self.label_count
            self.label_count += 1
            print("jne 1", else_label, file=self.output_file)
            self.traverse(node.children[1])
            print("j", end_label, file=self.output_file)
            print("label", else_label, file=self.output_file)
            self.traverse(node.children[2])
            print("label", end_label, file=self.output_file)

    def while_node(self, node, label_prefix):
        start_label = "label_%d" % self.label_count
        self.label_count += 1
        end_label = "label_%d" % self.label_count
        self.label_count += 1
        print("label", start_label, file=self.output_file)
        self.traverse(node.children[0], label_prefix)
        print("jne 1", end_label, file=self.output_file)
        self.traverse(node.children[1], label_prefix)
        print("j", start_label, file=self.output_file)
        print("label", end_label, file=self.output_file)
















        
