#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .shell_conduction_child import shell_conduction_child

class shell_conduction(ListObject[shell_conduction_child]):
    """
    'shell_conduction' child.
    """

    fluent_name = "shell-conduction"

    child_object_type: shell_conduction_child = shell_conduction_child
    """
    child_object_type of shell_conduction.
    """
