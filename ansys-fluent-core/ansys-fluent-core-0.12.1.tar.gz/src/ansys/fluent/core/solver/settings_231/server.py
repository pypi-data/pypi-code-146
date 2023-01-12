#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .web_server import web_server
class server(Group):
    """
    'server' child.
    """

    fluent_name = "server"

    child_names = \
        ['web_server']

    web_server: web_server = web_server
    """
    web_server child of server.
    """
