#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
class fast_solution(Command):
    """
    Write a FAST/Plot3D unstructured solution file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "fast-solution"

    argument_names = \
        ['name']

    name: name = name
    """
    name argument of fast_solution.
    """
