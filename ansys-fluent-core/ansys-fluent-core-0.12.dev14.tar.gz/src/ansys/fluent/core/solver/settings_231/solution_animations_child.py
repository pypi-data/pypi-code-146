#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .animate_on import animate_on
from .frequency_1 import frequency
from .flow_time_frequency import flow_time_frequency
from .frequency_of import frequency_of
from .storage_type import storage_type
from .storage_dir import storage_dir
from .window_id import window_id
from .view import view
from .use_raytracing import use_raytracing
from .display_2 import display
class solution_animations_child(Group):
    """
    'child_object_type' of solution_animations.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'animate_on', 'frequency', 'flow_time_frequency',
         'frequency_of', 'storage_type', 'storage_dir', 'window_id', 'view',
         'use_raytracing']

    name: name = name
    """
    name child of solution_animations_child.
    """
    animate_on: animate_on = animate_on
    """
    animate_on child of solution_animations_child.
    """
    frequency: frequency = frequency
    """
    frequency child of solution_animations_child.
    """
    flow_time_frequency: flow_time_frequency = flow_time_frequency
    """
    flow_time_frequency child of solution_animations_child.
    """
    frequency_of: frequency_of = frequency_of
    """
    frequency_of child of solution_animations_child.
    """
    storage_type: storage_type = storage_type
    """
    storage_type child of solution_animations_child.
    """
    storage_dir: storage_dir = storage_dir
    """
    storage_dir child of solution_animations_child.
    """
    window_id: window_id = window_id
    """
    window_id child of solution_animations_child.
    """
    view: view = view
    """
    view child of solution_animations_child.
    """
    use_raytracing: use_raytracing = use_raytracing
    """
    use_raytracing child of solution_animations_child.
    """
    command_names = \
        ['display']

    display: display = display
    """
    display command of solution_animations_child.
    """
