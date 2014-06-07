
from parser import parse
import sys


class Runner:
    
    def __init__(self, output_file_prefix):
        self.root = None
        self.output_file_prefix = output_file_prefix
        
    def run(self):
        self.root = parse()
        self.pprint(self.root)
        self.write_graphing_data()

    def write_graphing_data(self):
        output_file = open("%s.out" % self.output_file_prefix, 'w')
        self._write_node_ids(output_file, self.root)
        print('', file=output_file)
        self._write_node_children(output_file, self.root)

    def _write_node_ids(self, output_file, node):
        if node.data != None:
            print(node.node_id, "%s:" % node.__class__.__name__, node.data, file=output_file)
        else:
            print(node.node_id, "%s" % node.__class__.__name__, file=output_file)
        for child in node.children:
            self._write_node_ids(output_file, child)

    def _write_node_children(self, output_file, node):
        children_ids = map(lambda x: str(x.node_id), node.children)
        children_ids = ' '.join(children_ids)
        print(children_ids)
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
        output_file_prefix = sys.argv[1]
    runner = Runner(output_file_prefix)
    runner.run()
