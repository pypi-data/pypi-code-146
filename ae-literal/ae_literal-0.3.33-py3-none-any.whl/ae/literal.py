"""
literal type detection and evaluation
=====================================

a number, calendar date or other none-text-value gets represented by a literal string, if entered as user input or
has to be stored, e.g. as :ref:`configuration variable <config-variables>`.

the :class:`Literal` class implemented by this portion converts such a
:ref:`evaluable literal string <evaluable-literal-formats>` into the corresponding value (and type).
"""
import datetime
from typing import Any, Callable, Optional, Tuple, Type

from ae.base import DEF_ENCODE_ERRORS, UNSET                                        # type: ignore
from ae.parse_date import parse_date                                                # type: ignore
from ae.dynamicod import try_call, try_eval, try_exec                               # type: ignore


__version__ = '0.3.33'


BEG_CHARS = "([{'\""
END_CHARS = ")]}'\""


def evaluable_literal(literal: str) -> Tuple[Optional[Callable], Optional[str]]:
    """ check evaluable format of literal string, possibly return appropriate evaluation function and stripped literal.

    :param literal:     string to be checked if it is in the
                        :ref:`evaluable literal format <evaluable-literal-formats>` and if
                        it has to be stripped.
    :return:            tuple of evaluation/execution function and the (optionally stripped) literal
                        string (removed triple high-commas on expression/code-blocks) - if
                        :paramref:`~evaluable_literal.literal` is in one of the supported
                        :ref:`evaluable literal formats <evaluable-literal-formats>` - else the tuple
                        (None, <empty string>).
    """
    func = None
    ret = ''
    if (literal.startswith("'''") and literal.endswith("'''")) \
            or (literal.startswith('"""') and literal.endswith('"""')):
        func = try_exec
        ret = literal[3:-3]                                             # code block
    elif literal and literal[0] in BEG_CHARS and BEG_CHARS.find(literal[0]) == END_CHARS.find(literal[-1]):
        func = try_eval
        ret = literal                                                   # expression/list/dict/tuple/str/... literal
    elif literal in ('False', 'True'):
        func = bool                                                     # bool literal
        if literal == 'True':
            ret = literal       # else return empty string to get bool('') == False
    else:
        try:
            int(literal)
            func = int
            ret = literal                                               # int literal
        except ValueError:
            try:
                float(literal)
                func = float
                ret = literal                                           # float literal
            except ValueError:
                pass

    return func, ret


