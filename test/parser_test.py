
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


    
if __name__ == '__main__':
    unittest.main()
