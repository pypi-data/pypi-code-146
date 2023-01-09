#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .hexahedron import hexahedron
from .sphere import sphere
from .cylinder import cylinder
from .boundary import boundary
from .limiters import limiters
from .field_value import field_value
from .residual import residual
from .volume_1 import volume
from .yplus_star import yplus_star
from .yplus_ystar import yplus_ystar
class type(Group):
    """
    'type' child.
    """

    fluent_name = "type"

    child_names = \
        ['option', 'hexahedron', 'sphere', 'cylinder', 'boundary', 'limiters',
         'field_value', 'residual', 'volume', 'yplus_star', 'yplus_ystar']

    option: option = option
    """
    option child of type.
    """
    hexahedron: hexahedron = hexahedron
    """
    hexahedron child of type.
    """
    sphere: sphere = sphere
    """
    sphere child of type.
    """
    cylinder: cylinder = cylinder
    """
    cylinder child of type.
    """
    boundary: boundary = boundary
    """
    boundary child of type.
    """
    limiters: limiters = limiters
    """
    limiters child of type.
    """
    field_value: field_value = field_value
    """
    field_value child of type.
    """
    residual: residual = residual
    """
    residual child of type.
    """
    volume: volume = volume
    """
    volume child of type.
    """
    yplus_star: yplus_star = yplus_star
    """
    yplus_star child of type.
    """
    yplus_ystar: yplus_ystar = yplus_ystar
    """
    yplus_ystar child of type.
    """
