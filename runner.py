
import sys, os.path

import parser.parser as parser
from parser.ast import AST
from parser.nodes import *
from parser.semantic_checker import *
from parser.ir_code_generator import IRCodeGenerator


class Runner:
    
    def __init__(self, output_file_prefix):
        self.root = None
        self.output_file_prefix = output_file_prefix
        self.ast = None
        
    def run(self):
        self.root = parser.parse()
        self.ast = AST(self.root)
        self.ast.run_transformations()
        self.ast.write_graphing_data("output")
        semantic_checker = SemanticChecker(self.ast)
        ir_generator = IRCodeGenerator()
        ir_generator.generate(self.ast, "ir")
        


        
if __name__ == "__main__":
    output_file_prefix = "output"
    if len(sys.argv) >= 2:
        output_file_prefix = os.path.splitext(sys.argv[1])[0]
    runner = Runner(output_file_prefix)
    runner.run()
