from typing import Union

from . import _Table


class Where:
    """Where base class for all selection conditions."""
    _operator = "????"

    def __init__(self, field1: '_Table.TableField', field2: '_Table.TableField'):
        self._left = field1
        self._right = field2

        if isinstance(self._left, Union[_Table.TableField, _Table.CalculatedField]):
            self._left = self._left.full_name

        if isinstance(self._right, Union[_Table.TableField, _Table.CalculatedField]):
            self._right = self._right.full_name

    def __str__(self) -> str:
        return f'({self._left} {self.__class__._operator} {self._right})'


class WhereEq(Where):
    """Selection condition on equality ="""
    _operator = "="


class WhereGt(Where):
    """Selection condition on greater >"""
    _operator = ">"


class WhereLt(Where):
    """Selection condition on less <"""
    _operator = "<"


class WhereComposition(Where):
    """WhereComposition base class for compositions os Where objects."""
    _operator = "????"

    def __init__(self, *wheres: Union[Where, 'WhereComposition']):
        self._wheres = wheres

    def __str__(self) -> str:
        return f'({f" {self.__class__._operator} ".join(str(w) for w in self._wheres)})'


class WhereAND(WhereComposition):
    """Compose two Where objects with AND"""
    _operator = "AND"


class WhereOR(WhereComposition):
    """Compose two Where objets with OR"""
    _operator = "OR"