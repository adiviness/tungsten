
class VM:

    def __init__(self):
        self.call_stack = []
        self.operand_stack = []
        self.locals_ = []
        self.named_memory = {}
        self.function_info = {}

    def run(self, instructions):
        instructions = self._grab_function_definitions(instructions)
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
                if instr[1][0].isdigit():
                    self.operand_stack.append(self.locals_[-1][int(instr[1][0])]) # TODO should grab full number from push instr
                else:
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
                print(self.operand_stack.pop())
            else:
                local_count = self.function_info[instr[1]][0]
                self.locals_.append(self.operand_stack[0:local_count])
                self.locals_[-1].reverse()
                self.operand_stack = self.operand_stack[local_count:]
                for i in self.named_memory[instr[1]]:
                    self.execute(i)
                self.locals_.pop()

        

    def _grab_function_definitions(self, instructions):
        index = 0
        while index < len(instructions):
            instr = instructions[index]
            if instr[0] == "def":
                function_code = []
                while index + 1 < len(instructions):
                    function_code.append(instructions.pop(index + 1))
                    if function_code[-1][0] == "return":
                        break
                self.named_memory[instr[1]] = function_code
                self.function_info[instr[1]] = (int(instr[2]), int(instr[3]))
                instructions.pop(index)
            else:
                index += 1
        return instructions
                        
                    
