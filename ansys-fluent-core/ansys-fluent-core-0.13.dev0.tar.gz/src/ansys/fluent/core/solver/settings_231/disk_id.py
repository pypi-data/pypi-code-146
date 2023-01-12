#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .embedded_face_zone import embedded_face_zone
from .floating_surface import floating_surface
class disk_id(Group):
    """
    Menu to define the disk face/surface name:
    
     - embedded-face-zone: select embedded-face-zone name, 
     - floating-disk	: select floating-surface name, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-id"

    child_names = \
        ['embedded_face_zone', 'floating_surface']

    embedded_face_zone: embedded_face_zone = embedded_face_zone
    """
    embedded_face_zone child of disk_id.
    """
    floating_surface: floating_surface = floating_surface
    """
    floating_surface child of disk_id.
    """
