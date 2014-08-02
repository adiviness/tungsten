
COMPARISION_PRECEDENCE = 7
# Operator Precedence
# -------------------
# 1. ()
# 2. x.attribute
# 3. **
# 4. -x
# 5. *, /, %
# 6. +, -
# 7. ==, !=, <, <=, >, >=
# 8. not
# 9. and
#10. or

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

    def disassociate(self):
        '''resets references to siblings and parent'''
        self.leftmost_sibling = self 
        self.right_sibling = None
        self.parent = None

    def give_child(self, child):
        child.disassociate()
        if self.children != []:
            child.leftmost_sibling = self.children[0]
            self.children[-1].right_sibling = child
        child.parent = self
        self.children.append(child)

class BinaryOpNode(ASTNode):

    def __init__(self, precedence):
        '''the closer to 0 precedence is, the earlier its operation is applied'''
        super().__init__()
        self.precedence = precedence

class UnaryOpNode(ASTNode):

    def __init__(self, precedence):
        super().__init__()
        self.precedence = precedence
        
class IntNode(ASTNode):

    def __init__(self, value):
        super().__init__(value)

class FloatNode(ASTNode):

    def __init__(self, value):
        super().__init__(value)

class TypeNode(ASTNode):

    def __init__(self, type_):
        super().__init__(type_)

class StringNode(ASTNode):

    def __init__(self, val):
        super().__init__(val)
    
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

class PlusNode(BinaryOpNode):

    def __init__(self):
        super().__init__(6)

class MinusNode(BinaryOpNode):

    def __init__(self):
        super().__init__(6)

class MultiplyNode(BinaryOpNode):

    def __init__(self):
        super().__init__(5)

class DivideNode(BinaryOpNode):

    def __init__(self):
        super().__init__(5)

class ModNode(BinaryOpNode):

    def __init__(self):
        super().__init__(5)

class ExponentNode(BinaryOpNode):

    def __init__(self):
        super().__init__(3)

class AndNode(BinaryOpNode):

    def __init__(self):
        super().__init__(8)

class OrNode(BinaryOpNode):

    def __init__(self):
        super().__init__(10)

class EqualNode(BinaryOpNode):

    def __init__(self):
        super().__init__(COMPARISION_PRECEDENCE)

class NotEqualNode(BinaryOpNode):

    def __init__(self):
        super().__init__(COMPARISION_PRECEDENCE)

class LessThanNode(BinaryOpNode):

    def __init__(self):
        super().__init__(COMPARISION_PRECEDENCE)

class LessThanEqualNode(BinaryOpNode):

    def __init__(self):
        super().__init__(COMPARISION_PRECEDENCE)

class GreaterThanNode(BinaryOpNode):

    def __init__(self):
        super().__init__(COMPARISION_PRECEDENCE)

class GreaterThanEqualNode(BinaryOpNode):

    def __init__(self):
        super().__init__(COMPARISION_PRECEDENCE)

class AttributeAccessorNode(BinaryOpNode):

    def __init__(self, struct, accessor):
        BinaryOpNode.__init__(self, 2)
        self.give_child(struct)
        self.give_child(accessor)

class NotNode(UnaryOpNode):

    def __init__(self):
        super().__init__(8)

class NegNode(UnaryOpNode):

    def __init__(self):
        super().__init__(4)

class BoolNode(ASTNode):

    def __init__(self, bool_):
        super().__init__(bool_)

class IfNode(ASTNode):

    def __init__(self):
        super().__init__()

class WhileNode(ASTNode):

    def __init__(self):
        super().__init__()

class CallNode(ASTNode):

    def __init__(self):
        super().__init__()

class DefNode(ASTNode):

    def __init__(self):
        super().__init__()

class ReturnNode(ASTNode):

    def __init__(self):
        super().__init__()

class IndexNode(ASTNode):

    def __init__(self):
        super().__init__()

class ClassNode(ASTNode):

    def __init__(self):
        super().__init__()

class ClassBlockNode(ASTNode):

    def __init__(self):
        super().__init__()

class StaticNode(ASTNode):

    def __init__(self):
        super().__init__()

class InstanceNode(ASTNode):

    def __init__(self):
        super().__init__()

class ClassVarNode(ASTNode):

    def __init__(self, val):
        super().__init__(val)

class InstanceVarNode(ASTNode):

    def __init__(self, val):
        super().__init__(val)

class FieldNode(ASTNode):

    def __init__(self):
        super().__init__()

class NilNode(ASTNode):

    def __init__(self):
        super().__init__()




        
