#!/usr/bin/env python

from .elements import mass_dict
from .molecular_formula import MolecularFormula

e = 5.4857990946e-4
p = 1.007276466812
n = 1.00866491600


def of(mf, **specialisation):
    value = MolecularFormula(mf).mass(**specialisation)
    if value is None:
        raise ValueError(f"formula '{mf}' is not valid")
    return value


def __dir__():
    """forward attributes for autocompletion"""
    return list(mass_dict.keys())


locals().update(mass_dict)
