#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sample_var import sample_var
from .reset_range import reset_range
class reset_min_and_max(Command):
    """
    Reset the min and max values of the range to be considered for a specific variable in the data reduction.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        reset_range : bool
            'reset_range' child.
    
    """

    fluent_name = "reset-min-and-max"

    argument_names = \
        ['sample_var', 'reset_range']

    sample_var: sample_var = sample_var
    """
    sample_var argument of reset_min_and_max.
    """
    reset_range: reset_range = reset_range
    """
    reset_range argument of reset_min_and_max.
    """
