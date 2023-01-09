#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .start import start
from .stop import stop
from .print_server_info import print_server_info
from .get_server_info import get_server_info
class web_server(Group):
    """
    'web_server' child.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop', 'print_server_info']

    start: start = start
    """
    start command of web_server.
    """
    stop: stop = stop
    """
    stop command of web_server.
    """
    print_server_info: print_server_info = print_server_info
    """
    print_server_info command of web_server.
    """
    query_names = \
        ['get_server_info']

    get_server_info: get_server_info = get_server_info
    """
    get_server_info query of web_server.
    """
