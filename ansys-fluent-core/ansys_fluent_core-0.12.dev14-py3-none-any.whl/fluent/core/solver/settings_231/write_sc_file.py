#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name import file_name
from .overwrite import overwrite
class write_sc_file(Command):
    """
    Write a Fluent Input File for System Coupling.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "write-sc-file"

    argument_names = \
        ['file_name', 'overwrite']

    file_name: file_name = file_name
    """
    file_name argument of write_sc_file.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of write_sc_file.
    """
