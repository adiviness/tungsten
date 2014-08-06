
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

    def class_resolve(self, name):
        if self.parent == None:
            return None
        else:
            self.parent.class_resolve(name)

class LocalScope(Scope):

    def __init__(self, parent):
        super().__init__("Local", parent)


class GlobalScope(Scope):

    def __init__(self):
        super().__init__("Global")
        self.define(ClassSymbol("Int", self))

    def class_resolve(self, name):
        return None

class Symbol:

    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

class VariableSymbol(Symbol):

    def __init__(self, name, type_):
        super().__init__(name, type_)

class ClassVariableSymbol(VariableSymbol):

    def __init__(self, name, type_):
        super().__init__(name, type_)

class InstanceVariableSymbol(VariableSymbol):

    def __init__(self, name, type_):
        super().__init__(name, type_)

class FunctionSymbol(Symbol, Scope):

    def __init__(self, name, type_, args, parent):
        super(Symbol, self).__init__(name, type_)
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

    def class_resolve(self, name):
        if name in self.symbols.keys():
            return self.symbols[name]
        elif self.parent_class != None:
            return self.parent_class.class_resolve(name)
        else:
            return None
        



