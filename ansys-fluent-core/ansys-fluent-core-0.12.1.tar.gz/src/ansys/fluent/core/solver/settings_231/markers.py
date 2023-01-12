#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .markers_child import markers_child

class markers(ListObject[markers_child]):
    """
    'markers' child.
    """

    fluent_name = "markers"

    child_object_type: markers_child = markers_child
    """
    child_object_type of markers.
    """
