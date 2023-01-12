#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .address import address
from .port import port
class start(Command):
    """
    'start' command.
    
    Parameters
    ----------
        address : str
            'address' child.
        port : int
            'port' child.
    
    """

    fluent_name = "start"

    argument_names = \
        ['address', 'port']

    address: address = address
    """
    address argument of start.
    """
    port: port = port
    """
    port argument of start.
    """
