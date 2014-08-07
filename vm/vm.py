
class VM:

    def __init__(self):
        call_stack = []
        operand_stack = []
        locals_ = []
        named_memory = {}

    def run(self, instructions):
        for instr in intructions:
            self.execute(instr)

    def execute(self, instr):
        if instr[0] == "name":
            named_memory[instr[1]] = None
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
            if instr[1] == "print":
                print(self.operand_stack[0])
                # TODO
        
