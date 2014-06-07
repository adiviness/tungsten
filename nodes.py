
class ASTNode:

    count = 0

    def __init__(self, data = None):
        self.children = []
        self.data = data
        self.right_sibling = None
        self.parent = None
        self.leftmost_sibling = self
        self.node_id = ASTNode.count
        ASTNode.count += 1

    def add_right_sibling(self, node):
        self.right_sibling = node
        node.leftmost_sibling = self.leftmost_sibling
        node.parent = self.parent
        
class IntNode(ASTNode):

    def __init__(self, value):
        super().__init__(value)

class TypeNode(ASTNode):

    def __init__(self, type_):
        super().__init__(type_)

class IDNode(ASTNode):

    def __init__(self, id_):
        super().__init__(id_)
    
class AssignNode(ASTNode):

    def __init__(self, children = None):
        super().__init__()
        if children != None:
            self.children = children

class BlockNode(ASTNode):

    def __init__(self):
        super().__init__()

class PlusNode(ASTNode):

    def __init__(self):
        super().__init__()

class MinusNode(ASTNode):

    def __init__(self):
        super().__init__()

class MultiplyNode(ASTNode):

    def __init__(self):
        super().__init__()

class DivideNode(ASTNode):

    def __init__(self):
        super().__init__()


        
