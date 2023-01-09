#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .repair_1 import repair
class repair_wall_distance(Command):
    """
    Correct wall distance at very high aspect ratio hexahedral/polyhedral cells.
    
    Parameters
    ----------
        repair : bool
            'repair' child.
    
    """

    fluent_name = "repair-wall-distance"

    argument_names = \
        ['repair']

    repair: repair = repair
    """
    repair argument of repair_wall_distance.
    """
