#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .flow_rate import flow_rate
from .flow_rate_2 import flow_rate_2
from .total_flow_rate import total_flow_rate
from .scale_by_area import scale_by_area
class flow_rate(Group):
    """
    'flow_rate' child.
    """

    fluent_name = "flow-rate"

    child_names = \
        ['flow_rate', 'flow_rate_2', 'total_flow_rate', 'scale_by_area']

    flow_rate: flow_rate = flow_rate
    """
    flow_rate child of flow_rate.
    """
    flow_rate_2: flow_rate_2 = flow_rate_2
    """
    flow_rate_2 child of flow_rate.
    """
    total_flow_rate: total_flow_rate = total_flow_rate
    """
    total_flow_rate child of flow_rate.
    """
    scale_by_area: scale_by_area = scale_by_area
    """
    scale_by_area child of flow_rate.
    """
