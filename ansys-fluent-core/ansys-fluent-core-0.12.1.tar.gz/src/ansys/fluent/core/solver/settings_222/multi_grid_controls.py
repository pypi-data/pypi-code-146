#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .multi_grid_controls_child import multi_grid_controls_child

class multi_grid_controls(NamedObject[multi_grid_controls_child], _CreatableNamedObjectMixin[multi_grid_controls_child]):
    """
    'multi_grid_controls' child.
    """

    fluent_name = "multi-grid-controls"

    child_object_type: multi_grid_controls_child = multi_grid_controls_child
    """
    child_object_type of multi_grid_controls.
    """