class Literal:
    """ convert literal string into the corresponding value (and type).

    pass the literal string on instantiation as first (the :paramref:`~Literal.literal_or_value`) argument. the
    :paramref:`second argument <Literal.value_type>` specifies the expected value type::

        >>>number = Literal("3", int)

    alternatively assign the :ref:`evaluable literal string <evaluable-literal-formats>` after the instantiation,
    directly to the :attr:`~Literal.value` attribute of the :class:`Literal` instance::

        >>>number = Literal(value_type=int)
        >>>number.value = "3"

    the corresponding `int` value provides the :attr:`~Literal.value` attribute::

        >>>assert number.value == 3
        >>>assert type(number.value) is int

    the second argument :paramref:`Literal.value_type` is not needed when the literal string indicates the exact type::

        >>>number = Literal("6")
        >>>assert type(number.value) is int

    specifying the second argument forces/restricts the value to a type, e.g. in the following example to a `float` even
    if the literal specifies an integer::

        >>>float_number = Literal("9", float)
        >>>assert float_number.value = 9.0
        >>>assert type(float_number.value) is float

    any type can be specified as the literal value type::

        my_list = Literal(value_type=list)
        my_dict = Literal(value_type=dict)
        my_datetime = Literal(value_type=datetime.datetime)
        my_instance = Literal(value_type=MyClass)

    by converting an :ref:`evaluable python expression literal <evaluable-literal-formats>` the value type get
    automatically determined. for example the following literal gets automatically converted into a `datetime` object::

        >>>datetime_value = Literal('(datetime.datetime.now())')

    also if assigned directly to the :attr:`~Literal.value` attribute::

        >>>date_value = Literal()
        >>>date_value.value = '(datetime.date.today())'

    .. hint::
        the literal string of the last two examples has to start and end with round brackets, to mark it as a
        :ref:`evaluable literal <evaluable-literal-formats>`.

    to convert calendar date literal strings into one of the supported ISO formats (:data:`~ae.base.DATE_TIME_ISO`
    or :data:`~ae.base.DATE_ISO`), the expected value type has to be specified::

        >>>date_value = Literal('2033-12-31', value_type=datetime.date)
        >>>assert date_value.value == datetime.date(2033, 12, 31)

    a `ValueError` exception will be raised if the conversion fails, or if the result cannot be converted into the
    requested value type::

        >>>date_literal = Literal(value_type=datetime.date)
        >>>date_literal.value = "invalid-date-literal"
        >>>date_value = date_literal.value             # value getter raises ValueError

    all supported literal formats are documented at the :attr:`~Literal.value` property/attribute.
    """

    def __init__(self, literal_or_value: Optional[Any] = None, value_type: Optional[Type] = None, name: str = 'LiT'):
        """ create new Literal instance.

        :param literal_or_value:    initial literal (evaluable string expression) or value of this instance.
        :param value_type:          type of the value of this instance (def=determined latest by/in the
                                    :attr:`~Literal.value` property getter).
        :param name:                name of the literal (only used for debugging/error-message).
        """
        self._name = name
        self._literal_or_value = None
        self._type = None if isinstance(value_type, type(None)) else value_type
        if literal_or_value is not None:
            self.value = literal_or_value

    def __repr__(self):
        return f"Literal({self._literal_or_value!r})"

    @property
    def value(self) -> Any:
        """ property representing the value of this Literal instance.

        :setter:    assign literal or a new value; can be either a value literal string or directly
                    the represented/resulting value. if the assigned value is not a string
                    and the value type of this instance got still unspecified then this instance
                    will be restricted to the type of the assigned value.
                    assigning a None value will be ignored - neither
                    the literal nor the value will change with that!
        :getter:    return the literal value; on the first call the literal will be evaluated
                    (lazy/late) and the value type will be set if still unspecified. further
                    getter calls will directly return the already converted literal value.

        .. _evaluable-literal-formats:

        if the literal of this :class:`Literal` instance coincide with one of the following
        evaluable formats then the value and the type of the value gets automatically recognized.
        an evaluable formatted literal strings has to start and end with one of the character pairs
        shown in the following table:

        +-------------+------------+------------------------------+
        | starts with | ends with  | evaluation value type        |
        +=============+============+==============================+
        |     (       |     )      | tuple literal or expression  |
        +-------------+------------+------------------------------+
        |     [       |     ]      | list literal                 |
        +-------------+------------+------------------------------+
        |     {       |     }      | dict literal                 |
        +-------------+------------+------------------------------+
        |     '       |     '      | string literal               |
        +-------------+------------+------------------------------+
        |     \"       |     \"      | string literal               |
        +-------------+------------+------------------------------+
        |    '''      |    '''     | code block with return       |
        +-------------+------------+------------------------------+
        |    \"\"\"      |    \"\"\"     | code block with return       |
        +-------------+------------+------------------------------+

        **other supported literals and values**

        literals with type restriction to a boolean type are evaluated as python expression.
        this way literal strings like 'True', 'False', '0' and '1' will be correctly recognized
        and converted into a boolean value.

        literal strings that representing a date value (with type restriction to either
        :class:`datetime.datetime` or :class:`datetime.date`) will be converted with the
        :func:`~ae.core.parse_date` function and should be formatted in one of the
        standard date formats (defined via the :mod:`ae.base` constants
        :data:`~ae.base.DATE_TIME_ISO` and :data:`~ae.base.DATE_ISO`).

        literals and values that are not in one of the above formats will finally be passed to
        the constructor of the restricted type class to try to convert them into their
        representing value.
       """
        check_val = self._literal_or_value
        msg = f"Literal {self._name} with value {check_val!r} "
        if self.type_mismatching_with(check_val):     # first or new late real value conversion/initialization
            try:
                check_val = self._determine_value(check_val)
            except Exception as ex:
                raise ValueError(msg + f"throw exception: {ex}") from ex

        self._chk_val_reset_else_set_type(check_val)
        if check_val is not None:
            if self._type and self.type_mismatching_with(check_val):
                raise ValueError(msg + f"type mismatch: {self._type} != {type(check_val)}")
            self._literal_or_value = check_val

        return self._literal_or_value

    @value.setter
    def value(self, lit_or_val: Any):
        if lit_or_val is not None:
            if isinstance(lit_or_val, bytes) and self._type != bytes:       # if not restricted to bytes
                lit_or_val = lit_or_val.decode('utf-8', DEF_ENCODE_ERRORS)  # ..then convert bytes to string
            self._literal_or_value = lit_or_val     # late evaluation: real value will be checked/converted by getter
            if not self._type and not isinstance(lit_or_val, str):          # set type if unset and no eval
                self._type = type(lit_or_val)

    def append_value(self, item_value: Any) -> Any:
        """ add new item to the list value of this Literal instance (lazy/late self.value getter call function pointer).

        :param item_value:  value of the item to be appended to the value of this Literal instance.
        :return:            the value (==list) of this Literal instance.

        this method gets e.g. used by the :class:`~.console.ConsoleApp` method
        :meth:`~.console.ConsoleApp.add_option` to have a function pointer to this
        literal value with lazy/late execution of the value getter (value.append cannot be used in this case
        because the list could have be changed before it get finally read/used).

        .. note::
           this method calls the append method of the value object and will therefore
           only work if the value is of type :class:`list` (or a compatible type).
        """
        self.value.append(item_value)
        return self.value

    def convert_value(self, lit_or_val: Any) -> Any:
        """ set/change the literal/value of this :class:`Literal` instance and return the represented value.

        :param lit_or_val:  the new value to be set.
        :return:            the final/converted value of this Literal instance.

        this method gets e.g. used by the :class:`~.console.ConsoleApp` method
        :meth:`~.console.ConsoleApp.add_option` to have a function pointer
        to let the ArgumentParser convert a configuration option literal into the
        represented value.
        """
        self.value = lit_or_val
        return self.value

    def type_mismatching_with(self, value: Any) -> bool:
        """ check if this literal instance would reject the passed value because of type mismatch.

        :param value:       new literal value.
        :return:            True if the passed value would have an type mismatch or if literal type is still not set,
                            else False.
        """
        return self._type != type(value)

    def _determine_value(self, lit_or_val: Any) -> Any:
        """ check passed value if it is still a literal determine the represented value.

        :param lit_or_val:  new literal value or the representing literal string.
        :return:            determined/converted value or self._lit_or_val if value could not be recognized/converted.
        """
        if isinstance(lit_or_val, str):
            func, eval_expr = evaluable_literal(lit_or_val)
            if func:
                lit_or_val = self._chk_val_reset_else_set_type(func(eval_expr))

        if self._type:
            if self.type_mismatching_with(lit_or_val) and isinstance(lit_or_val, str):
                if self._type == bool:
                    lit_or_val = bool(try_eval(lit_or_val))
                elif self._type in (datetime.date, datetime.datetime):
                    lit_or_val = parse_date(lit_or_val, ret_date=self._type == datetime.date)
                lit_or_val = self._chk_val_reset_else_set_type(lit_or_val)

            if self.type_mismatching_with(lit_or_val):          # finally try type conversion with type constructor
                lit_or_val = self._chk_val_reset_else_set_type(
                    try_call(self._type, lit_or_val, ignored_exceptions=(TypeError,)))  # ignore int(None) exception

        return lit_or_val

    def _chk_val_reset_else_set_type(self, value: Any) -> Any:
        """ reset and return passed value if is None, else determine value type and set type (if not already set).

        :param value:       just converted new literal value to be checked and if ok used to set an unset type.
        :return:            passed value or the stored literal/value if passed value is None.
        """
        if value is None or value is UNSET:
            value = self._literal_or_value  # literal evaluation failed, therefore reset to try with type conversion
        elif not self._type and value is not None and value is not UNSET:
            self._type = type(value)
        return value
