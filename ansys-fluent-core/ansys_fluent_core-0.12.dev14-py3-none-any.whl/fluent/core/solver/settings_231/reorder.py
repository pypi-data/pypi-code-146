#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .band_width import band_width
from .reorder_domain import reorder_domain
from .reorder_zones import reorder_zones
class reorder(Group):
    """
    Enter the reorder domain menu.
    """

    fluent_name = "reorder"

    command_names = \
        ['band_width', 'reorder_domain', 'reorder_zones']

    band_width: band_width = band_width
    """
    band_width command of reorder.
    """
    reorder_domain: reorder_domain = reorder_domain
    """
    reorder_domain command of reorder.
    """
    reorder_zones: reorder_zones = reorder_zones
    """
    reorder_zones command of reorder.
    """
