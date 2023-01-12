#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fluid_child import fluid_child

class droplet_particle(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'droplet_particle' child.
    """

    fluent_name = "droplet-particle"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of droplet_particle.
    """
