#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sample_var import sample_var
from .min_val import min_val
class set_minimum(Command):
    """
    Set the minimum value of the range to be considered for a specific variable in the data reduction.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        min_val : real
            'min_val' child.
    
    """

    fluent_name = "set-minimum"

    argument_names = \
        ['sample_var', 'min_val']

    sample_var: sample_var = sample_var
    """
    sample_var argument of set_minimum.
    """
    min_val: min_val = min_val
    """
    min_val argument of set_minimum.
    """
