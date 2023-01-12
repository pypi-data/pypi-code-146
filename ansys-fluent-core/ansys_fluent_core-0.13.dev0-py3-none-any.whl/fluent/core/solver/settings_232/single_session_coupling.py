#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method_4 import method
from .type_1 import type
from .interval_1 import interval
from .frequency_1 import frequency
class single_session_coupling(Group):
    """
    'single_session_coupling' child.
    """

    fluent_name = "single-session-coupling"

    child_names = \
        ['method', 'type', 'interval', 'frequency']

    method: method = method
    """
    method child of single_session_coupling.
    """
    type: type = type
    """
    type child of single_session_coupling.
    """
    interval: interval = interval
    """
    interval child of single_session_coupling.
    """
    frequency: frequency = frequency
    """
    frequency child of single_session_coupling.
    """
