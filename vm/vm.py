
class VM:

    def __init__(self):
        self.call_stack = []
        self.operand_stack = []
        self.locals_ = []
        self.named_memory = {}

    def run(self, instructions):
        for instr in instructions:
            #print(self.operand_stack, self.call_stack)
            self.execute(instr)

    def execute(self, instr):
        if instr[0] == "name":
            self.named_memory[instr[1]] = None
        elif instr[0] == "store":
            self.named_memory[instr[1]] = self.operand_stack.pop()
        elif instr[0] == "push":
            if "@" in instr[1]:
                self.operand_stack.append(self.named_memory[instr[1]])
            else:
                self.operand_stack.append(int(instr[1]))
        elif instr[0] == "+":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(b + a)
        elif instr[0] == "-":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(b - a)
        elif instr[0] == "call":
            if instr[1] == "print@Global":
                print(self.operand_stack[0])
                # TODO
        
