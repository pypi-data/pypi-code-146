#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .spatial_discretization_limiter import spatial_discretization_limiter
from .pseudo_time_method_usage import pseudo_time_method_usage
class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['spatial_discretization_limiter', 'pseudo_time_method_usage']

    spatial_discretization_limiter: spatial_discretization_limiter = spatial_discretization_limiter
    """
    spatial_discretization_limiter child of expert.
    """
    pseudo_time_method_usage: pseudo_time_method_usage = pseudo_time_method_usage
    """
    pseudo_time_method_usage child of expert.
    """
