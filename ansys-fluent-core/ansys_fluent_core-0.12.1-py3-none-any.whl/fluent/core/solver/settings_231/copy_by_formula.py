#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_1 import type
from .formula import formula
class copy_by_formula(Command):
    """
    Copy a material from the database (pick by formula).
    
    Parameters
    ----------
        type : str
            'type' child.
        formula : str
            'formula' child.
    
    """

    fluent_name = "copy-by-formula"

    argument_names = \
        ['type', 'formula']

    type: type = type
    """
    type argument of copy_by_formula.
    """
    formula: formula = formula
    """
    formula argument of copy_by_formula.
    """
