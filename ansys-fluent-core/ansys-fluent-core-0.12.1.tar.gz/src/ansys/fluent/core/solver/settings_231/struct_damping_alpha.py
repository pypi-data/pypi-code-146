#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class struct_damping_alpha(Group):
    """
    'struct_damping_alpha' child.
    """

    fluent_name = "struct-damping-alpha"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of struct_damping_alpha.
    """
    value: value = value
    """
    value child of struct_damping_alpha.
    """
