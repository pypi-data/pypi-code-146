#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .partition_mask import partition_mask
from .verbosity_9 import verbosity
from .time_out import time_out
from .fast_io import fast_io
class set(Group):
    """
    'set' child.
    """

    fluent_name = "set"

    child_names = \
        ['partition_mask', 'verbosity', 'time_out', 'fast_io']

    partition_mask: partition_mask = partition_mask
    """
    partition_mask child of set.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of set.
    """
    time_out: time_out = time_out
    """
    time_out child of set.
    """
    fast_io: fast_io = fast_io
    """
    fast_io child of set.
    """
