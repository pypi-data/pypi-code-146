#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x import x
from .x_2 import x_2
from .y import y
from .y_2 import y_2
from .z import z
from .z_2 import z_2
from .azimuthal_start_angle import azimuthal_start_angle
from .azimuthal_stop_angle import azimuthal_stop_angle
from .injection_surfaces import injection_surfaces
from .random_surface_inj import random_surface_inj
class location(Group):
    """
    'location' child.
    """

    fluent_name = "location"

    child_names = \
        ['x', 'x_2', 'y', 'y_2', 'z', 'z_2', 'azimuthal_start_angle',
         'azimuthal_stop_angle', 'injection_surfaces', 'random_surface_inj']

    x: x = x
    """
    x child of location.
    """
    x_2: x_2 = x_2
    """
    x_2 child of location.
    """
    y: y = y
    """
    y child of location.
    """
    y_2: y_2 = y_2
    """
    y_2 child of location.
    """
    z: z = z
    """
    z child of location.
    """
    z_2: z_2 = z_2
    """
    z_2 child of location.
    """
    azimuthal_start_angle: azimuthal_start_angle = azimuthal_start_angle
    """
    azimuthal_start_angle child of location.
    """
    azimuthal_stop_angle: azimuthal_stop_angle = azimuthal_stop_angle
    """
    azimuthal_stop_angle child of location.
    """
    injection_surfaces: injection_surfaces = injection_surfaces
    """
    injection_surfaces child of location.
    """
    random_surface_inj: random_surface_inj = random_surface_inj
    """
    random_surface_inj child of location.
    """
