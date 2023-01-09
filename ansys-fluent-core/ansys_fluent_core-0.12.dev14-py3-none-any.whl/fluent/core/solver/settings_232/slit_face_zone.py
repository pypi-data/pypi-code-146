#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .zone_id import zone_id
class slit_face_zone(Command):
    """
    Slit a two-sided wall into two connected wall zones.
    
    Parameters
    ----------
        zone_id : int
            'zone_id' child.
    
    """

    fluent_name = "slit-face-zone"

    argument_names = \
        ['zone_id']

    zone_id: zone_id = zone_id
    """
    zone_id argument of slit_face_zone.
    """
