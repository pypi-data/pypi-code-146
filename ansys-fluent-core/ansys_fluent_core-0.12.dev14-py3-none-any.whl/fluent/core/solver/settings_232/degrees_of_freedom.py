#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class degrees_of_freedom(Group):
    """
    'degrees_of_freedom' child.
    """

    fluent_name = "degrees-of-freedom"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of degrees_of_freedom.
    """
    value: value = value
    """
    value child of degrees_of_freedom.
    """
