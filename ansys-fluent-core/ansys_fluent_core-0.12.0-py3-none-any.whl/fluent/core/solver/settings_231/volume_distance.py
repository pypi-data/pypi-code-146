#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .boundary_volume import boundary_volume
from .volume_growth import volume_growth
class volume_distance(Group):
    """
    'volume_distance' child.
    """

    fluent_name = "volume-distance"

    child_names = \
        ['boundary_volume', 'volume_growth']

    boundary_volume: boundary_volume = boundary_volume
    """
    boundary_volume child of volume_distance.
    """
    volume_growth: volume_growth = volume_growth
    """
    volume_growth child of volume_distance.
    """
