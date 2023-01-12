#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_8 import option
from .max_vf_allowed_for_blocking import max_vf_allowed_for_blocking
from .enable_drag_scaling import enable_drag_scaling
from .enable_source_term_scaling import enable_source_term_scaling
class volume_displacement(Group):
    """
    In many Lagrangian-Eulerian simulations, the volume fraction of the local particle phase may not be small,
    and the blocking effect of the particulate phase on the carrier phase may need to be taken into account.
    To enable the volume displacement effect of particles, select "option = #t".
    """

    fluent_name = "volume-displacement"

    child_names = \
        ['option', 'max_vf_allowed_for_blocking', 'enable_drag_scaling',
         'enable_source_term_scaling']

    option: option = option
    """
    option child of volume_displacement.
    """
    max_vf_allowed_for_blocking: max_vf_allowed_for_blocking = max_vf_allowed_for_blocking
    """
    max_vf_allowed_for_blocking child of volume_displacement.
    """
    enable_drag_scaling: enable_drag_scaling = enable_drag_scaling
    """
    enable_drag_scaling child of volume_displacement.
    """
    enable_source_term_scaling: enable_source_term_scaling = enable_source_term_scaling
    """
    enable_source_term_scaling child of volume_displacement.
    """
