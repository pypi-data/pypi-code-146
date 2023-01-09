#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_origin import axis_origin
from .axis_direction import axis_direction
from .radial_conductivity import radial_conductivity
from .tangential_conductivity import tangential_conductivity
from .axial_conductivity import axial_conductivity
class cyl_orthotropic(Group):
    """
    'cyl_orthotropic' child.
    """

    fluent_name = "cyl-orthotropic"

    child_names = \
        ['axis_origin', 'axis_direction', 'radial_conductivity',
         'tangential_conductivity', 'axial_conductivity']

    axis_origin: axis_origin = axis_origin
    """
    axis_origin child of cyl_orthotropic.
    """
    axis_direction: axis_direction = axis_direction
    """
    axis_direction child of cyl_orthotropic.
    """
    radial_conductivity: radial_conductivity = radial_conductivity
    """
    radial_conductivity child of cyl_orthotropic.
    """
    tangential_conductivity: tangential_conductivity = tangential_conductivity
    """
    tangential_conductivity child of cyl_orthotropic.
    """
    axial_conductivity: axial_conductivity = axial_conductivity
    """
    axial_conductivity child of cyl_orthotropic.
    """
