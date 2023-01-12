#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .terminology import terminology
from .disk_normal_x import disk_normal_x
from .disk_normal_y import disk_normal_y
from .disk_normal_z import disk_normal_z
from .disk_pitch_angle import disk_pitch_angle
from .disk_bank_angle import disk_bank_angle
class disk_orientation(Group):
    """
    Menu to define the rotor disk orientation.
    
     - terminology      : the terminology to specify the rotor disk orientation: rotor-disk-angles / rotor-disk-normal, 
     - disk-normal-x/yz : rotor-disk-normal components, 
     - disk-pitch-angle : , 
     - disk-bank-angle : , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-orientation"

    child_names = \
        ['terminology', 'disk_normal_x', 'disk_normal_y', 'disk_normal_z',
         'disk_pitch_angle', 'disk_bank_angle']

    terminology: terminology = terminology
    """
    terminology child of disk_orientation.
    """
    disk_normal_x: disk_normal_x = disk_normal_x
    """
    disk_normal_x child of disk_orientation.
    """
    disk_normal_y: disk_normal_y = disk_normal_y
    """
    disk_normal_y child of disk_orientation.
    """
    disk_normal_z: disk_normal_z = disk_normal_z
    """
    disk_normal_z child of disk_orientation.
    """
    disk_pitch_angle: disk_pitch_angle = disk_pitch_angle
    """
    disk_pitch_angle child of disk_orientation.
    """
    disk_bank_angle: disk_bank_angle = disk_bank_angle
    """
    disk_bank_angle child of disk_orientation.
    """
