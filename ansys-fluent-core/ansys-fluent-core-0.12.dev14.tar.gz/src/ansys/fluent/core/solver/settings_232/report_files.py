#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_files_child import report_files_child

class report_files(NamedObject[report_files_child], _CreatableNamedObjectMixin[report_files_child]):
    """
    'report_files' child.
    """

    fluent_name = "report-files"

    child_object_type: report_files_child = report_files_child
    """
    child_object_type of report_files.
    """
