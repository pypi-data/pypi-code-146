#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .reset_statistics import reset_statistics
from .statistics_controls import statistics_controls
class statistics(Group):
    """
    Specify statistics parameter of sampling and averaging of flow and optical quantiies.
    """

    fluent_name = "statistics"

    child_names = \
        ['reset_statistics']

    reset_statistics: reset_statistics = reset_statistics
    """
    reset_statistics child of statistics.
    """
    command_names = \
        ['statistics_controls']

    statistics_controls: statistics_controls = statistics_controls
    """
    statistics_controls command of statistics.
    """
