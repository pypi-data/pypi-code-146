#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .auto import auto
from .set_3 import set
from .combine_partition import combine_partition
from .merge_clusters import merge_clusters
from .method_3 import method
from .print_partitions import print_partitions
from .print_active_partitions import print_active_partitions
from .print_stored_partitions import print_stored_partitions
from .reorder_partitions import reorder_partitions
from .reorder_partitions_to_architecture import reorder_partitions_to_architecture
from .smooth_partition import smooth_partition
from .use_stored_partitions import use_stored_partitions
class partition(Group):
    """
    Enter the partition domain menu.
    """

    fluent_name = "partition"

    child_names = \
        ['auto', 'set']

    auto: auto = auto
    """
    auto child of partition.
    """
    set: set = set
    """
    set child of partition.
    """
    command_names = \
        ['combine_partition', 'merge_clusters', 'method', 'print_partitions',
         'print_active_partitions', 'print_stored_partitions',
         'reorder_partitions', 'reorder_partitions_to_architecture',
         'smooth_partition', 'use_stored_partitions']

    combine_partition: combine_partition = combine_partition
    """
    combine_partition command of partition.
    """
    merge_clusters: merge_clusters = merge_clusters
    """
    merge_clusters command of partition.
    """
    method: method = method
    """
    method command of partition.
    """
    print_partitions: print_partitions = print_partitions
    """
    print_partitions command of partition.
    """
    print_active_partitions: print_active_partitions = print_active_partitions
    """
    print_active_partitions command of partition.
    """
    print_stored_partitions: print_stored_partitions = print_stored_partitions
    """
    print_stored_partitions command of partition.
    """
    reorder_partitions: reorder_partitions = reorder_partitions
    """
    reorder_partitions command of partition.
    """
    reorder_partitions_to_architecture: reorder_partitions_to_architecture = reorder_partitions_to_architecture
    """
    reorder_partitions_to_architecture command of partition.
    """
    smooth_partition: smooth_partition = smooth_partition
    """
    smooth_partition command of partition.
    """
    use_stored_partitions: use_stored_partitions = use_stored_partitions
    """
    use_stored_partitions command of partition.
    """
