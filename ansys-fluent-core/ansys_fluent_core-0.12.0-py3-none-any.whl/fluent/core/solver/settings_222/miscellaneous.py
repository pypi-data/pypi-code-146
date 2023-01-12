#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .compute_statistics import compute_statistics
from .statistics_level import statistics_level
class miscellaneous(Group):
    """
    'miscellaneous' child.
    """

    fluent_name = "miscellaneous"

    child_names = \
        ['compute_statistics', 'statistics_level']

    compute_statistics: compute_statistics = compute_statistics
    """
    compute_statistics child of miscellaneous.
    """
    statistics_level: statistics_level = statistics_level
    """
    statistics_level child of miscellaneous.
    """
