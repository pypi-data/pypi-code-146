#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use_enhancement import use_enhancement
from .aspect_ratio_1 import aspect_ratio
class stretched_mesh_enhancement(Group):
    """
    Enhancement for mesh with stretched cells.
    """

    fluent_name = "stretched-mesh-enhancement"

    child_names = \
        ['use_enhancement', 'aspect_ratio']

    use_enhancement: use_enhancement = use_enhancement
    """
    use_enhancement child of stretched_mesh_enhancement.
    """
    aspect_ratio: aspect_ratio = aspect_ratio
    """
    aspect_ratio child of stretched_mesh_enhancement.
    """
