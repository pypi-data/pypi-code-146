#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_list import file_name_list
class read_journal(Command):
    """
    Read a journal file.
    
    Parameters
    ----------
        file_name_list : typing.List[str]
            'file_name_list' child.
    
    """

    fluent_name = "read-journal"

    argument_names = \
        ['file_name_list']

    file_name_list: file_name_list = file_name_list
    """
    file_name_list argument of read_journal.
    """
