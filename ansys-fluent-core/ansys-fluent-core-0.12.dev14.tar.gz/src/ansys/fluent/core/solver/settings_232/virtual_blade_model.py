#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_4 import enable
from .mode import mode
from .disk import disk
from .list_disk_names import list_disk_names
class virtual_blade_model(Group):
    """
    Enter the vbm model menu.
    """

    fluent_name = "virtual-blade-model"

    child_names = \
        ['enable', 'mode', 'disk']

    enable: enable = enable
    """
    enable child of virtual_blade_model.
    """
    mode: mode = mode
    """
    mode child of virtual_blade_model.
    """
    disk: disk = disk
    """
    disk child of virtual_blade_model.
    """
    command_names = \
        ['list_disk_names']

    list_disk_names: list_disk_names = list_disk_names
    """
    list_disk_names command of virtual_blade_model.
    """
