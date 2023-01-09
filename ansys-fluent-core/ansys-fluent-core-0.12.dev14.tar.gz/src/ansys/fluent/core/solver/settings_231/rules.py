#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x_axis_1 import x_axis
from .y_axis_1 import y_axis
class rules(Group):
    """
    'rules' child.
    """

    fluent_name = "rules"

    child_names = \
        ['x_axis', 'y_axis']

    x_axis: x_axis = x_axis
    """
    x_axis child of rules.
    """
    y_axis: y_axis = y_axis
    """
    y_axis child of rules.
    """
