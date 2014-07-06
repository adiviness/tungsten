
import sys, os.path

from parser import parse
from semantic_checker import SemanticChecker
from CGenerator import CGenerator
from nodes import *


class Runner:
    
    def __init__(self, output_file_prefix):
        self.root = None
        self.output_file_prefix = output_file_prefix
        self.semantic_checker = SemanticChecker()
        
    def run(self):
        self.root = parse()
        #self.semantic_checker.build_symbol_table(self.root)
        #self.pprint(self.root)
        self.write_graphing_data()
        cGenerator = CGenerator(self.root, self.output_file_prefix)
        cGenerator.generate()

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

    def pprint(self, node, depth = 0):
        '''pretty prints tree with node as root'''
        if node == None:
            return
        print('  ' * depth, "node_id:%s %s data:%s" % (node.node_id, node.__class__.__name__, str(node.data)), sep='')
        for child in node.children:
            self.pprint(child, depth + 1)
        


if __name__ == "__main__":
    output_file_prefix = "output"
    if len(sys.argv) >= 2:
        output_file_prefix = os.path.splitext(sys.argv[1])[0]
    runner = Runner(output_file_prefix)
    runner.run()
