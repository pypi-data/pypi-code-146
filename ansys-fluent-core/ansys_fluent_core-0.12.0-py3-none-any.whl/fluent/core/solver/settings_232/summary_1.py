#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .write_to_file import write_to_file
from .file_name_1 import file_name
from .overwrite import overwrite
class summary(Command):
    """
    Print report summary.
    
    Parameters
    ----------
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "summary"

    argument_names = \
        ['write_to_file', 'file_name', 'overwrite']

    write_to_file: write_to_file = write_to_file
    """
    write_to_file argument of summary.
    """
    file_name: file_name = file_name
    """
    file_name argument of summary.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of summary.
    """
