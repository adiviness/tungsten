
class TypeNode:
    '''Node that contains information about a type'''

    def __init__(self, type_name):
        self.type_name = type_name
        self.static_symbols = {}
        self.instance_symbols = {}
        self.parent = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def path_to_root(self):
        node = self
        path = []
        while node.parent != None:
            path.append(node.parent)
            node = node.parent
        return path

class TypeTree:
    '''contains a hierarchy of all types'''

    def __init__(self):
        self.root = None

    def have_relation(self, one, two):
        nodeOne = self.find(one)
        nodeTwo = self.find(two)
        if nodeOne == None or nodeTwo == None:
            return False
        pathOne = nodeOne.path_to_root()
        pathTwo = nodeTwo.path_to_root()
        return nodeOne in pathTwo or nodeTwo in pathOne

    def generalize(self, one, two):
        '''returns the more general of the provided type names'''
        nodeOne = self.find(one)
        nodeTwo = self.find(two)
        pathOne = nodeOne.path_to_root()
        pathTwo = nodeTwo.path_to_root()
        if nodeOne in pathTwo:
            return nodeOne.type_name
        return nodeTwo.type_name
        

    def find(self, type_, node = None):
        return_node = None
        if node == None:
            node = self.root
        if type_ == node.type_name:
            return node
        else:
            for child in node.children:
                return_node = self.find(type_, child)
        return return_node
            

def get_default_type_tree():
    tree = TypeTree()
    nodeOne = TypeNode("Int")
    nodeTwo = TypeNode("Float")
    nodeTwo.add_child(nodeOne)
    nodeOne = TypeNode("Object")
    nodeOne.add_child(nodeTwo)
    tree.root = nodeOne
    return tree
                    
    
