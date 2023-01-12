#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
class fast_velocity(Command):
    """
    Write a FAST/Plot3D unstructured vector function file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "fast-velocity"

    argument_names = \
        ['name']

    name: name = name
    """
    name argument of fast_velocity.
    """
