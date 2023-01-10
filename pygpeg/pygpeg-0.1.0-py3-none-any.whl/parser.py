from abc import ABC, abstractmethod
from inspect import signature
import logging
from typing import Any, Callable, List
from .exceptions import (
    IncompleteParseError,
    NoGrammarError,
    NoRulesError,
    UnboundSymbolError,
    UnknownCallbackError,
)
from .mixins import RegistryMixin, UnknownSymbolError
from .helpers import (
    optional_space as osp,
    optional_whitespace as ows,
    required_line_break as rlb,
    required_whitespace as rws,
)
from .symbols import (
    Choice,
    Literal as lit,
    Match,
    Matchp,
    Notp,
    OneOrMore as oom,
    Optional as opt,
    Regex as re,
    Sequence as seq,
    Symbol,
    ZeroOrMore as zom,
)


Callback = Callable[[List[str]], Any]


def trace(fn):
    def _trace(self, *args, **kwargs):
        try:
            value = fn(self, *args, **kwargs)
            self.logger.debug(
                "%s\n\t > %s\n\t args: %s\n\t kwargs: %s",
                fn.__name__,
                value,
                args,
                kwargs,
            )
            return value
        except Exception as e:
            self.logger.error(
                "%s\n\t > %s\n\t args: %s\n\t kwargs: %s",
                fn.__name__,
                e,
                args,
                kwargs,
            )
            raise e

    return _trace


class Rule(RegistryMixin):
    """A rule in a grammar

    Parameters
    ----------
    callback: Callback
        The callback to use when the rule matches
    name: str
        The name of the rule
    symbol: :class:`pygpeg.symbols.Symbol`
        The symbol that provides the matching specification for the rule
    """
    def __init__(self, callback: Callback, name: str, symbol: Symbol):
        if not callable(callback):
            raise TypeError("callback must be callable")
        if not isinstance(symbol, Symbol) and not isinstance(symbol, str):
            raise TypeError("symbol must be a pygpeg.symbols.Symbol or str")
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        self._name = name
        self._symbol = symbol
        self._callback = callback

    def match(self, content: str, index: int) -> Match:
        """Matches content starting at ``index`` in ``content``

        Parameters
        ----------
        content: str
            The content of the string
        index: int
            The index in ``content`` to start matching at

        Returns
        -------
        matches: bool
            A flag that indicates if a match exists
        index: int
            The index at which the match ends
        parsed: List[Any]
            The value that the content was parsed into, one value per symbol
        """
        original_index = index
        symbol = self.lookup(self._symbol)
        matches, index, value = symbol.match(content, index)
        if not matches:
            return False, original_index, None
            value = [value]
        parsed = self._callback(value)
        return matches, index, parsed

    @property
    def name(self):
        """The name of the rule
        """
        return self._name

    def set_registry(self, value):
        """Sets the registry to be used by the rule to look up symbol callbacks

        Parameters
        ----------
        value: dict
            The dictionary that contains the callback for a symbol
        """
        try:
            symbol = self.lookup(self._symbol)
        except UnknownSymbolError as use:
            raise UnboundSymbolError(self, use.name)
        symbol.registry = value

    def __str__(self):
        return f"{self._name} <- {self._symbol}"


class Parser(ABC):
    """A base class for creating parsers.
    """
    def __init__(self):
        self._registry = {}
        self._starting_expression = None

    def add_rule(self, name: str, callback: Callback, symbol: Symbol):
        """Adds a rule to a parser

        Parameters
        ----------
        name: str
            The name of the rule
        callback: Callable[[List[str]], Any]
            The callback for the rule
        symbol: :class:`pygpeg.symbols.Symbol`
            The ``Symbol`` to use for the rule to match
        """
        if isinstance(name, Rule):
            rule = name
            name = rule.name
        else:
            rule = Rule(callback, name, symbol)
        self._registry[name] = rule
        if self._starting_expression is None:
            self._starting_expression = rule

    @abstractmethod
    def parse(self, content: str, ignore_incomplete_parse=False) -> Any:
        """Parse the content using the rules of the parser

        Parameters
        ----------
        content: str
            The contet to parse starting at index 0
        ignore_incomplete_parse: bool
            Set to ``True`` to parse the content as far as the parser will
            match
        """
        pass

    @property
    def registry(self):
        """Get the registry used by the parser
        """
        return self._registry

    def __str__(self):
        lines = [str(self._starting_expression)]
        for name, rule in self.registry.items():
            if rule == self._starting_expression:
                continue
            lines.append(str(rule))
        return "\n".join(lines)


class StringParser(Parser):
    """Parses a string of content based on its rules.
    """
    def parse(self, content: str, ignore_incomplete_parse=False) -> Any:
        if self._starting_expression is None:
            raise NoRulesError("parser has no rules")
        for r in self._registry.values():
            try:
                r.registry = self._registry
            except UnknownSymbolError as use:
                raise UnboundSymbolError(r, use.name)
        matches, index, value = self._starting_expression.match(content, 0)
        if index != len(content) and not ignore_incomplete_parse:
            raise IncompleteParseError(index, value)
        return value


