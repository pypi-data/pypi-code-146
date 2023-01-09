#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .outflow_child import outflow_child

class outflow(NamedObject[outflow_child], _NonCreatableNamedObjectMixin[outflow_child]):
    """
    'outflow' child.
    """

    fluent_name = "outflow"

    child_object_type: outflow_child = outflow_child
    """
    child_object_type of outflow.
    """
