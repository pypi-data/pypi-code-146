#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .disk_origin_x import disk_origin_x
from .disk_origin_y import disk_origin_y
from .disk_origin_z import disk_origin_z
class disk_origin(Group):
    """
    Menu to define the disk center coordinates.
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-origin"

    child_names = \
        ['disk_origin_x', 'disk_origin_y', 'disk_origin_z']

    disk_origin_x: disk_origin_x = disk_origin_x
    """
    disk_origin_x child of disk_origin.
    """
    disk_origin_y: disk_origin_y = disk_origin_y
    """
    disk_origin_y child of disk_origin.
    """
    disk_origin_z: disk_origin_z = disk_origin_z
    """
    disk_origin_z child of disk_origin.
    """
