#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .design_point import design_point
class duplicate(Command):
    """
    Duplicate Design Point.
    
    Parameters
    ----------
        design_point : str
            'design_point' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['design_point']

    design_point: design_point = design_point
    """
    design_point argument of duplicate.
    """
