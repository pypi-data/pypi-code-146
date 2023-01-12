#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name import file_name
class replace_mesh(Command):
    """
    'replace_mesh' command.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "replace-mesh"

    argument_names = \
        ['file_name']

    file_name: file_name = file_name
    """
    file_name argument of replace_mesh.
    """
