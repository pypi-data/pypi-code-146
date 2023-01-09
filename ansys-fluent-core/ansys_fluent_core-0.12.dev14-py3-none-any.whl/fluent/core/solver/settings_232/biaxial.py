#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .planar_conductivity import planar_conductivity
from .transverse_conductivity import transverse_conductivity
class biaxial(Group):
    """
    'biaxial' child.
    """

    fluent_name = "biaxial"

    child_names = \
        ['planar_conductivity', 'transverse_conductivity']

    planar_conductivity: planar_conductivity = planar_conductivity
    """
    planar_conductivity child of biaxial.
    """
    transverse_conductivity: transverse_conductivity = transverse_conductivity
    """
    transverse_conductivity child of biaxial.
    """
