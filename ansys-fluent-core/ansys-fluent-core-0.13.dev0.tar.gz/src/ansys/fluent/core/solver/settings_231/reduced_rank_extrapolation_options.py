#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .subspace_size import subspace_size
from .skip_iter_count import skip_iter_count
class reduced_rank_extrapolation_options(Group):
    """
    Reduced Rank Extrapolation options.
    """

    fluent_name = "reduced-rank-extrapolation-options"

    child_names = \
        ['subspace_size', 'skip_iter_count']

    subspace_size: subspace_size = subspace_size
    """
    subspace_size child of reduced_rank_extrapolation_options.
    """
    skip_iter_count: skip_iter_count = skip_iter_count
    """
    skip_iter_count child of reduced_rank_extrapolation_options.
    """
