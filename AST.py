
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
