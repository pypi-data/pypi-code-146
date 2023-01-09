#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .rgb_vector import rgb_vector
class set_ambient_color(Command):
    """
    'set_ambient_color' command.
    
    Parameters
    ----------
        rgb_vector : typing.Tuple[real, real, real]
            'rgb_vector' child.
    
    """

    fluent_name = "set-ambient-color"

    argument_names = \
        ['rgb_vector']

    rgb_vector: rgb_vector = rgb_vector
    """
    rgb_vector argument of set_ambient_color.
    """
