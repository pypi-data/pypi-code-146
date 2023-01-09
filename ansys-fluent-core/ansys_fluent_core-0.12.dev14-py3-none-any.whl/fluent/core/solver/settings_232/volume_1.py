#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .volume_magnitude import volume_magnitude
from .volume_change import volume_change
class volume(Group):
    """
    'volume' child.
    """

    fluent_name = "volume"

    child_names = \
        ['option', 'volume_magnitude', 'volume_change']

    option: option = option
    """
    option child of volume.
    """
    volume_magnitude: volume_magnitude = volume_magnitude
    """
    volume_magnitude child of volume.
    """
    volume_change: volume_change = volume_change
    """
    volume_change child of volume.
    """
