#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .axis_origin import axis_origin
from .axis_direction import axis_direction
from .radial_diffusivity import radial_diffusivity
from .tangential_diffusivity import tangential_diffusivity
from .axial_diffusivity import axial_diffusivity
class cyl_orthotropic(Group):
    """
    'cyl_orthotropic' child.
    """

    fluent_name = "cyl-orthotropic"

    child_names = \
        ['axis_origin', 'axis_direction', 'radial_diffusivity',
         'tangential_diffusivity', 'axial_diffusivity']

    axis_origin: axis_origin = axis_origin
    """
    axis_origin child of cyl_orthotropic.
    """
    axis_direction: axis_direction = axis_direction
    """
    axis_direction child of cyl_orthotropic.
    """
    radial_diffusivity: radial_diffusivity = radial_diffusivity
    """
    radial_diffusivity child of cyl_orthotropic.
    """
    tangential_diffusivity: tangential_diffusivity = tangential_diffusivity
    """
    tangential_diffusivity child of cyl_orthotropic.
    """
    axial_diffusivity: axial_diffusivity = axial_diffusivity
    """
    axial_diffusivity child of cyl_orthotropic.
    """
