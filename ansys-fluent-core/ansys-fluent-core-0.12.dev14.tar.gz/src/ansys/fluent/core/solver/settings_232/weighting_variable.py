#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .change_curr_sample import change_curr_sample
from .sample import sample
class weighting_variable(Command):
    """
    Choose the weighting variable for the averaging in each bin in the data reduction.
    
    Parameters
    ----------
        change_curr_sample : bool
            'change_curr_sample' child.
        sample : str
            'sample' child.
    
    """

    fluent_name = "weighting-variable"

    argument_names = \
        ['change_curr_sample', 'sample']

    change_curr_sample: change_curr_sample = change_curr_sample
    """
    change_curr_sample argument of weighting_variable.
    """
    sample: sample = sample
    """
    sample argument of weighting_variable.
    """
