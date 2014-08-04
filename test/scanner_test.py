
import unittest
from parser.scanner import *

class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()

    def test_scan_no_text(self):
        self.scanner.scan("")
        self.assertEqual(self.scanner.tokens, [])

    def test_scan_assignment(self):
        self.scanner.scan("test Int = 3")
        self.assertEqual(len(self.scanner.tokens), 4)
        self.scanner.scan("test = 4")
        self.assertEqual(len(self.scanner.tokens), 3)
        self.scanner.scan("test=4+3")
        self.assertEqual(len(self.scanner.tokens), 5)

    def test_reserved_words_can_be_part_of_variable(self):
        self.scanner.scan("inform Bool = false")
        self.assertEqual(len(self.scanner.tokens), 4)

    def test_indent_dedent_added_correctly(self):
        self.scanner.scan("if true:\n  x = 1\nx = x + 3")
        self.assertEqual(len(list(filter(lambda x: x.kind == TokenType.INDENT, self.scanner.tokens))), 1)
        self.assertEqual(len(list(filter(lambda x: x.kind == TokenType.DEDENT, self.scanner.tokens))), 1)
        
    def test_exception_on_illegal_input(self):
        with self.assertRaises(IllegalCharacterException):
            self.scanner.scan("&test Int = 3")

if __name__ == '__main__':
    unittest.main()
