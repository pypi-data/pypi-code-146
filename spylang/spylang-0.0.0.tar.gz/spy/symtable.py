from dataclasses import dataclass
from spy.vm import W_Type

class SymbolAlreadyDeclaredError(Exception):
    """
    A symbol is being redeclared
    """


@dataclass
class Symbol:
    name: str
    wt_type: W_Type


class SymTable:
    def __init__(self, scope_name, parent=None):
        self._scope_name = scope_name
        self._symbols = {}
        self._parent = parent

    def declare(self, name, wt_type):
        if name in self._symbols:
            raise SymbolAlreadyDeclaredError(name)
        self._symbols[name] = s = Symbol(name, wt_type)
        return s

    def lookup(self, name):
        if name in self._symbols:
            # found in the local scope
            return self._symbols[name]
        elif self._parent is not None:
            return self._parent.lookup(name)
        else:
            return None # not found
