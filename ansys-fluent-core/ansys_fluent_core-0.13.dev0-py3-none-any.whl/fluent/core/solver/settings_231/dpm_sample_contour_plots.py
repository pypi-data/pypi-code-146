#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .select_sample import select_sample
from .plotting_grid_interval_size import plotting_grid_interval_size
from .prepare_expressions import prepare_expressions
class dpm_sample_contour_plots(Group):
    """
    'dpm_sample_contour_plots' child.
    """

    fluent_name = "dpm-sample-contour-plots"

    child_names = \
        ['select_sample', 'plotting_grid_interval_size']

    select_sample: select_sample = select_sample
    """
    select_sample child of dpm_sample_contour_plots.
    """
    plotting_grid_interval_size: plotting_grid_interval_size = plotting_grid_interval_size
    """
    plotting_grid_interval_size child of dpm_sample_contour_plots.
    """
    command_names = \
        ['prepare_expressions']

    prepare_expressions: prepare_expressions = prepare_expressions
    """
    prepare_expressions command of dpm_sample_contour_plots.
    """
