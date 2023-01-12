#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_auto_creation_of_scp_file import enable_auto_creation_of_scp_file
from .write_sc_file import write_sc_file
class sc_def_file_settings(Group):
    """
    File menu.
    """

    fluent_name = "sc-def-file-settings"

    child_names = \
        ['enable_auto_creation_of_scp_file']

    enable_auto_creation_of_scp_file: enable_auto_creation_of_scp_file = enable_auto_creation_of_scp_file
    """
    enable_auto_creation_of_scp_file child of sc_def_file_settings.
    """
    command_names = \
        ['write_sc_file']

    write_sc_file: write_sc_file = write_sc_file
    """
    write_sc_file command of sc_def_file_settings.
    """
