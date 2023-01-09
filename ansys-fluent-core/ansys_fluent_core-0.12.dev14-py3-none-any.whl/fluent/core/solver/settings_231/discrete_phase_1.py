#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .histogram import histogram
from .sample_trajectories import sample_trajectories
from .summary import summary
from .extended_summary import extended_summary
from .zone_summaries_per_injection import zone_summaries_per_injection
class discrete_phase(Group):
    """
    'discrete_phase' child.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['histogram', 'sample_trajectories']

    histogram: histogram = histogram
    """
    histogram child of discrete_phase.
    """
    sample_trajectories: sample_trajectories = sample_trajectories
    """
    sample_trajectories child of discrete_phase.
    """
    command_names = \
        ['summary', 'extended_summary', 'zone_summaries_per_injection']

    summary: summary = summary
    """
    summary command of discrete_phase.
    """
    extended_summary: extended_summary = extended_summary
    """
    extended_summary command of discrete_phase.
    """
    zone_summaries_per_injection: zone_summaries_per_injection = zone_summaries_per_injection
    """
    zone_summaries_per_injection command of discrete_phase.
    """
