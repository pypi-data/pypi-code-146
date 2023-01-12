#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .number_of_partitions import number_of_partitions
class combine_partition(Command):
    """
    Merge every N partitions.
    
    Parameters
    ----------
        number_of_partitions : int
            'number_of_partitions' child.
    
    """

    fluent_name = "combine-partition"

    argument_names = \
        ['number_of_partitions']

    number_of_partitions: number_of_partitions = number_of_partitions
    """
    number_of_partitions argument of combine_partition.
    """
