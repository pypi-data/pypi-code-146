#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .thin_film import thin_film
from .liquid_vof_factor import liquid_vof_factor
class boiling_parameters(Group):
    """
    Multiphase boiling parameters menu.
    """

    fluent_name = "boiling-parameters"

    child_names = \
        ['thin_film', 'liquid_vof_factor']

    thin_film: thin_film = thin_film
    """
    thin_film child of boiling_parameters.
    """
    liquid_vof_factor: liquid_vof_factor = liquid_vof_factor
    """
    liquid_vof_factor child of boiling_parameters.
    """
