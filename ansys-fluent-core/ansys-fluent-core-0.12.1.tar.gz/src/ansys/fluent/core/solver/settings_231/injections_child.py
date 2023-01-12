#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .particle_type import particle_type
from .material import material
from .reference_frame import reference_frame
from .number_of_streams import number_of_streams
from .injection_type import injection_type
from .interaction_1 import interaction
from .parcel_method import parcel_method
from .particle_reinjector import particle_reinjector
from .physical_models import physical_models
from .initial_props import initial_props
class injections_child(Group):
    """
    'child_object_type' of injections.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['particle_type', 'material', 'reference_frame', 'number_of_streams',
         'injection_type', 'interaction', 'parcel_method',
         'particle_reinjector', 'physical_models', 'initial_props']

    particle_type: particle_type = particle_type
    """
    particle_type child of injections_child.
    """
    material: material = material
    """
    material child of injections_child.
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of injections_child.
    """
    number_of_streams: number_of_streams = number_of_streams
    """
    number_of_streams child of injections_child.
    """
    injection_type: injection_type = injection_type
    """
    injection_type child of injections_child.
    """
    interaction: interaction = interaction
    """
    interaction child of injections_child.
    """
    parcel_method: parcel_method = parcel_method
    """
    parcel_method child of injections_child.
    """
    particle_reinjector: particle_reinjector = particle_reinjector
    """
    particle_reinjector child of injections_child.
    """
    physical_models: physical_models = physical_models
    """
    physical_models child of injections_child.
    """
    initial_props: initial_props = initial_props
    """
    initial_props child of injections_child.
    """
