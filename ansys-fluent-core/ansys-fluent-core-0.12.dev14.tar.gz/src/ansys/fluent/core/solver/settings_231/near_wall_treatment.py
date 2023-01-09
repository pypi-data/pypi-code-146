#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .wall_function_1 import wall_function
from .law_of_the_wall import law_of_the_wall
from .enhanced_wall_treatment_options import enhanced_wall_treatment_options
from .wall_omega_treatment import wall_omega_treatment
class near_wall_treatment(Group):
    """
    'near_wall_treatment' child.
    """

    fluent_name = "near-wall-treatment"

    child_names = \
        ['wall_function', 'law_of_the_wall',
         'enhanced_wall_treatment_options', 'wall_omega_treatment']

    wall_function: wall_function = wall_function
    """
    wall_function child of near_wall_treatment.
    """
    law_of_the_wall: law_of_the_wall = law_of_the_wall
    """
    law_of_the_wall child of near_wall_treatment.
    """
    enhanced_wall_treatment_options: enhanced_wall_treatment_options = enhanced_wall_treatment_options
    """
    enhanced_wall_treatment_options child of near_wall_treatment.
    """
    wall_omega_treatment: wall_omega_treatment = wall_omega_treatment
    """
    wall_omega_treatment child of near_wall_treatment.
    """
