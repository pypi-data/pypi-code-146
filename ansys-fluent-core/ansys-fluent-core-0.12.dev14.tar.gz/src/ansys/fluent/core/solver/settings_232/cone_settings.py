#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .half_angle import half_angle
from .dispersion_angle import dispersion_angle
from .inner_radius import inner_radius
from .outer_radius import outer_radius
from .x_axis import x_axis
from .y_axis import y_axis
from .z_axis import z_axis
class cone_settings(Group):
    """
    'cone_settings' child.
    """

    fluent_name = "cone-settings"

    child_names = \
        ['half_angle', 'dispersion_angle', 'inner_radius', 'outer_radius',
         'x_axis', 'y_axis', 'z_axis']

    half_angle: half_angle = half_angle
    """
    half_angle child of cone_settings.
    """
    dispersion_angle: dispersion_angle = dispersion_angle
    """
    dispersion_angle child of cone_settings.
    """
    inner_radius: inner_radius = inner_radius
    """
    inner_radius child of cone_settings.
    """
    outer_radius: outer_radius = outer_radius
    """
    outer_radius child of cone_settings.
    """
    x_axis: x_axis = x_axis
    """
    x_axis child of cone_settings.
    """
    y_axis: y_axis = y_axis
    """
    y_axis child of cone_settings.
    """
    z_axis: z_axis = z_axis
    """
    z_axis child of cone_settings.
    """
