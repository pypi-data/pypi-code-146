#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x_axis_2 import x_axis
from .y_axis_2 import y_axis
class log_scale(Group):
    """
    'log_scale' child.
    """

    fluent_name = "log-scale"

    child_names = \
        ['x_axis', 'y_axis']

    x_axis: x_axis = x_axis
    """
    x_axis child of log_scale.
    """
    y_axis: y_axis = y_axis
    """
    y_axis child of log_scale.
    """
