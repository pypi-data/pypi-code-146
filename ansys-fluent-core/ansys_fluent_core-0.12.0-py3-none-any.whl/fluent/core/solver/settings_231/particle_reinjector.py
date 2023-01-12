#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable import enable
from .time_delay import time_delay
class particle_reinjector(Group):
    """
    'particle_reinjector' child.
    """

    fluent_name = "particle-reinjector"

    child_names = \
        ['enable', 'time_delay']

    enable: enable = enable
    """
    enable child of particle_reinjector.
    """
    time_delay: time_delay = time_delay
    """
    time_delay child of particle_reinjector.
    """
