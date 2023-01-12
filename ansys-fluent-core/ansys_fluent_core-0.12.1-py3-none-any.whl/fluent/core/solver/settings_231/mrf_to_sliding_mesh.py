#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .zone_id import zone_id
class mrf_to_sliding_mesh(Command):
    """
    Change motion specification from MRF to moving mesh.
    
    Parameters
    ----------
        zone_id : int
            'zone_id' child.
    
    """

    fluent_name = "mrf-to-sliding-mesh"

    argument_names = \
        ['zone_id']

    zone_id: zone_id = zone_id
    """
    zone_id argument of mrf_to_sliding_mesh.
    """
