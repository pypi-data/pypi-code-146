#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .phase_child_23 import phase_child

class phase(NamedObject[phase_child], _CreatableNamedObjectMixin[phase_child]):
    """
    'phase' child.
    """

    fluent_name = "phase"

    child_object_type: phase_child = phase_child
    """
    child_object_type of phase.
    """
