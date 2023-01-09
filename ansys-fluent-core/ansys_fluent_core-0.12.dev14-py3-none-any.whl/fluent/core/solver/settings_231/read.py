#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_type import file_type
from .file_name_1 import file_name
class read(Command):
    """
    'read' command.
    
    Parameters
    ----------
        file_type : str
            'file_type' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "read"

    argument_names = \
        ['file_type', 'file_name']

    file_type: file_type = file_type
    """
    file_type argument of read.
    """
    file_name: file_name = file_name
    """
    file_name argument of read.
    """
