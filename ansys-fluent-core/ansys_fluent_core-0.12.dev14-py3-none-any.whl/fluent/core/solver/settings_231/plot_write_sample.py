#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .plot_sample import plot_sample
from .write_sample import write_sample
class plot_write_sample(Group):
    """
    'plot_write_sample' child.
    """

    fluent_name = "plot-write-sample"

    command_names = \
        ['plot_sample', 'write_sample']

    plot_sample: plot_sample = plot_sample
    """
    plot_sample command of plot_write_sample.
    """
    write_sample: write_sample = write_sample
    """
    write_sample command of plot_write_sample.
    """
