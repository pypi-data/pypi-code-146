#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .yplus_1 import yplus
from .ystar import ystar
class option(Group):
    """
    'option' child.
    """

    fluent_name = "option"

    child_names = \
        ['option', 'yplus', 'ystar']

    option: option = option
    """
    option child of option.
    """
    yplus: yplus = yplus
    """
    yplus child of option.
    """
    ystar: ystar = ystar
    """
    ystar child of option.
    """
