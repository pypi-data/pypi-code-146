#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .zone_name import zone_name
from .overwrite import overwrite
class copy_mrf_to_mesh_motion(Command):
    """
    Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.
    
    Parameters
    ----------
        zone_name : str
            'zone_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "copy-mrf-to-mesh-motion"

    argument_names = \
        ['zone_name', 'overwrite']

    zone_name: zone_name = zone_name
    """
    zone_name argument of copy_mrf_to_mesh_motion.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of copy_mrf_to_mesh_motion.
    """
