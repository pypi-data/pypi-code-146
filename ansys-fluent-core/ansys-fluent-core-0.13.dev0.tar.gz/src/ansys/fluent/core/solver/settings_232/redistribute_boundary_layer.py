#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .thread_id import thread_id
from .growth_rate import growth_rate
class redistribute_boundary_layer(Command):
    """
    Enforce growth rate in boundary layer.
    
    Parameters
    ----------
        thread_id : int
            'thread_id' child.
        growth_rate : real
            'growth_rate' child.
    
    """

    fluent_name = "redistribute-boundary-layer"

    argument_names = \
        ['thread_id', 'growth_rate']

    thread_id: thread_id = thread_id
    """
    thread_id argument of redistribute_boundary_layer.
    """
    growth_rate: growth_rate = growth_rate
    """
    growth_rate argument of redistribute_boundary_layer.
    """
