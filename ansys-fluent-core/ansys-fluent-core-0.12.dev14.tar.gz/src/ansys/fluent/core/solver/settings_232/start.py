#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .session_name import session_name
from .port import port
from .port_span import port_span
from .address import address
class start(Command):
    """
    'start' command.
    
    Parameters
    ----------
        session_name : str
            'session_name' child.
        port : int
            'port' child.
        port_span : int
            'port_span' child.
        address : str
            'address' child.
    
    """

    fluent_name = "start"

    argument_names = \
        ['session_name', 'port', 'port_span', 'address']

    session_name: session_name = session_name
    """
    session_name argument of start.
    """
    port: port = port
    """
    port argument of start.
    """
    port_span: port_span = port_span
    """
    port_span argument of start.
    """
    address: address = address
    """
    address argument of start.
    """
