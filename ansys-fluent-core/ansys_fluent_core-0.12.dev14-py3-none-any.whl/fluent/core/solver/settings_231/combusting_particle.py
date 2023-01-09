#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .combusting_particle_child import combusting_particle_child

class combusting_particle(NamedObject[combusting_particle_child], _CreatableNamedObjectMixin[combusting_particle_child]):
    """
    'combusting_particle' child.
    """

    fluent_name = "combusting-particle"

    child_object_type: combusting_particle_child = combusting_particle_child
    """
    child_object_type of combusting_particle.
    """
