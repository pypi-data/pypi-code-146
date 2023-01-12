#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .compressible_liquid import compressible_liquid
from .user_defined_function import user_defined_function
from .value import value
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'compressible_liquid', 'user_defined_function', 'value']

    option: option = option
    """
    option child of density.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of density.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of density.
    """
    value: value = value
    """
    value child of density.
    """
