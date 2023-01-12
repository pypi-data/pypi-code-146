#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .turbulence_options import turbulence_options
from .enable_8 import enable
class warped_face_gradient_correction(Group):
    """
    Enter warped-face-gradient-correction menu.
    """

    fluent_name = "warped-face-gradient-correction"

    child_names = \
        ['turbulence_options']

    turbulence_options: turbulence_options = turbulence_options
    """
    turbulence_options child of warped_face_gradient_correction.
    """
    command_names = \
        ['enable']

    enable: enable = enable
    """
    enable command of warped_face_gradient_correction.
    """
