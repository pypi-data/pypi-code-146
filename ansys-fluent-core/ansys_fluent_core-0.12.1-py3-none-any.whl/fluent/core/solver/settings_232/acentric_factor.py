#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class acentric_factor(Group):
    """
    'acentric_factor' child.
    """

    fluent_name = "acentric-factor"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of acentric_factor.
    """
    value: value = value
    """
    value child of acentric_factor.
    """
