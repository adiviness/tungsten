
from parser import parse


class Runner:
    
    def __init__(self):
        self.root = None
        
    def run(self):
        self.root = parse()


if __name__ == "__main__":
    runner = Runner()
    runner.run()
