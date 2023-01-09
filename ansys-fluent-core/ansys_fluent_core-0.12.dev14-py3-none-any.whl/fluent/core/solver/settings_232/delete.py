#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .surface import surface
class delete(Command):
    """
    Delete surface mesh.
    
    Parameters
    ----------
        surface : str
            'surface' child.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['surface']

    surface: surface = surface
    """
    surface argument of delete.
    """
