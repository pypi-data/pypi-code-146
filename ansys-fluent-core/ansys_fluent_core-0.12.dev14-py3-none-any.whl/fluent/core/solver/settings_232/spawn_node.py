#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .hostname import hostname
from .username import username
class spawn_node(Command):
    """
    Spawn a compute node process on a specified machine.
    
    Parameters
    ----------
        hostname : str
            'hostname' child.
        username : str
            'username' child.
    
    """

    fluent_name = "spawn-node"

    argument_names = \
        ['hostname', 'username']

    hostname: hostname = hostname
    """
    hostname argument of spawn_node.
    """
    username: username = username
    """
    username argument of spawn_node.
    """
