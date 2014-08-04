
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
        print(self.scanner.tokens)
        self.assertEqual(len(self.scanner.tokens), 4)
        self.scanner.scan("test = 4")
        self.assertEqual(len(self.scanner.tokens), 3)
        self.scanner.scan("test=4+3")
        self.assertEqual(len(self.scanner.tokens), 5)


if __name__ == '__main__':
    unittest.main()
