"""
Generic classes for holding information on any cavcalc parameter type.
"""

import abc
import numpy as np

from .. import Q_
from .._exiters import (
    bug as _bug,
    quit_print as _quit_print,
)
from . import ParameterType, ParameterCategory
from ._maps import (
    NAME_PTYPE_MAP as _NAME_PTYPE_MAP,
    PTYPE_CATEGORY_MAP as _PTYPE_CATEGORY_MAP,
    PTYPE_DESCR_MAP as _PTYPE_DESCR_MAP,
    PTYPE_NAME_MAP as _PTYPE_NAME_MAP,
    PTYPE_SYMBOL_MAP as _PTYPE_SYMBOL_MAP,
)
from .tools import get_default_units


class Parameter(abc.ABC):
    """Abstract base class for cavity parameter instances."""

    def __init__(self, name_or_ptype, value: Q_ = None):
        if isinstance(name_or_ptype, str):
            self.__name = name_or_ptype
            self.__ptype = _NAME_PTYPE_MAP.get(self.name)
            if self.ptype is None:
                _bug(f"No ParameterType associated with name: {self.name}")
        elif isinstance(name_or_ptype, ParameterType):
            self.__ptype = name_or_ptype
            self.__name = _PTYPE_NAME_MAP.get(self.ptype)
            if self.name is None:
                _bug(f"No name associated with ParameterType: {self.ptype}")
        else:
            _bug(f"An object, {name_or_ptype}, of unrecognised type was passed to Parameter.")

        self.__category = _PTYPE_CATEGORY_MAP.get(self.ptype)
        if self.category is None:
            _bug(f"No ParameterCategory associated with name: {self.name}")

        if value is not None:
            if isinstance(self, ArgParameter):
                default_units = get_default_units(self.name) if not self.is_unitless else ""

                # For any quantity specified without units, choose the default units
                if value.unitless and not self.is_unitless:
                    value = Q_(value.m, default_units)

                if not value.check(default_units):
                    _quit_print(f"Invalid units ({value.units}) given for parameter {self.name}")

        self._value = value

    def __str__(self):
        if self.value is not None:
            if self.is_array:
                value_str = (
                    f"Values:\n"
                    f"\t\tfirst = {self.value.m[0]}\n"
                    f"\t\tlast  = {self.value.m[-1]}\n"
                    f"\t\tsize  = {self.value.m.size}"
                )
            else:
                value_str = f"Value: {self.value.m}"
        else:
            value_str = ""

        return (
            f"{self.description}:\n"
            f"\tCategory: {self.category}\n"
            f"\t{value_str}\n"
            f"\tUnits: {self.value.units}"
        )

    @property
    def category(self) -> ParameterCategory:
        """The :class:`.ParameterCategory` that this parameter belongs to."""
        return self.__category

    @property
    def compact_str(self):
        """A shortened string representation of the parameter with its value."""
        return self.name + f": {self.value:~}" if self.value is not None else ""

    @property
    def description(self):
        """A brief description of the parameter type."""
        return _PTYPE_DESCR_MAP[self.ptype]

    @property
    def has_angular_units(self):
        """Whether the units of this parameter are of angular type."""
        cat = self.category
        PC = ParameterCategory
        return cat == PC.Angle or cat == PC.Phase

    @property
    def has_frequency_units(self):
        """Whether the units of this parameter are of frequency type."""
        return self.category == ParameterCategory.Frequency

    @property
    def has_length_units(self):
        """Whether the units of this parameter are of length type.."""
        PC = ParameterCategory
        return self.category in (PC.BeamRadius, PC.Curvature, PC.Distance, PC.Wave)

    @property
    def is_array(self):
        """Whether the magnitude of the current value, if any, is array-like."""
        return self.value is not None and isinstance(self.value.m, np.ndarray)

    @property
    def is_scalar(self):
        """Whether the magnitude of the current value, if any, is not array-like."""
        return self.value is not None and not self.is_array

    @property
    def is_unitless(self):
        """Whether this parameter is a dimensionless type."""
        cat = self.category
        PC = ParameterCategory
        return cat == PC.Power or cat == PC.Stability

    @property
    def name(self):
        """The name of the parameter."""
        return self.__name

    @property
    def ptype(self) -> ParameterType:
        """The type of the parameter."""
        return self.__ptype

    @property
    def symbol_str(self):
        """A LaTeX style string representation of the parameter name."""
        return _PTYPE_SYMBOL_MAP[self.ptype]

    @property
    def value(self) -> Q_:
        """The current value of the parameter, as a pint Quantity."""
        return self._value


class ArgParameter(Parameter):
    """Cavity parameters which represent arguments given to cavcalc.

    .. note::

        You should never need to instantiate objects of this type manually. These
        are constructed during the argument parsing, and calculation process.
    """

    def __init__(self, name_or_ptype, value: Q_ = None, index: int = None, axis: int = None):
        super().__init__(name_or_ptype, value)
        self.__index = index
        self.__axis = axis

    @property
    def axis(self):
        """The axis that the parameter corresponds to, as an integer indexed from zero.

        If :attr:`.Parameter.is_scalar` is true, then this will be None. Otherwise, it
        is an integer.
        """
        return self.__axis

    @property
    def cli_form(self):
        """The name of the parameter in a CLI argument format."""
        return f"-{self.name}"

    @property
    def index(self):
        """The index of the argument in the sequence of specified args."""
        return self.__index


class TargetParameter(Parameter):
    """Cavity parameters which represent targets computed by cavcalc.

    .. note::

        You should never need to instantiate objects of this type manually. These
        are constructed during the calculation process.
    """

    def __init__(self, name_or_ptype, value: Q_ = None):
        super().__init__(name_or_ptype, value)
