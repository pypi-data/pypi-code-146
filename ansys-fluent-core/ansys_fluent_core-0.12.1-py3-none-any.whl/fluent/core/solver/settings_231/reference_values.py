#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .area import area
from .depth import depth
from .density_6 import density
from .enthalpy import enthalpy
from .length import length
from .pressure import pressure
from .temperature_3 import temperature
from .yplus import yplus
from .velocity_2 import velocity
from .viscosity_3 import viscosity
from .zone import zone
from .compute import compute
from .list_val import list_val
class reference_values(Group):
    """
    'reference_values' child.
    """

    fluent_name = "reference-values"

    child_names = \
        ['area', 'depth', 'density', 'enthalpy', 'length', 'pressure',
         'temperature', 'yplus', 'velocity', 'viscosity', 'zone']

    area: area = area
    """
    area child of reference_values.
    """
    depth: depth = depth
    """
    depth child of reference_values.
    """
    density: density = density
    """
    density child of reference_values.
    """
    enthalpy: enthalpy = enthalpy
    """
    enthalpy child of reference_values.
    """
    length: length = length
    """
    length child of reference_values.
    """
    pressure: pressure = pressure
    """
    pressure child of reference_values.
    """
    temperature: temperature = temperature
    """
    temperature child of reference_values.
    """
    yplus: yplus = yplus
    """
    yplus child of reference_values.
    """
    velocity: velocity = velocity
    """
    velocity child of reference_values.
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of reference_values.
    """
    zone: zone = zone
    """
    zone child of reference_values.
    """
    command_names = \
        ['compute', 'list_val']

    compute: compute = compute
    """
    compute command of reference_values.
    """
    list_val: list_val = list_val
    """
    list_val command of reference_values.
    """
