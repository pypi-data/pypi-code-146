#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .uid import uid
from .options_10 import options
from .plot_direction import plot_direction
from .x_axis_function import x_axis_function
from .y_axis_function import y_axis_function
from .surfaces_list import surfaces_list
from .physics import physics
from .geometry_3 import geometry
from .surfaces import surfaces
from .axes import axes
from .curves import curves
from .display_2 import display
class xy_plot_child(Group):
    """
    'child_object_type' of xy_plot.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'plot_direction', 'x_axis_function',
         'y_axis_function', 'surfaces_list', 'physics', 'geometry',
         'surfaces', 'axes', 'curves']

    name: name = name
    """
    name child of xy_plot_child.
    """
    uid: uid = uid
    """
    uid child of xy_plot_child.
    """
    options: options = options
    """
    options child of xy_plot_child.
    """
    plot_direction: plot_direction = plot_direction
    """
    plot_direction child of xy_plot_child.
    """
    x_axis_function: x_axis_function = x_axis_function
    """
    x_axis_function child of xy_plot_child.
    """
    y_axis_function: y_axis_function = y_axis_function
    """
    y_axis_function child of xy_plot_child.
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of xy_plot_child.
    """
    physics: physics = physics
    """
    physics child of xy_plot_child.
    """
    geometry: geometry = geometry
    """
    geometry child of xy_plot_child.
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of xy_plot_child.
    """
    axes: axes = axes
    """
    axes child of xy_plot_child.
    """
    curves: curves = curves
    """
    curves child of xy_plot_child.
    """
    command_names = \
        ['display']

    display: display = display
    """
    display command of xy_plot_child.
    """
