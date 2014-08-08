
import sys, os.path

from parser.parser import *
from parser.scanner import Scanner
from parser.ast import AST
from parser.nodes import *
from parser.semantic_checker import *
from parser.ir_code_generator import IRCodeGenerator
from vm.vm import VM


class Runner:
    
    def __init__(self, output_file_prefix):
        self.root = None
        self.output_file_prefix = output_file_prefix
        self.ast = None
        
    def run(self):
        self.root = parse()
        self.ast = AST(self.root)
        self.ast.run_transformations()
        self.ast.write_graphing_data("output")
        semantic_checker = SemanticChecker(self.ast)
        ir_generator = IRCodeGenerator()
        ir_generator.generate(self.ast.root, "ir")
        fp = open("ir.s", 'r')
        lines = fp.readlines()
        for index in range(0, len(lines)):
            lines[index] = lines[index].strip().split()
        fp.close
        vm = VM()
        vm.run(lines)

    def repl(self):
        scanner = Scanner()
        parser = Parser()
        ir_generator = IRCodeGenerator()
        master_ast = AST(BlockNode())
        vm = VM()
        indent = False
        while(True):
            lines = []
            lines.append(input("> "))
            if lines[-1][-1] == ":":
                indent = True
            while indent:
                lines.append(input("] "))
                if lines[-1] == "": 
                    indent = False
                    break
                
            scanner.scan('\n'.join(lines))
            parser.parse(scanner.tokens)
            ast = AST(parser.root_node)
            for child in parser.root_node.children:
                master_ast.root.give_child(child)
            ast.run_transformations()
            semantic_checker = SemanticChecker(master_ast)
            for child in parser.root_node.children:
                ir_generator.scopes.append(master_ast.root.scope)
                ir_output = ir_generator.generate(child)
                ir_generator.scopes.pop()
                ir_output = [x.strip().split() for x in ir_output]
                vm.run(ir_output)
            #print("# ", vm.operand_stack[-1])

        


        
if __name__ == "__main__":
    output_file_prefix = "output"
    if len(sys.argv) >= 2:
        output_file_prefix = os.path.splitext(sys.argv[1])[0]
    runner = Runner(output_file_prefix)
    runner.repl()
