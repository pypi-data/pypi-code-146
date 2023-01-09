#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .basic_info import basic_info
from .disk_origin import disk_origin
from .disk_orientation import disk_orientation
from .disk_id import disk_id
from .blade_pitch_angles import blade_pitch_angles
from .blade_flap_angles import blade_flap_angles
from .tip_loss import tip_loss
class general(Group):
    """
    Menu to define the rotor general information.
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "general"

    child_names = \
        ['basic_info', 'disk_origin', 'disk_orientation', 'disk_id',
         'blade_pitch_angles', 'blade_flap_angles', 'tip_loss']

    basic_info: basic_info = basic_info
    """
    basic_info child of general.
    """
    disk_origin: disk_origin = disk_origin
    """
    disk_origin child of general.
    """
    disk_orientation: disk_orientation = disk_orientation
    """
    disk_orientation child of general.
    """
    disk_id: disk_id = disk_id
    """
    disk_id child of general.
    """
    blade_pitch_angles: blade_pitch_angles = blade_pitch_angles
    """
    blade_pitch_angles child of general.
    """
    blade_flap_angles: blade_flap_angles = blade_flap_angles
    """
    blade_flap_angles child of general.
    """
    tip_loss: tip_loss = tip_loss
    """
    tip_loss child of general.
    """
