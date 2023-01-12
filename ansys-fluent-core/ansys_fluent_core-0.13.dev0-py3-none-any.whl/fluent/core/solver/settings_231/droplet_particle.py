#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .droplet_particle_child import droplet_particle_child

class droplet_particle(NamedObject[droplet_particle_child], _CreatableNamedObjectMixin[droplet_particle_child]):
    """
    'droplet_particle' child.
    """

    fluent_name = "droplet-particle"

    child_object_type: droplet_particle_child = droplet_particle_child
    """
    child_object_type of droplet_particle.
    """
