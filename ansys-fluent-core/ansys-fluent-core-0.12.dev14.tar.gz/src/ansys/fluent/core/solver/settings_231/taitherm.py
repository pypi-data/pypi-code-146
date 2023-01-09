#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
from .surface_name_list import surface_name_list
from .wall_function import wall_function
from .htc_on_walls import htc_on_walls
class taitherm(Command):
    """
    Write a TAITherm file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surface_name_list : typing.List[str]
            'surface_name_list' child.
        wall_function : bool
            'wall_function' child.
        htc_on_walls : bool
            'htc_on_walls' child.
    
    """

    fluent_name = "taitherm"

    argument_names = \
        ['name', 'surface_name_list', 'wall_function', 'htc_on_walls']

    name: name = name
    """
    name argument of taitherm.
    """
    surface_name_list: surface_name_list = surface_name_list
    """
    surface_name_list argument of taitherm.
    """
    wall_function: wall_function = wall_function
    """
    wall_function argument of taitherm.
    """
    htc_on_walls: htc_on_walls = htc_on_walls
    """
    htc_on_walls argument of taitherm.
    """
