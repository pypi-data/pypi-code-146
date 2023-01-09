#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .reconstruct_geometry import reconstruct_geometry
class geometry(Group):
    """
    Enter the adaption geometry menu.
    """

    fluent_name = "geometry"

    child_names = \
        ['reconstruct_geometry']

    reconstruct_geometry: reconstruct_geometry = reconstruct_geometry
    """
    reconstruct_geometry child of geometry.
    """
