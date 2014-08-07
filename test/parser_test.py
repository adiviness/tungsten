
import unittest
from parser.parser import *
from parser.scanner import Scanner, TokenType, Token 
from parser.nodes import *

class TestParser(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()
        self.parser = Parser()

    def test_no_input(self):
        self.parser.parse([])
        self.assertEqual(type(self.parser.root_node), BlockNode)
        self.assertEqual(len(self.parser.root_node.children), 0)

    def test_match_one_type(self):
        self.parser.tokens = []
        int_token = Token(TokenType.INTEGER, "3")
        self.assertFalse(self.parser.match(TokenType.INTEGER))
        self.parser.tokens.append(int_token)
        self.assertTrue(self.parser.match(TokenType.INTEGER))

    def test_match_multiple_types(self):
        int_token = Token(TokenType.INTEGER, "3")
        self.parser.tokens = [int_token]
        self.assertTrue(self.parser.match(TokenType.STRING, TokenType.INTEGER))

    def test_matchN(self):
        self.parser.tokens = [Token(TokenType.STRING, "hello"),
                              Token(TokenType.STRING, "world"),
                              Token(TokenType.INTEGER, "7")]
        self.assertFalse(self.parser.matchN(TokenType.INTEGER, 3))
        self.assertTrue(self.parser.matchN(TokenType.STRING, 0))
        self.assertTrue(self.parser.matchN(TokenType.INTEGER, 2))

    def test_consume(self):
        while_token = Token(TokenType.WHILE, "while")
        int_token = Token(TokenType.INTEGER, "7")
        self.parser.tokens = [while_token, int_token]
        self.assertEqual(self.parser.consume(TokenType.WHILE), while_token)
        self.assertEqual(len(self.parser.tokens), 1)

    def test_new_variable_assignment(self):
        assignment = "test Int = 3"
        self.scanner.scan(assignment)
        self.parser.parse(self.scanner.tokens)
        root_node = self.parser.root_node
        self.assertEqual(type(root_node), BlockNode)
        self.assertEqual(len(root_node.children), 1)
        self.assertEqual(type(root_node.children[0]), AssignNode)
        assign_node = root_node.children[0]
        self.assertEqual(len(assign_node.children), 3)
        self.assertEqual(type(assign_node.children[0]), IDNode)
        self.assertEqual(type(assign_node.children[1]), IDNode)
        self.assertEqual(type(assign_node.children[2]), IntNode)
        self.assertEqual(assign_node.children[0].data, "test")
        self.assertEqual(assign_node.children[1].data, "Int")
        self.assertEqual(assign_node.children[2].data, "3")

    def test_existing_variable_assignment(self):
        assignment = "test = 5"
        self.scanner.scan(assignment)
        self.parser.parse(self.scanner.tokens)
        root_node = self.parser.root_node
        self.assertEqual(type(root_node), BlockNode)
        self.assertEqual(len(root_node.children), 1)
        self.assertEqual(type(root_node.children[0]), AssignNode)
        assign_node = root_node.children[0]
        self.assertEqual(len(assign_node.children), 2)
        self.assertEqual(type(assign_node.children[0]), IDNode)
        self.assertEqual(type(assign_node.children[1]), IntNode)
        self.assertEqual(assign_node.children[0].data, "test")
        self.assertEqual(assign_node.children[1].data, "5")


    
if __name__ == '__main__':
    unittest.main()






    
