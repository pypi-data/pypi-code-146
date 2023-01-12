#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .proc_statistics import proc_statistics
from .sys_statistics import sys_statistics
from .gpgpu_statistics import gpgpu_statistics
from .time_statistics import time_statistics
class system(Group):
    """
    'system' child.
    """

    fluent_name = "system"

    command_names = \
        ['proc_statistics', 'sys_statistics', 'gpgpu_statistics',
         'time_statistics']

    proc_statistics: proc_statistics = proc_statistics
    """
    proc_statistics command of system.
    """
    sys_statistics: sys_statistics = sys_statistics
    """
    sys_statistics command of system.
    """
    gpgpu_statistics: gpgpu_statistics = gpgpu_statistics
    """
    gpgpu_statistics command of system.
    """
    time_statistics: time_statistics = time_statistics
    """
    time_statistics command of system.
    """
