
import sys

from parser.symbol_table import SymbolTable
from parser.nodes import *

class SemanticChecker:
    '''scans ast for semantic errors'''

    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = self.build_symbol_table(ast)

    def build_symbol_table(self, ast):
        symbol_table = SymbolTable()
        symbol_table.harvest_symbols(ast.root)
        return symbol_table
        
        

