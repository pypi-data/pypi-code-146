#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .neutral_involved_interaction import neutral_involved_interaction
from .charged_particle_interaction import charged_particle_interaction
class child_object_type_child(Group):
    """
    'child_object_type' of child_object_type.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'neutral_involved_interaction',
         'charged_particle_interaction']

    option: option = option
    """
    option child of child_object_type_child.
    """
    neutral_involved_interaction: neutral_involved_interaction = neutral_involved_interaction
    """
    neutral_involved_interaction child of child_object_type_child.
    """
    charged_particle_interaction: charged_particle_interaction = charged_particle_interaction
    """
    charged_particle_interaction child of child_object_type_child.
    """
