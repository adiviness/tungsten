
import sys, os.path

import parser.parser as parser
from parser.ast import AST
from parser.nodes import *


class Runner:
    
    def __init__(self, output_file_prefix):
        self.root = None
        self.output_file_prefix = output_file_prefix
        self.ast = None
        
    def run(self):
        self.root = parser.parse()
        self.ast = AST(self.root)
        self.ast.write_graphing_data("output")


        
if __name__ == "__main__":
    output_file_prefix = "output"
    if len(sys.argv) >= 2:
        output_file_prefix = os.path.splitext(sys.argv[1])[0]
    runner = Runner(output_file_prefix)
    runner.run()
