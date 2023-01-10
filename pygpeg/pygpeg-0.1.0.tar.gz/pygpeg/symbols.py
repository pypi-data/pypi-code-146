from abc import ABC, abstractmethod
import re
from typing import Any, List, Tuple
from .mixins import RegistryMixin


Match = Tuple[bool, int, List[Any]]


def single_value_identity(values: List[Any]):
    values[0] = values[1]


def multi_value_identity(values: List[Any]):
    values[0] = values[1:]


def none_or_one_identity(values: List[Any]):
    if len(values) == 2:
        values[0] = values[1]
    else:
        values[0] = None


class Symbol(RegistryMixin, ABC):
    """
    A symbol in the PEG used by the language.

    This is used as the base class for the other symbols
    used in the parsing grammar.

    * :class:`.Choice`
    * :class:`.Empty`
    * :class:`.Literal`
    * :class:`.Matchp`
    * :class:`.Notp`
    * :class:`.OneOrMore`
    * :class:`.Optional`
    * :class:`.Regex`
    * :class:`.Sequence`
    * :class:`.ZeroOrMore`
    """
    @abstractmethod
    def match(self, content: str, index: int) -> Match:
        """
        Determine if a match for the specific
        :class:`.Symbol` exists in the ``content`` at the
        specified ``index``.

        Parameters
        ----------
        content: ``str``
            The string that is trying to be matched by the
            parser

        index: ``int``
            The index in ``content`` where the
            :class:`.Symbol` will try to start matching
        """
        pass


class Choice(Symbol):
    """
    A choice symbol that allows for an ordered choice.

    **Grammar specification**: In the grammar, you use a
    forward slash to separate the symbols from which to make
    a choice, such as ``a / b`` to specify an ordered choice
    between ``a`` and ``b``.

    Parameters
    ----------
    symbols: ``List[Symbol]``
        A list of :class:`.Symbol` instances from which the
        parser can match
    """

    def __init__(self, *symbols: List[Symbol]):
        self._symbols = symbols

    def match(self, content: str, index: int) -> Match:
        original_index = index
        for s in self._symbols:
            symbol = self.lookup(s)
            matches, index, value = symbol.match(content, original_index)
            if matches:
                return True, index, value
        return False, original_index, None

    def set_registry(self, value):
        for symbol in self._symbols:
            self.lookup(symbol).registry = value

    def __str__(self):
        s = " / ".join([str(s) for s in self._symbols])
        return f"({s})"


class Empty(Symbol):
    """
    A choice symbol that matches the empty string ε.

    **Grammar specification**: There is no way to directly
    use ε at this time in the grammar.
    """

    def match(self, content: str, index: int) -> Match:
        return True, 0, ""

    def set_registry(self, value):
        pass

    def __str__(self):
        return '""'


class Literal(Symbol):
    """
    A matching symbol that matches a string literal.

    **Grammar specification**: In the grammar, you use a
    single-quoted or double-quoted delimited string to
    specify a literal, such as ``'hello'``.

    Parameters
    ----------
    literal: ``str``
        The string literal that this symbol should match
    """

    def __init__(self, literal: str):
        self._literal = literal

    def match(self, content: str, index: int) -> Match:
        for i in range(len(self._literal)):
            end = index + i
            if end >= len(content) or content[end] != self._literal[i]:
                return False, -1, None
        return True, len(self._literal) + index, self._literal

    def set_registry(self, value):
        pass

    def __str__(self):
        return f'"{self._literal}"'


class Matchp(Symbol):
    """
    A matching symbol that is the and-predicate.

    From the description on Wikipedia:

        The and-predicate expression &e invokes the
        sub-expression e, and then succeeds if e succeeds
        and fails if e fails, but in either case never
        consumes any input.

    **Grammar specification**: In the grammar, you prefix
    the symbol to test with an ``&`` character.

    Parameters
    ----------
    symbol: :class:`.Symbol`
        The symbol to match on
    """

    def __init__(self, symbol: Symbol):
        self._symbol = symbol

    def match(self, content: str, index: int) -> Match:
        symbol = self.lookup(self._symbol)
        matches, _index, value = symbol.match(content, index)
        return matches, index, True if matches else None

    def set_registry(self, value):
        self.lookup(self._symbol).registry = value

    def __str__(self):
        return f"&({self._symbol})"


