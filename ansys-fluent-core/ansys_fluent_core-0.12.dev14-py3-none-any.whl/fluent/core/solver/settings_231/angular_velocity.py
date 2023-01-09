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
from .magnitude import magnitude
class angular_velocity(Group):
    """
    'angular_velocity' child.
    """

    fluent_name = "angular-velocity"

    child_names = \
        ['x', 'x_2', 'y', 'y_2', 'z', 'z_2', 'magnitude']

    x: x = x
    """
    x child of angular_velocity.
    """
    x_2: x_2 = x_2
    """
    x_2 child of angular_velocity.
    """
    y: y = y
    """
    y child of angular_velocity.
    """
    y_2: y_2 = y_2
    """
    y_2 child of angular_velocity.
    """
    z: z = z
    """
    z child of angular_velocity.
    """
    z_2: z_2 = z_2
    """
    z_2 child of angular_velocity.
    """
    magnitude: magnitude = magnitude
    """
    magnitude child of angular_velocity.
    """
