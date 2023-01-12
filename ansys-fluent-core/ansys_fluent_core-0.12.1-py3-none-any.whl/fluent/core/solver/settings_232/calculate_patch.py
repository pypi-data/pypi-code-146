#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .domain import domain
from .cell_zones_1 import cell_zones
from .register_id import register_id
from .variable import variable
from .patch_velocity import patch_velocity
from .use_custom_field_function import use_custom_field_function
from .custom_field_function_name import custom_field_function_name
from .value import value
class calculate_patch(Command):
    """
    Patch a value for a flow variable in the domain.
    
    Parameters
    ----------
        domain : str
            'domain' child.
        cell_zones : typing.List[str]
            'cell_zones' child.
        register_id : typing.List[str]
            'register_id' child.
        variable : str
            'variable' child.
        patch_velocity : bool
            'patch_velocity' child.
        use_custom_field_function : bool
            'use_custom_field_function' child.
        custom_field_function_name : str
            'custom_field_function_name' child.
        value : real
            'value' child.
    
    """

    fluent_name = "calculate-patch"

    argument_names = \
        ['domain', 'cell_zones', 'register_id', 'variable', 'patch_velocity',
         'use_custom_field_function', 'custom_field_function_name', 'value']

    domain: domain = domain
    """
    domain argument of calculate_patch.
    """
    cell_zones: cell_zones = cell_zones
    """
    cell_zones argument of calculate_patch.
    """
    register_id: register_id = register_id
    """
    register_id argument of calculate_patch.
    """
    variable: variable = variable
    """
    variable argument of calculate_patch.
    """
    patch_velocity: patch_velocity = patch_velocity
    """
    patch_velocity argument of calculate_patch.
    """
    use_custom_field_function: use_custom_field_function = use_custom_field_function
    """
    use_custom_field_function argument of calculate_patch.
    """
    custom_field_function_name: custom_field_function_name = custom_field_function_name
    """
    custom_field_function_name argument of calculate_patch.
    """
    value: value = value
    """
    value argument of calculate_patch.
    """
