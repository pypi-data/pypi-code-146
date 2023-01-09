#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .thread_number_control import thread_number_control
from .check_verbosity_1 import check_verbosity
from .partition_1 import partition
from .set_4 import set
from .load_balance import load_balance
from .multidomain import multidomain
from .network_1 import network
from .timer import timer
from .check_1 import check
from .show_connectivity import show_connectivity
from .latency import latency
from .bandwidth import bandwidth
class parallel(Group):
    """
    'parallel' child.
    """

    fluent_name = "parallel"

    child_names = \
        ['thread_number_control', 'check_verbosity', 'partition', 'set',
         'load_balance', 'multidomain', 'network', 'timer']

    thread_number_control: thread_number_control = thread_number_control
    """
    thread_number_control child of parallel.
    """
    check_verbosity: check_verbosity = check_verbosity
    """
    check_verbosity child of parallel.
    """
    partition: partition = partition
    """
    partition child of parallel.
    """
    set: set = set
    """
    set child of parallel.
    """
    load_balance: load_balance = load_balance
    """
    load_balance child of parallel.
    """
    multidomain: multidomain = multidomain
    """
    multidomain child of parallel.
    """
    network: network = network
    """
    network child of parallel.
    """
    timer: timer = timer
    """
    timer child of parallel.
    """
    command_names = \
        ['check', 'show_connectivity', 'latency', 'bandwidth']

    check: check = check
    """
    check command of parallel.
    """
    show_connectivity: show_connectivity = show_connectivity
    """
    show_connectivity command of parallel.
    """
    latency: latency = latency
    """
    latency command of parallel.
    """
    bandwidth: bandwidth = bandwidth
    """
    bandwidth command of parallel.
    """
