#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .distance_option import distance_option
from .boundary_list import boundary_list
from .create_volume_surface import create_volume_surface
class boundary(Group):
    """
    'boundary' child.
    """

    fluent_name = "boundary"

    child_names = \
        ['distance_option', 'boundary_list', 'create_volume_surface']

    distance_option: distance_option = distance_option
    """
    distance_option child of boundary.
    """
    boundary_list: boundary_list = boundary_list
    """
    boundary_list child of boundary.
    """
    create_volume_surface: create_volume_surface = create_volume_surface
    """
    create_volume_surface child of boundary.
    """
