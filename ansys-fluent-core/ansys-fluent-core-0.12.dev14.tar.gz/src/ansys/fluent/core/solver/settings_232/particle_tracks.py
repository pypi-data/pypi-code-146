#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .display_3 import display
from .history_filename import history_filename
from .report_default_variables import report_default_variables
from .track_single_particle_stream_1 import track_single_particle_stream
from .arrow_scale_1 import arrow_scale
from .arrow_space_1 import arrow_space
from .coarsen_factor import coarsen_factor
from .line_width_1 import line_width
class particle_tracks(Group):
    """
    'particle_tracks' child.
    """

    fluent_name = "particle-tracks"

    child_names = \
        ['display', 'history_filename', 'report_default_variables',
         'track_single_particle_stream', 'arrow_scale', 'arrow_space',
         'coarsen_factor', 'line_width']

    display: display = display
    """
    display child of particle_tracks.
    """
    history_filename: history_filename = history_filename
    """
    history_filename child of particle_tracks.
    """
    report_default_variables: report_default_variables = report_default_variables
    """
    report_default_variables child of particle_tracks.
    """
    track_single_particle_stream: track_single_particle_stream = track_single_particle_stream
    """
    track_single_particle_stream child of particle_tracks.
    """
    arrow_scale: arrow_scale = arrow_scale
    """
    arrow_scale child of particle_tracks.
    """
    arrow_space: arrow_space = arrow_space
    """
    arrow_space child of particle_tracks.
    """
    coarsen_factor: coarsen_factor = coarsen_factor
    """
    coarsen_factor child of particle_tracks.
    """
    line_width: line_width = line_width
    """
    line_width child of particle_tracks.
    """
