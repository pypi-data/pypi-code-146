#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .orthotropic_structure_ym import orthotropic_structure_ym
class struct_youngs_modulus(Group):
    """
    'struct_youngs_modulus' child.
    """

    fluent_name = "struct-youngs-modulus"

    child_names = \
        ['option', 'value', 'orthotropic_structure_ym']

    option: option = option
    """
    option child of struct_youngs_modulus.
    """
    value: value = value
    """
    value child of struct_youngs_modulus.
    """
    orthotropic_structure_ym: orthotropic_structure_ym = orthotropic_structure_ym
    """
    orthotropic_structure_ym child of struct_youngs_modulus.
    """
