#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sample import sample
from .variable import variable
class compute_sample(Command):
    """
    Compute minimum/maximum of a sample variable.
    
    Parameters
    ----------
        sample : str
            'sample' child.
        variable : str
            'variable' child.
    
    """

    fluent_name = "compute-sample"

    argument_names = \
        ['sample', 'variable']

    sample: sample = sample
    """
    sample argument of compute_sample.
    """
    variable: variable = variable
    """
    variable argument of compute_sample.
    """
