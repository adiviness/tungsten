
import unittest
from parser.scanner import *

class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()

    def test_scan_no_text(self):
        self.scanner.scan("")
        self.assertEqual(self.scanner.tokens, [])

if __name__ == '__main__':
    unittest.main()
