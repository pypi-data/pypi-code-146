#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .case_frequency import case_frequency
from .data_frequency import data_frequency
from .root_name import root_name
from .retain_most_recent_files import retain_most_recent_files
from .max_files import max_files
from .append_file_name_with import append_file_name_with
from .save_data_file_every import save_data_file_every
class auto_save(Group):
    """
    'auto_save' child.
    """

    fluent_name = "auto-save"

    child_names = \
        ['case_frequency', 'data_frequency', 'root_name',
         'retain_most_recent_files', 'max_files', 'append_file_name_with',
         'save_data_file_every']

    case_frequency: case_frequency = case_frequency
    """
    case_frequency child of auto_save.
    """
    data_frequency: data_frequency = data_frequency
    """
    data_frequency child of auto_save.
    """
    root_name: root_name = root_name
    """
    root_name child of auto_save.
    """
    retain_most_recent_files: retain_most_recent_files = retain_most_recent_files
    """
    retain_most_recent_files child of auto_save.
    """
    max_files: max_files = max_files
    """
    max_files child of auto_save.
    """
    append_file_name_with: append_file_name_with = append_file_name_with
    """
    append_file_name_with child of auto_save.
    """
    save_data_file_every: save_data_file_every = save_data_file_every
    """
    save_data_file_every child of auto_save.
    """