class ParserBuilder:
    logger = logging.getLogger(f"{__name__}.Builder")

    def __init__(self, callback_registry={}):
        self.callback_registry = callback_registry
        self._parser = parser = StringParser()
        parser.add_rule(
            "peg",
            self._peg,
            seq("ows", "rule", zom(seq(oom("rlb"), "rule")), "ows"),
        )
        parser.add_rule(
            "rule",
            self._rule,
            seq(
                "osp",
                "name",
                "osp",
                Choice(lit("<-"), lit("←")),
                "osp",
                "choice",
                "rws",
                lit("<"),
                "name",
                lit(">"),
            ),
        )
        parser.add_rule(
            "choice",
            self._choice,
            seq("sequence", zom(seq("rws", lit("/"), "rws", "sequence"))),
        )
        parser.add_rule(
            "sequence", self._seq, seq("operated", zom(seq("rws", "operated")))
        )
        parser.add_rule(
            "operated",
            self._operated,
            seq("predicate", opt(Choice(lit("*"), lit("+"), lit("?")))),
        )
        parser.add_rule(
            "predicate",
            self._predicate,
            seq(opt(Choice(lit("&"), lit("!"))), "atomic"),
        )
        parser.add_rule(
            "atomic",
            self._atomic,
            Choice("literal", "regex", "name", seq(lit("("), "choice", lit(")"))),  # noqa
        )
        parser.add_rule(
            "literal",
            self._lit,
            Choice(
                seq(lit("'"), re("[^']+"), lit("'")),
                seq(lit('"'), re('[^"]+'), lit('"')),
            ),
        )
        parser.add_rule("regex", self._re, seq(lit("|"), re("[^|]+"), lit("|")))  # noqa
        parser.add_rule("name", self._name, re(r"\w+"))
        parser.add_rule("osp", self._osp, osp())
        parser.add_rule("rlb", self._rlb, rlb())
        parser.add_rule("rws", self._rws, rws())
        parser.add_rule("ows", self._ows, ows())

    def build(self, grammar: str, parser: Parser = None) -> Parser:
        self._target = parser or StringParser()
        if grammar is None or len(grammar) == 0:
            raise ValueError("grammar must be a non-empty string")
        return self._parser.parse(grammar)

    @trace
    def _andp(self, values):
        return Matchp(values[1])

    @trace
    def _atomic(self, values):
        if isinstance(values, list):
            return values[1]
        return values

    @trace
    def _choice(self, values):
        if len(values[1]) == 0:
            return values[0]
        args = [s for _, _, _, s in values[1]]
        return Choice(values[0], *args)

    @trace
    def _lit(self, values):
        return lit(values[1])

    @trace
    def _name(self, values):
        return values

    @trace
    def _notp(self, values):
        return Notp(values[2])

    @trace
    def _operated(self, values):
        sym = values[0]
        if values[1] == "*":
            sym = zom(sym)
        elif values[1] == "+":
            sym = oom(sym)
        elif values[1] == "?":
            sym = opt(sym)
        return sym

    @trace
    def _osp(self, values):
        pass

    @trace
    def _ows(self, values):
        pass

    @trace
    def _peg(self, values):
        self._target.add_rule(values[1], None, None)
        for _, rule in values[2]:
            self._target.add_rule(rule, None, None)
        return self._target

    @trace
    def _predicate(self, values):
        sym = values[1]
        if values[0] == "&":
            sym = Matchp(sym)
        elif values[0] == "!":
            sym = Notp(sym)
        return sym

    @trace
    def _re(self, values):
        return re(values[1])

    @trace
    def _rlb(self, values):
        pass

    @trace
    def _rws(self, values):
        pass

    @trace
    def _rule(self, values):
        callback_name = values[8]
        if callback_name not in self.callback_registry:
            raise UnknownCallbackError(callback_name)
        cb = self.callback_registry[callback_name]
        name = values[1]
        symbol = values[5]
        return Rule(cb, name, symbol)

    @trace
    def _seq(self, values):
        if len(values[1]) == 0:
            return values[0]
        else:
            args = [values[0]]
            for _, v in values[1]:
                args.append(v)
            return seq(*args)


class MethodRegistryParser(StringParser):
    """A base class to build convenient parsers

    Set the class attribute ``grammar`` to a string that
    describes your grammar.

    Use methods on the class as handlers for each rule.

    Parameters
    ----------
    grammar: str
        A grammar in a string to be parsed to build a :class:`.Parser`
    """
    def __init__(self, grammar: str = None):
        super().__init__()
        cls = self.__class__
        if not hasattr(cls, "_method_registry"):
            cls._method_registry = []
            for entry in dir(cls):
                if entry.startswith("__") and entry.endswith("__"):
                    continue
                attr = getattr(cls, entry)
                if not callable(attr):
                    continue
                spec = signature(attr)
                if len(spec.parameters) == 2:
                    cls._method_registry.append(entry)
        if grammar is None and not hasattr(self, "grammar"):
            raise NoGrammarError(self.__class__)
        elif grammar is None:
            grammar = self.grammar
        callback_registry = {
            key: getattr(self, key) for key in self.__class__._method_registry
        }
        ParserBuilder(callback_registry).build(grammar, self)
