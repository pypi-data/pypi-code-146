#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .merge_small_regions import merge_small_regions
from .max_merge_iterations import max_merge_iterations
class merge(Group):
    """
    Set partition merging optimization.
    """

    fluent_name = "merge"

    child_names = \
        ['merge_small_regions', 'max_merge_iterations']

    merge_small_regions: merge_small_regions = merge_small_regions
    """
    merge_small_regions child of merge.
    """
    max_merge_iterations: max_merge_iterations = max_merge_iterations
    """
    max_merge_iterations child of merge.
    """
