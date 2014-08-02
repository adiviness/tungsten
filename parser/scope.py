
from enum import Enum

class SymbolType(Enum):
    CLASS = 1
    FUNCTION = 2
    VARIABLE = 3
    
class Scope:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def resolve(self, name):
        if name in self.symbols.keys():
            return  self.symbols[name]
        elif self.parent != None:
            return self.parent.resolve(name)
        else:
            return None

class LocalScope(Scope):

    def __init__(self, parent):
        super().__init__("Local", parent)

class GlobalScope(Scope):

    def __init__(self):
        super().__init__("Global")
        self.define(ClassSymbol("Int", self))

class Symbol:

    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

class VariableSymbol(Symbol):

    def __init__(self, name, type_):
        super().__init__(name, type_)

class FunctionSymbol(Symbol, Scope):

    # TODO
    def __init__(self, name, args, parent):
        super(Symbol, self).__init__(name, SymbolType.FUNCTION)
        self.args = args
        self.parent = parent
        self.name = name
        self.symbols = {}
        for arg in args:
            self.define(arg)

    def resolve(self, name):
        if name in self.symbols.keys():
            return  self.symbols[name]
        else:
            return self.parent.resolve(name)

class ClassSymbol(Symbol, Scope):

    # TODO
    def __init__(self, name, parent_scope, parent_class=None):
        super(Symbol, self).__init__(name, SymbolType.CLASS)
        self.name = name
        self.parent = parent_scope
        self.symbols = {}
        self.parent_class = parent_class
        



