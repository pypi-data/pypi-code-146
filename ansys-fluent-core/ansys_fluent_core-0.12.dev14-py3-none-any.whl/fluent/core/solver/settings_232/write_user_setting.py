#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_1 import file_name
from .overwrite import overwrite
class write_user_setting(Command):
    """
    Write the contents of the Modified Settings Summary table to a file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "write-user-setting"

    argument_names = \
        ['file_name', 'overwrite']

    file_name: file_name = file_name
    """
    file_name argument of write_user_setting.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of write_user_setting.
    """