class Notp(Symbol):
    """
    A matching symbol that is the not-predicate.

    From the description on Wikipedia:

        The not-predicate expression !e succeeds if e fails
        and fails if e succeeds, again consuming no input in
        either case.

    **Grammar specification**: In the grammar, you prefix
    the symbol to test with an ``!`` character.

    Parameters
    ----------
    symbol: :class:`.Symbol`
        The symbol to test for not matching
    """
    def __init__(self, symbol: Symbol):
        self._symbol = symbol

    def match(self, content: str, index: int) -> Match:
        symbol = self.lookup(self._symbol)
        matches, _index, value = symbol.match(content, index)
        return not matches, index, None if matches else True

    def set_registry(self, value):
        self.lookup(self._symbol).registry = value

    def __str__(self):
        return f"!({self._symbol})"


class OneOrMore(Symbol):
    """
    A matching symbol that provides the ability to consume
    one or more of the same symbol.

    **Grammar specification**: In the grammar, you use
    suffix the symbol an ``+`` character.

    Parameters
    ----------
    symbol: :class:`.Symbol`
        The symbol to allow one or more occurrences
    """
    def __init__(self, symbol: Symbol):
        self._symbol = symbol

    def match(self, content: str, index: int) -> Match:
        good_index = index
        values = []
        symbol = self.lookup(self._symbol)
        matches, index, value = symbol.match(content, index)
        if not matches:
            return False, good_index, None
        while matches:
            values.append(value)
            good_index = index
            matches, index, value = symbol.match(content, index)
        return True, good_index, values

    def set_registry(self, value):
        self.lookup(self._symbol).registry = value

    def __str__(self):
        return f"({self._symbol})+"


class Optional(Symbol):
    """
    A matching symbol that provides the ability to consume
    zero or one of a same symbol.

    **Grammar specification**: In the grammar, you use
    suffix the symbol an ``?`` character.

    Parameters
    ----------
    symbol: :class:`.Symbol`
        The symbol to test for zero or one instance
    """
    def __init__(self, symbol: Symbol):
        self._symbol = symbol

    def match(self, content: str, index: int) -> Match:
        good_index = index
        symbol = self.lookup(self._symbol)
        matches, index, value = symbol.match(content, index)
        final_value = None
        if matches:
            good_index = index
            final_value = value
        return True, good_index, final_value

    def set_registry(self, value):
        self.lookup(self._symbol).registry = value

    def __str__(self):
        return f"({self._symbol})?"


class Regex(Symbol):
    """
    A matching symbol that works based on a regular expression.

    Parameters
    ----------
    literal: ``str``
        The string representation of a regular expression
        that this symbol should match
    """

    def __init__(self, literal: str):
        self._literal = re.compile(literal)

    def match(self, content: str, index: int) -> Match:
        m = self._literal.match(content, index)
        if m is None:
            return False, -1, None
        return True, m.end(), m.group(0)

    def set_registry(self, value):
        pass

    def __str__(self):
        return f"|{self._literal.pattern}|"


class Sequence(Symbol):
    """
    A matching symbol that matches the entire sequence of
    symbols, or fails.

    **Grammar specification**: In the grammar, you just list
    the symbols with spaces between them, such as ``a b c``.

    Parameters
    ----------
    symbols: :class:`List[Symbol]`
        The symbol to test for zero or one instance
    """
    def __init__(self, *symbols: List[Symbol]):
        self._symbols = symbols

    def match(self, content: str, index: int) -> Match:
        original_index = index
        values = []
        for symbol in self._symbols:
            symbol = self.lookup(symbol)
            try:
                matches, index, value = symbol.match(content, index)
            except AttributeError:
                raise
            if not matches:
                return False, original_index, None
            values.append(value)
        return True, index, values

    def set_registry(self, value):
        for s in self._symbols:
            try:
                self.lookup(s).registry = value
            except AttributeError:
                pass

    def __str__(self):
        syms = " ".join([str(s) for s in self._symbols])
        return f"({syms})"


class ZeroOrMore(Symbol):
    """
    A matching symbol that provides the ability to consume
    zero or more of the same symbol.

    **Grammar specification**: In the grammar, you use
    suffix the symbol an ``*`` character.

    Parameters
    ----------
    symbol: :class:`.Symbol`
        The symbol to allow zero or more occurrences
    """
    def __init__(self, symbol: Symbol):
        self._symbol = symbol

    def match(self, content: str, index: int) -> Match:
        good_index = index
        matches = True
        values = None
        symbol = self.lookup(self._symbol)
        value = None
        while matches:
            if values is None:
                values = []
            else:
                values.append(value)
            good_index = index
            matches, index, value = symbol.match(content, index)
        return True, good_index, values

    def set_registry(self, value):
        self.lookup(self._symbol).registry = value

    def __str__(self):
        return f"({self._symbol})*"
