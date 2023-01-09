#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .inert_particle_child import inert_particle_child

class inert_particle(NamedObject[inert_particle_child], _CreatableNamedObjectMixin[inert_particle_child]):
    """
    'inert_particle' child.
    """

    fluent_name = "inert-particle"

    child_object_type: inert_particle_child = inert_particle_child
    """
    child_object_type of inert_particle.
    """
