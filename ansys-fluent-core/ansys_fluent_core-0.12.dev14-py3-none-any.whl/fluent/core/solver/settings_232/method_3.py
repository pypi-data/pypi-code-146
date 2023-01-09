#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .partition_method import partition_method
from .count import count
class method(Command):
    """
    Partition the domain.
    
    Parameters
    ----------
        partition_method : str
            'partition_method' child.
        count : int
            'count' child.
    
    """

    fluent_name = "method"

    argument_names = \
        ['partition_method', 'count']

    partition_method: partition_method = partition_method
    """
    partition_method argument of method.
    """
    count: count = count
    """
    count argument of method.
    """
