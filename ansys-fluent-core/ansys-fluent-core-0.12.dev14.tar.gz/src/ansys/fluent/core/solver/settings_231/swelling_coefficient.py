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
class swelling_coefficient(Group):
    """
    'swelling_coefficient' child.
    """

    fluent_name = "swelling-coefficient"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of swelling_coefficient.
    """
    value: value = value
    """
    value child of swelling_coefficient.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of swelling_coefficient.
    """
