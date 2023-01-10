class IncompleteParseError(RuntimeError):
    """Indicates that the parser does not completely parse the input

    Parameters
    ----------
    index: int
        The place in the parse that fails

    value: :class:`typing.Any`
        The value parsed at the index
    """
    def __init__(self, index, value):
        self.index = index
        self.value = value


class NoGrammarError(ValueError):
    """A child of :class:`pygpeg.parser.MethodRegistryParser`
    without a ``grammar`` attribute

    Parameters
    ----------
    cls: :class:`typing.Type`
        The class that does not have a ``grammar`` attribute
    """
    def __init__(self, cls):
        super().__init__(f"No grammar attribute for {cls.__name__}")


class NoRulesError(RuntimeError):
    """Indicates that a grammar has no rules
    """
    pass


class UnboundSymbolError(RuntimeError):
    """Indicates a symbol that does not have a corresponding rule

    Parameters
    ----------
    rule: :class:`pygpeg.parser.Rule`
        The rule that contains the unbound sybmol
    unbound_name: str
        The symbol that has no corresponding rule
    """
    def __init__(self, rule, unbound_name):
        super().__init__(f'Missing "{unbound_name}" in {rule.name}')
        self.rule = rule
        self.unbound_name = unbound_name


class UnknownCallbackError(RuntimeError):
    """Indicates a name has no callback in the registry

    Parameters
    ----------
    name: str
        The name that has no corresponding callback in the registry
    """
    def __init__(self, name):
        super().__init__(f"Missing callback {name} from registry")
        self.name = name


class UnknownSymbolError(RuntimeError):
    """Indicates that there is an unknown symbol in the grammar

    Parameters
    ----------
    name: str
        The name of used in the rule that does not exist in the grammar
    """
    def __init__(self, name):
        super().__init__(f"Unknown symbol {name}")
        self.name = name
