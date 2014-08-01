
class NamespaceNode:
    '''A node that contains a char for the namespace'''

    def __init__(self, ch, parent = None):
        self.ch = ch
        self.parent = parent
        self.children = []

    def has_child(self, ch):
        '''returns True if node has a child with ch'''
        for child in self.children:
            if child.ch == ch:
                return True
        return False

    def get_child(self, ch):
        '''returns child with ch, else returns None'''
        for child in self.children:
            if child.ch == ch:
                return child
        return None

class Namespace:
    '''A container for immutable strings'''

    def __init__(self):
        self.root = NamespaceNode('')

    def add_word(self, word):
        '''adds word to namespace'''
        node = self.root
        for ch in word:
            if node.has_child(ch):
                node = node.get_child(ch)
            else:
                new_node = NamespaceNode(ch, node)
                node.children.append(new_node)
                node = new_node
        return node

    def get_word(self, node):
        '''returns word that node points to'''
        word = ''
        while node.parent != None:
            word += node.ch
            node = node.parent
        return word

    def find(self, word):
        '''return node that points to word'''
        node = self.root
        while len(word) != 0:
            if node.has_child(word[0]):
                node = node.get_child(word[0])
                word = word[1:]
            else:
                return None
        return node

        
        
