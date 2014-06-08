
from namespace import Namespace

class SymbolTable:

    def __init__(self):
        self.scopes = []
        self.namespace = Namespace()

    def open_scope(self):
        '''creates a new scope in symbol table'''
        self.scopes.append({})

    def close_scope(self):
        '''removes most recent scope from symbol table'''
        self.scopes.pop()

    def declared_locally(self, symbol):
        '''returns true if symbol is already declared in most recent scope'''
        symbol = self._normalize_symbol(symbol)
        return symbol in self.scopes[-1]

    def enter_symbol(self, name, type_, value):
        '''enters symbol into most recent scope'''
        namespace_node = self.namespace.add_word(name)
        self.scopes[-1][namespace_node] = (type_, value)


    def retrieve_symbol(self, symbol):
        '''returns data about symbol if it exists in a scope, else None'''
        symbol = self._normalize_symbol(symbol)
        index = len(self.scopes) - 1
        while index >= 0:
            if symbol in self.scopes[index]:
                return self.scopes[index][symbol]
            index -= 1
        return None

    def get_type(self, symbol):
        '''gets type of symbol'''
        return self.retrieve_symbol(symbol)[0]

    def get_value(self, symbol):
        '''gets value of symbol'''
        return self.retrieve_symbol(symbol)[1]
        
    def _normalize_symbol(self, symbol):
        if type(symbol) == str:
            symbol = self.namespace.find_word(symbol)
        return symbol
    
