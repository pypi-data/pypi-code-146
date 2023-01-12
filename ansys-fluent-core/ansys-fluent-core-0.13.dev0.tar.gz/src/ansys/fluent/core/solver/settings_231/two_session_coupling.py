#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method_4 import method
from .type_1 import type
from .frequency_1 import frequency
class two_session_coupling(Group):
    """
    'two_session_coupling' child.
    """

    fluent_name = "two-session-coupling"

    child_names = \
        ['method', 'type', 'frequency']

    method: method = method
    """
    method child of two_session_coupling.
    """
    type: type = type
    """
    type child of two_session_coupling.
    """
    frequency: frequency = frequency
    """
    frequency child of two_session_coupling.
    """
