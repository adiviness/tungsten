
import sys, os.path

#from parser.parser import parse

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
        self.write_graphing_data()

    def write_graphing_data(self):
        output_file = open("%s.out" % self.output_file_prefix, 'w')
        self._write_node_ids(output_file, self.root)
        print('', file=output_file)
        self._write_node_children(output_file, self.root)

    def _write_node_ids(self, output_file, node):
        # need to escape " on strings
        if type(node) == StringNode:
            print(node.node_id, "%s:" % node.__class__.__name__, node.data.replace('"', '\\"'), file=output_file)
        elif node.data != None:
            print(node.node_id, "%s:" % node.__class__.__name__, node.data, file=output_file)
        else:
            print(node.node_id, "%s" % node.__class__.__name__, file=output_file)
        for child in node.children:
            self._write_node_ids(output_file, child)

    def _write_node_children(self, output_file, node):
        children_ids = map(lambda x: str(x.node_id), node.children)
        children_ids = ' '.join(children_ids)
        print(str(node.node_id), children_ids, file=output_file)
        for child in node.children:
            self._write_node_children(output_file, child)



if __name__ == "__main__":
    output_file_prefix = "output"
    if len(sys.argv) >= 2:
        output_file_prefix = os.path.splitext(sys.argv[1])[0]
    runner = Runner(output_file_prefix)
    runner.run()
