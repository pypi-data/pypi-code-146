#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .shell_script_path import shell_script_path
from .kill_all_nodes import kill_all_nodes
from .kill_node import kill_node
from .spawn_node import spawn_node
from .load_hosts import load_hosts
from .save_hosts import save_hosts
class network(Group):
    """
    Enter the network configuration menu.
    """

    fluent_name = "network"

    child_names = \
        ['shell_script_path']

    shell_script_path: shell_script_path = shell_script_path
    """
    shell_script_path child of network.
    """
    command_names = \
        ['kill_all_nodes', 'kill_node', 'spawn_node', 'load_hosts',
         'save_hosts']

    kill_all_nodes: kill_all_nodes = kill_all_nodes
    """
    kill_all_nodes command of network.
    """
    kill_node: kill_node = kill_node
    """
    kill_node command of network.
    """
    spawn_node: spawn_node = spawn_node
    """
    spawn_node command of network.
    """
    load_hosts: load_hosts = load_hosts
    """
    load_hosts command of network.
    """
    save_hosts: save_hosts = save_hosts
    """
    save_hosts command of network.
    """
