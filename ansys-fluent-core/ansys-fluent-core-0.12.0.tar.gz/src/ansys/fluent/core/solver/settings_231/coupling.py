#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .iter_per_coupling_count import iter_per_coupling_count
from .single_session_coupling import single_session_coupling
from .two_session_coupling import two_session_coupling
class coupling(Group):
    """
    'coupling' child.
    """

    fluent_name = "coupling"

    child_names = \
        ['iter_per_coupling_count', 'single_session_coupling',
         'two_session_coupling']

    iter_per_coupling_count: iter_per_coupling_count = iter_per_coupling_count
    """
    iter_per_coupling_count child of coupling.
    """
    single_session_coupling: single_session_coupling = single_session_coupling
    """
    single_session_coupling child of coupling.
    """
    two_session_coupling: two_session_coupling = two_session_coupling
    """
    two_session_coupling child of coupling.
    """
