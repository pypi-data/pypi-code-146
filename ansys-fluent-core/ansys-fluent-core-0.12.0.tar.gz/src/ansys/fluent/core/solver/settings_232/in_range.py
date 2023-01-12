#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .value1 import value1
from .value2 import value2
class in_range(Group):
    """
    'in_range' child.
    """

    fluent_name = "in-range"

    child_names = \
        ['value1', 'value2']

    value1: value1 = value1
    """
    value1 child of in_range.
    """
    value2: value2 = value2
    """
    value2 child of in_range.
    """
