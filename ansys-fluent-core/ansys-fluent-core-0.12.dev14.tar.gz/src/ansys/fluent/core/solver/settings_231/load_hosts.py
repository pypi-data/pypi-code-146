#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .host_file import host_file
class load_hosts(Command):
    """
    Read a hosts file.
    
    Parameters
    ----------
        host_file : str
            'host_file' child.
    
    """

    fluent_name = "load-hosts"

    argument_names = \
        ['host_file']

    host_file: host_file = host_file
    """
    host_file argument of load_hosts.
    """
