#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .field import field
from .option_10 import option
from .scaling import scaling
from .derivative import derivative
from .size_ratio import size_ratio
from .create_volume_surface import create_volume_surface
class field_value(Group):
    """
    'field_value' child.
    """

    fluent_name = "field-value"

    child_names = \
        ['field', 'option', 'scaling', 'derivative', 'size_ratio',
         'create_volume_surface']

    field: field = field
    """
    field child of field_value.
    """
    option: option = option
    """
    option child of field_value.
    """
    scaling: scaling = scaling
    """
    scaling child of field_value.
    """
    derivative: derivative = derivative
    """
    derivative child of field_value.
    """
    size_ratio: size_ratio = size_ratio
    """
    size_ratio child of field_value.
    """
    create_volume_surface: create_volume_surface = create_volume_surface
    """
    create_volume_surface child of field_value.
    """
