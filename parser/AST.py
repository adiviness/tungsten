
from parser.nodes import *

class AST:

    def __init__(self, root):
        self.root = root

    def pprint(self, node, depth = 0):
        '''pretty prints tree with node as root'''
        if node == None:
            return
        print('  ' * depth, "node_id:%s %s data:%s" % (node.node_id, node.__class__.__name__, str(node.data)), sep='')
        for child in node.children:
            self.pprint(child, depth + 1)

    def run_transformations(self):
        self.fix_negative_nodes(self.root)

    def write_graphing_data(self, filename):
        '''writes ast data for parse-tree-to-graphvis.py'''
        output_file = open("%s.out" % filename, 'w')
        self._write_node_ids(output_file, self.root)
        print('', file=output_file)
        self._write_node_children(output_file, self.root)

    def _write_node_ids(self, output_file, node):
        # need to escape " on strings
        if type(node) == StringNode:
            print(node.node_id, "%s:" % node.__class__.__name__, node.data.replace('"', '\\"'), file=output_file)
        elif node.data != None:
            print(node.node_id, "%s:" % node.__class__.__name__, node.data, file=output_file)
        else:
            print(node.node_id, "%s" % node.__class__.__name__, file=output_file)
        for child in node.children:
            self._write_node_ids(output_file, child)

    def _write_node_children(self, output_file, node):
        children_ids = map(lambda x: str(x.node_id), node.children)
        children_ids = ' '.join(children_ids)
        print(str(node.node_id), children_ids, file=output_file)
        for child in node.children:
            self._write_node_children(output_file, child)

    def replace_node(self, node, new_node_type):
        new_node = new_node_type()
        new_node.children = node.children
        new_node.parent = node.parent
        new_node.right_sibling = node.right_sibling
        new_node.leftmost_sibling = node.leftmost_sibling
        new_node.data = node.data
        index = node.parent.children.index(node)
        node.parent.children[index] = new_node
        if index == 0:
            for child in node.parent.children:
                child.leftmost_sibling = new_node
        else:
            node.parent.children[index - 1].right_sibling = new_node

    def fix_negative_nodes(self, node):
        if type(node) == MinusNode and len(node.children) == 1:
            self.replace_node(node, NegNode)
        for child in node.children:
            self.fix_negative_nodes(child)

    def fix_arithmetic_expressions(self, node):
        if type(node) in [BinaryOpNode, UnaryOpNode]:
            self.makeArithmeticTree(node)
        else:
            for child in node.children:
                self.fix_arithmetic_expressions(child)
        
        

# TODO copied from previous project, rework for this project
#
#    def fix_arithmetic_expressions(node):
#        if issubclass(type(node), BinaryOpNode):
#            parent = node.getParent()
#            node = self.makeArithmeticTree(node)
#        else:
#            for child in node.getChildren():
#                self.transformArithmetic(child)
#
#
#    def makeArithmeticTree(self, node):
#        operaterPrecedence = [[MultNode, DivNode],
#                              [PlusNode, MinusNode],
#                              [ShiftLNode, ShiftRNode]
#
#        ]
#        xs = self.flattenTree(node)
#        for n in xs:
#            n.destroyFamily()
#        for ops in operaterPrecedence:
#            index = 0
#            while index < len(xs):
#                if type(xs[index]) in ops:
#                    node = xs[index]
#                    right = xs.pop(index + 1)
#                    left = xs.pop(index - 1)
#                    node.setLeftmostChild(left)
#                    left.setRightSib(right)
#                    right.setParent(node)
#                    left.setParent(node)
#                else:
#                    index += 1
#
#        return xs[0]
#
#
#
#    def flattenTree(self, node):
#        if node == None:
#            return []
#        left = node.getLeftmostChild()
#        if left == None:
#            return [node]
#        xs = []
#        right = left.getRightSib()
#        xs += self.flattenTree(left) + [node] + self.flattenTree(right)
#        node.destroyFamily()
#        return xs
#    
