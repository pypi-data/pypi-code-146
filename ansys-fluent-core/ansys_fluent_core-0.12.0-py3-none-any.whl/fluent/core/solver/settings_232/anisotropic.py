#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .matrix_component import matrix_component
from .diffusivity import diffusivity
class anisotropic(Group):
    """
    'anisotropic' child.
    """

    fluent_name = "anisotropic"

    child_names = \
        ['matrix_component', 'diffusivity']

    matrix_component: matrix_component = matrix_component
    """
    matrix_component child of anisotropic.
    """
    diffusivity: diffusivity = diffusivity
    """
    diffusivity child of anisotropic.
    """
