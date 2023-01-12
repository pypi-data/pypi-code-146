#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .user_defined_function import user_defined_function
class latent_heat(Group):
    """
    'latent_heat' child.
    """

    fluent_name = "latent-heat"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of latent_heat.
    """
    value: value = value
    """
    value child of latent_heat.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of latent_heat.
    """
