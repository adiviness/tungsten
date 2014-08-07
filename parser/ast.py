
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
        self.fix_arithmetic_expressions(self.root)

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

    def fix_negative_nodes(self, node):
        if type(node) == MinusNode and len(node.children) == 1:
            negNode = NegNode()
            negNode.children = node.children
            node.parent.replace(node, negNode)
        for child in node.children:
            self.fix_negative_nodes(child)

    def fix_arithmetic_expressions(self, node):
        if (issubclass(type(node), BinaryOpNode)
            or issubclass(type(node), UnaryOpNode)):

            parent = node.parent
            new_node = self.makeArithmeticTree(node)
            parent.replace(node, new_node)
        else:
            for child in node.children:
                self.fix_arithmetic_expressions(child)

    def flattenTree(self, node):
        if node == None:
            return []
        if len(node.children) == 0:
            return [node]
        xs = []
        xs += self.flattenTree(node.children[0]) + [node]
        if len(node.children) > 1:
            xs += self.flattenTree(node.children[1])
        node.disassociate()
        return xs
        
    def makeArithmeticTree(self, node):
        flat_tree = self.flattenTree(node)
        for x in flat_tree:
            x.disassociate()
            x.children = []
        for precedence in range(1, 11):
            index = 0
            while index < len(flat_tree):
                if (hasattr(flat_tree[index], 'precedence')
                    and flat_tree[index].precedence == precedence):

                    parent = flat_tree[index]
                    if (issubclass(type(parent), UnaryOpNode)):
                        left = flat_tree.pop(index - 1)
                        parent.give_child(left)
                    else:
                        right = flat_tree.pop(index + 1)
                        left = flat_tree.pop(index - 1)
                        parent.give_child(left)
                        parent.give_child(right)
                else:
                    index += 1
        return flat_tree[0]

