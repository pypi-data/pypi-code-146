#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .start import start
from .stop import stop
class web_server(Group):
    """
    'web_server' child.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop']

    start: start = start
    """
    start command of web_server.
    """
    stop: stop = stop
    """
    stop command of web_server.
    """
