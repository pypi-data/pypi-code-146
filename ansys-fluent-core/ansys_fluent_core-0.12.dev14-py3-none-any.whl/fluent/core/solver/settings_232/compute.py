#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .from_zone_type import from_zone_type
from .from_zone_name import from_zone_name
from .phase_25 import phase
class compute(Command):
    """
    'compute' command.
    
    Parameters
    ----------
        from_zone_type : str
            'from_zone_type' child.
        from_zone_name : str
            'from_zone_name' child.
        phase : str
            'phase' child.
    
    """

    fluent_name = "compute"

    argument_names = \
        ['from_zone_type', 'from_zone_name', 'phase']

    from_zone_type: from_zone_type = from_zone_type
    """
    from_zone_type argument of compute.
    """
    from_zone_name: from_zone_name = from_zone_name
    """
    from_zone_name argument of compute.
    """
    phase: phase = phase
    """
    phase argument of compute.
    """
