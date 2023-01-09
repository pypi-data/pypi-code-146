#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class youngs_modulus_0(Group):
    """
    'youngs_modulus_0' child.
    """

    fluent_name = "youngs-modulus-0"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of youngs_modulus_0.
    """
    value: value = value
    """
    value child of youngs_modulus_0.
    """
