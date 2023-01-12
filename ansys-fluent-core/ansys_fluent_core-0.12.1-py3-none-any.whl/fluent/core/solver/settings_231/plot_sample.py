#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .loaded_samples import loaded_samples
from .variable_to_sampled import variable_to_sampled
from .weighting_var import weighting_var
from .correlation_var import correlation_var
from .read_fn import read_fn
from .overwrite import overwrite
class plot_sample(Command):
    """
    'plot_sample' command.
    
    Parameters
    ----------
        loaded_samples : str
            'loaded_samples' child.
        variable_to_sampled : str
            'variable_to_sampled' child.
        weighting_var : str
            'weighting_var' child.
        correlation_var : str
            'correlation_var' child.
        read_fn : str
            'read_fn' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "plot-sample"

    argument_names = \
        ['loaded_samples', 'variable_to_sampled', 'weighting_var',
         'correlation_var', 'read_fn', 'overwrite']

    loaded_samples: loaded_samples = loaded_samples
    """
    loaded_samples argument of plot_sample.
    """
    variable_to_sampled: variable_to_sampled = variable_to_sampled
    """
    variable_to_sampled argument of plot_sample.
    """
    weighting_var: weighting_var = weighting_var
    """
    weighting_var argument of plot_sample.
    """
    correlation_var: correlation_var = correlation_var
    """
    correlation_var argument of plot_sample.
    """
    read_fn: read_fn = read_fn
    """
    read_fn argument of plot_sample.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of plot_sample.
    """
