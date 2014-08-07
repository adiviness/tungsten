
class VM:

    def __init__(self):
        self.call_stack = []
        self.operand_stack = []
        self.locals_ = []
        self.named_memory = {}
        self.function_info = {}
        self.instr_memory = []
        self.instr_pointer = 0

    def run(self, instructions):
        #print(self.instr_memory)
        self.gather_labels(instructions)
        self.instr_memory += instructions
        while self.instr_pointer != len(self.instr_memory):
            self.execute(self.instr_memory[self.instr_pointer])
            self.instr_pointer += 1

    def gather_labels(self, instructions):
        index = 0
        while index < len(instructions):
            if instructions[index][0] == "label":
                self.named_memory[instructions[index][1]] = len(self.instr_memory) + index
            index += 1

    def execute(self, instr):
        #print(self.instr_pointer)
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
        elif instr[0] == "*":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(b * a)
        elif instr[0] == "/":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(b // a)
        elif instr[0] == "%":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(b % a)
        elif instr[0] == "**":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(b ** a)
        elif instr[0] == "and":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(bool(b) and bool(a)))
        elif instr[0] == "or":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(bool(b) or bool(a)))
        elif instr[0] == "not":
            a = self.operand_stack.pop()
            self.operand_stack.append(int(not bool(a)))
        elif instr[0] == "==":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(b == a))
        elif instr[0] == "!=":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(b != a))
        elif instr[0] == "<":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(b < a))
        elif instr[0] == "<=":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(b <= a))
        elif instr[0] == ">":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(b > a))
        elif instr[0] == ">=":
            a = self.operand_stack.pop()
            b = self.operand_stack.pop()
            self.operand_stack.append(int(b >= a))
        elif instr[0] == "neg":
            a = self.operand_stack.pop()
            self.operand_stack.append(-a)
        elif instr[0]  == "def":
            self.def_instr(instr)
        elif instr[0] == "call":
            self.call(instr)
        elif instr[0] == "return":
            self.instr_pointer = self.call_stack.pop()
        elif instr[0] == "jne":
            self.jne_instr(instr)
        elif instr[0] == "j":
            self.instr_pointer = self.named_memory[instr[1]]

    def jne_instr(self, instr):
        if self.operand_stack.pop() != int(instr[1]):
            self.instr_pointer = self.named_memory[instr[2]]
                
        
    def def_instr(self, instr):
        function_name = instr[1]
        self.named_memory[function_name] = self.instr_pointer
        self.function_info[instr[1]] = (int(instr[2]), int(instr[3]))
        next_instr = self.instr_memory[self.instr_pointer + 1]
        while True:
        #until next_instr[0] == "label" and "end_func" in next_instr[1]:
            if next_instr[0] == "label" and "end_func" in next_instr[1]:
                break
            self.instr_pointer += 1
            next_instr = self.instr_memory[self.instr_pointer + 1]

    def call(self, instr):
        if instr[1] == "print@Global":
            print(self.operand_stack.pop())
        else:
            local_count = self.function_info[instr[1]][0]
            self.locals_.append(self.operand_stack[0:local_count])
            self.locals_[-1].reverse()
            self.operand_stack = self.operand_stack[local_count:]
            self.call_stack.append(self.instr_pointer)
            self.instr_pointer = self.named_memory[instr[1]]
                    
