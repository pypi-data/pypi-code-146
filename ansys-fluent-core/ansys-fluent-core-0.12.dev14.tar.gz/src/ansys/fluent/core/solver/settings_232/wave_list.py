#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .wave_list_child import wave_list_child

class wave_list(ListObject[wave_list_child]):
    """
    'wave_list' child.
    """

    fluent_name = "wave-list"

    child_object_type: wave_list_child = wave_list_child
    """
    child_object_type of wave_list.
    """
