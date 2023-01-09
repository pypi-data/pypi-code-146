#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .only_list_case_boundaries import only_list_case_boundaries
from .use_inherent_material_color import use_inherent_material_color
from .reset import reset
class by_type(Group):
    """
    'by_type' child.
    """

    fluent_name = "by-type"

    child_names = \
        ['only_list_case_boundaries', 'use_inherent_material_color']

    only_list_case_boundaries: only_list_case_boundaries = only_list_case_boundaries
    """
    only_list_case_boundaries child of by_type.
    """
    use_inherent_material_color: use_inherent_material_color = use_inherent_material_color
    """
    use_inherent_material_color child of by_type.
    """
    command_names = \
        ['reset']

    reset: reset = reset
    """
    reset command of by_type.
    """
