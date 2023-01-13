"""
Functions for retrieving information on parameters, typically provided via
both str and :class:`.ParameterType` arguments.
"""

from . import ParameterType
from ._maps import (
    NAME_PTYPE_MAP as _NAME_PTYPE_MAP,
    PTYPE_NAME_MAP as _PTYPE_NAME_MAP,
)


def get_default_units(ptype):
    """Get the default units, as a string, of the given parameter type.

    The default units value is obtained from the loaded config file(s); i.e.
    the first instance of the corresponding option in the load order: current
    working directory -> user config directory -> package install location.

    Parameters
    ----------
    ptype : (str | :class:`.ParameterType`)
        The short-hand name (as it appears in the config file), or :class:`.ParameterType`,
        of the parameter.

    Returns
    -------
    units : (str | None)
        A string representing the units for the given parameter, or ``None``, if ``ptype``
        does not correspond to any valid option in any of the loaded config files.
    """
    from .. import _CONFIG

    if isinstance(ptype, ParameterType):
        return _CONFIG["units"].get(_PTYPE_NAME_MAP[ptype])

    return _CONFIG["units"].get(ptype)


def get_name(ptype: ParameterType):
    return _PTYPE_NAME_MAP.get(ptype)


def get_names():
    return tuple(_NAME_PTYPE_MAP.keys())


def get_type(name: str):
    return _NAME_PTYPE_MAP.get(name)


# TODO (sjr) Get rid of below eventually, as should be able to specify any
#            parameter as an arg or target


def get_valid_arguments():
    non_arg_ptypes = (
        ParameterType.FINESSE,
        ParameterType.FSR,
        ParameterType.FWHM,
        ParameterType.MODESEP,
        ParameterType.POLE,
        ParameterType.WAISTPOS,
    )
    return tuple(name for name in get_names() if get_type(name) not in non_arg_ptypes)


def get_valid_targets():
    non_tgt_ptypes = (
        ParameterType.CAV_LENGTH,
        ParameterType.LOSS_M1,
        ParameterType.LOSS_M2,
    )
    return tuple(name for name in get_names() if get_type(name) not in non_tgt_ptypes)
