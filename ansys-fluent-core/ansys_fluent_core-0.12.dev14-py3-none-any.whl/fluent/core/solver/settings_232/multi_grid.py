#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .mg_controls import mg_controls
from .amg_controls import amg_controls
from .fas_mg_controls import fas_mg_controls
from .amg_gpgpu_options import amg_gpgpu_options
class multi_grid(Group):
    """
    'multi_grid' child.
    """

    fluent_name = "multi-grid"

    child_names = \
        ['mg_controls', 'amg_controls', 'fas_mg_controls',
         'amg_gpgpu_options']

    mg_controls: mg_controls = mg_controls
    """
    mg_controls child of multi_grid.
    """
    amg_controls: amg_controls = amg_controls
    """
    amg_controls child of multi_grid.
    """
    fas_mg_controls: fas_mg_controls = fas_mg_controls
    """
    fas_mg_controls child of multi_grid.
    """
    amg_gpgpu_options: amg_gpgpu_options = amg_gpgpu_options
    """
    amg_gpgpu_options child of multi_grid.
    """
