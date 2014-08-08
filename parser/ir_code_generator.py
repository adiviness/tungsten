
from parser.nodes import *

LEFT = 0
RIGHT = 1

class IRCodeGenerator():
    '''generates intermediate code for a stack based vm'''

    def __init__(self):
        self.output_file = None
        self.scopes = []
        self.label_count = 0
        self.generated_code = []

    def generate(self, node, output_file_prefix=None):
        self.generated_code = []
        self.traverse(node)
        if output_file_prefix != None:
            self.output_file = open("%s.s" % output_file_prefix, 'w')
            for line in self.generated_code:
                print(line, file=self.output_file)
            self.output_file.close()
        return self.generated_code

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
        elif type(node) == ModNode:
            self.binary_op_node(node, label_prefix, "%", LEFT)
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
            self.generated_code.append("push %s%s" % (symbol.param_num, label_prefix))
        else:
            self.generated_code.append("push %s%s" % (str(node.data), label_prefix))

    def int_node(self, node, label_prefix):
        self.generated_code.append("push %s" %  str(node.data))

    def bool_node(self, node, label_prefix):
        if node.data == "true":
            self.generated_code.append("push 1")
        else:
            self.generated_code.append("push 0")
            

    def def_node(self, node, label_prefix):
        arity = len(node.scope.symbols.keys())
        locals_ = len(node.children[-1].scope.symbols.keys())
        self.generated_code.append("def %s%s %d %d" % (node.scope.name, label_prefix, arity, locals_))
        self.scopes.append(node.scope)
        self.traverse(node.children[-1], "@%s" % node.scope.name + label_prefix)
        self.scopes.pop()
        self.generated_code.append("label end_func@%s" % node.scope.name + label_prefix)

    def call_node(self, node, label_prefix):
        for child in node.children[1:]:
            self.traverse(child, label_prefix)
        #print("call", "%s" % node.children[0].data + label_prefix, file=self.output_file)
        scope = self.scopes[-1].find_containing_scope(node.children[0].data)
        scope_names = [node.children[0].data, scope.name]
        while scope.parent != None:
            scope = scope.parent
            scope_names.append(scope.name)
        self.generated_code.append("call %s" % "@".join(scope_names))

    def binary_op_node(self, node, label_prefix, operand, associativity):
        if associativity == LEFT:
            self.traverse(node.children[0], label_prefix)
            self.traverse(node.children[1], label_prefix)
        else:
            self.traverse(node.children[1], label_prefix)
            self.traverse(node.children[0], label_prefix)
        self.generated_code.append(operand)
        
    def unary_op_node(self, node, label_prefix, operand):
        self.traverse(node.children[0], label_prefix)
        self.generated_code.append(operand)

    def return_node(self, node, label_prefix):
        self.traverse(node.children[0], label_prefix)
        self.generated_code.append("return")

    def assign_node(self, node, label_prefix):
        if len(node.children) == 3:
            self.generated_code.append("name %s%s" % (str(node.children[0].data), label_prefix))
        self.traverse(node.children[-1], label_prefix)
        self.generated_code.append("store %s%s"% (str(node.children[0].data), label_prefix))

    def if_node(self, node, label_prefix):
        self.traverse(node.children[0], label_prefix)
        if len(node.children) == 2:
            end_label = "label_%d" % self.label_count
            self.label_count += 1
            self.generated_code.append("jne 1 %s" % end_label)
            self.traverse(node.children[1], label_prefix)
            self.generated_code.append("label %s" % end_label)
        else:
            else_label = "label_%d" % self.label_count
            self.label_count += 1
            end_label = "label_%d" % self.label_count
            self.label_count += 1
            self.generated_code.append("jne 1 %s" % else_label)
            self.traverse(node.children[1], label_prefix)
            self.generated_code.append("j %s" % end_label)
            self.generated_code.append("label %s" % else_label)
            self.traverse(node.children[2], label_prefix)
            self.generated_code.append("label %s" % end_label)

    def while_node(self, node, label_prefix):
        start_label = "label_%d" % self.label_count
        self.label_count += 1
        end_label = "label_%d" % self.label_count
        self.label_count += 1
        self.generated_code.append("label %s" % start_label)
        self.traverse(node.children[0], label_prefix)
        self.generated_code.append("jne 1 %s" % end_label)
        self.traverse(node.children[1], label_prefix)
        self.generated_code.append("j %s" % start_label)
        self.generated_code.append("label %s" % end_label)
















        
