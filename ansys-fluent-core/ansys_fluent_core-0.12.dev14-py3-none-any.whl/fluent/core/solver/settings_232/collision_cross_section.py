#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .cross_section_multicomponent import cross_section_multicomponent
class collision_cross_section(Group):
    """
    'collision_cross_section' child.
    """

    fluent_name = "collision-cross-section"

    child_names = \
        ['option', 'cross_section_multicomponent']

    option: option = option
    """
    option child of collision_cross_section.
    """
    cross_section_multicomponent: cross_section_multicomponent = cross_section_multicomponent
    """
    cross_section_multicomponent child of collision_cross_section.
    """
