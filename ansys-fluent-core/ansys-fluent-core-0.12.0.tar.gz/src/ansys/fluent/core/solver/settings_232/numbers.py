#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x_format import x_format
from .x_axis_precision import x_axis_precision
from .y_format import y_format
from .y_axis_precision import y_axis_precision
class numbers(Group):
    """
    'numbers' child.
    """

    fluent_name = "numbers"

    child_names = \
        ['x_format', 'x_axis_precision', 'y_format', 'y_axis_precision']

    x_format: x_format = x_format
    """
    x_format child of numbers.
    """
    x_axis_precision: x_axis_precision = x_axis_precision
    """
    x_axis_precision child of numbers.
    """
    y_format: y_format = y_format
    """
    y_format child of numbers.
    """
    y_axis_precision: y_axis_precision = y_axis_precision
    """
    y_axis_precision child of numbers.
    """
