#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .start_time import start_time
from .stop_time import stop_time
class times(Group):
    """
    'times' child.
    """

    fluent_name = "times"

    child_names = \
        ['start_time', 'stop_time']

    start_time: start_time = start_time
    """
    start_time child of times.
    """
    stop_time: stop_time = stop_time
    """
    stop_time child of times.
    """
