#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .histogram_options import histogram_options
from .histogram_parameters import histogram_parameters
from .plot_write_sample import plot_write_sample
from .reduction import reduction
from .dpm_sample_contour_plots import dpm_sample_contour_plots
from .compute_sample import compute_sample
from .delete_sample import delete_sample
from .list_samples import list_samples
from .read_sample_file import read_sample_file
class histogram(Group):
    """
    'histogram' child.
    """

    fluent_name = "histogram"

    child_names = \
        ['histogram_options', 'histogram_parameters', 'plot_write_sample',
         'reduction', 'dpm_sample_contour_plots']

    histogram_options: histogram_options = histogram_options
    """
    histogram_options child of histogram.
    """
    histogram_parameters: histogram_parameters = histogram_parameters
    """
    histogram_parameters child of histogram.
    """
    plot_write_sample: plot_write_sample = plot_write_sample
    """
    plot_write_sample child of histogram.
    """
    reduction: reduction = reduction
    """
    reduction child of histogram.
    """
    dpm_sample_contour_plots: dpm_sample_contour_plots = dpm_sample_contour_plots
    """
    dpm_sample_contour_plots child of histogram.
    """
    command_names = \
        ['compute_sample', 'delete_sample', 'list_samples',
         'read_sample_file']

    compute_sample: compute_sample = compute_sample
    """
    compute_sample command of histogram.
    """
    delete_sample: delete_sample = delete_sample
    """
    delete_sample command of histogram.
    """
    list_samples: list_samples = list_samples
    """
    list_samples command of histogram.
    """
    read_sample_file: read_sample_file = read_sample_file
    """
    read_sample_file command of histogram.
    """
