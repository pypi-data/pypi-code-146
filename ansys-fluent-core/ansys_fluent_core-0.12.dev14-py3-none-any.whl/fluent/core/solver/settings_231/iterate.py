#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .iter_count_3 import iter_count
class iterate(Command):
    """
    Perform a specified number of iterations.
    
    Parameters
    ----------
        iter_count : int
            Set incremental number of time steps.
    
    """

    fluent_name = "iterate"

    argument_names = \
        ['iter_count']

    iter_count: iter_count = iter_count
    """
    iter_count argument of iterate.
    """
