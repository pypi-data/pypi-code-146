#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .copy_design_points import copy_design_points
class duplicate(Command):
    """
    Duplicate Parametric Study.
    
    Parameters
    ----------
        copy_design_points : bool
            'copy_design_points' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['copy_design_points']

    copy_design_points: copy_design_points = copy_design_points
    """
    copy_design_points argument of duplicate.
    """
