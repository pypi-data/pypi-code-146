#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sample_var import sample_var
from .max_val import max_val
class set_maximum(Command):
    """
    'set_maximum' command.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        max_val : real
            'max_val' child.
    
    """

    fluent_name = "set-maximum"

    argument_names = \
        ['sample_var', 'max_val']

    sample_var: sample_var = sample_var
    """
    sample_var argument of set_maximum.
    """
    max_val: max_val = max_val
    """
    max_val argument of set_maximum.
    """
