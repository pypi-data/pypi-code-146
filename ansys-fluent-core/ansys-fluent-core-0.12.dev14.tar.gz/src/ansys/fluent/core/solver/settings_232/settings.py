#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_cgns_export_filetype import set_cgns_export_filetype
class settings(Group):
    """
    Enter the export settings menu.
    """

    fluent_name = "settings"

    command_names = \
        ['set_cgns_export_filetype']

    set_cgns_export_filetype: set_cgns_export_filetype = set_cgns_export_filetype
    """
    set_cgns_export_filetype command of settings.
    """
