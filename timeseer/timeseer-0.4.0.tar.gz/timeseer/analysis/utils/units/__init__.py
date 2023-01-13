"""Utility functions for unit conversions."""

import re
from pathlib import Path
import numpy as np
from pint import UnitRegistry, UndefinedUnitError, DefinitionSyntaxError


def get_unit_registry() -> UnitRegistry:
    """Return a pint UnitRegistry configured for Timeseer."""
    return UnitRegistry(str(Path(__file__).parent.resolve()) + "/default_replace.txt")


def clean_unit_string(unit: str) -> str:
    """Clean up the unit value for parsing in pint."""
    return re.sub(r"\s+", "_", unit.strip())


def get_dimension(unit):
    """Get dimensionality using pint library"""
    ureg = get_unit_registry()
    try:
        return ureg.get_dimensionality(clean_unit_string(unit))
    except (
        UndefinedUnitError,
        AttributeError,
        TypeError,
        ValueError,
        KeyError,
        DefinitionSyntaxError,
    ):
        return "Unknown"


def get_symbol(unit):
    """Get symbol using pint library"""
    ureg = get_unit_registry()
    try:
        return ureg.get_symbol(clean_unit_string(unit))
    except (
        UndefinedUnitError,
        AttributeError,
        TypeError,
        ValueError,
        KeyError,
        DefinitionSyntaxError,
    ):
        return "Unknown"


def get_limited_units():
    """List of units and dimensions where sensible limits are known"""
    ureg = get_unit_registry()
    units = [
        "hertz",
    ]
    dimensions = [
        # "meter",
        "kelvin",
        "second",
        # "ampere",
        "candela",
        "gram",
        "mole",
        "unit",
        "pH",
        "m2",
        "liter",
        # "kph",
        # "galileo",
        "newton",
        "joule",
        "watt",
        "water",
        # "pascal",
        "foot_pound",
        "poise",
        "stokes",
        "rhe",
        "particle",
        "molar",
        "katal",
        "clausius",
        "entropy_unit",
        # "curie",
        "langley",
        "nit",
        "lumen",
        "lux",
        "a_u_intensity",
        # "volt",
        "ohm",
        "siemens",
        "henry",
        "weber",
        "tesla",
        # "bohr_magneton",
    ]
    units_zero_min = [ureg.get_symbol(unit) for unit in units]
    dimensions_zero_min = [
        ureg.get_dimensionality(dimension) for dimension in dimensions
    ]
    return units_zero_min, dimensions_zero_min


def get_unit_range(unit):
    """Returns min and max value for general case of units with known limits
    and considering the special cases."""
    min_value = 0
    max_value = np.inf
    if get_dimension(unit) == get_dimension("pH"):
        max_value = 14
    if get_symbol(unit) == get_symbol("C"):
        min_value = -273.15
    if get_symbol(unit) == get_symbol("F"):
        min_value = -459.67
    return min_value, max_value
