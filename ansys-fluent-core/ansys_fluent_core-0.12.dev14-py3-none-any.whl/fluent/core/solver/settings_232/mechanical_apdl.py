#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
from .thread_name_list import thread_name_list
class mechanical_apdl(Command):
    """
    Write an Mechanical APDL file.
    
    Parameters
    ----------
        name : str
            'name' child.
        thread_name_list : typing.List[str]
            'thread_name_list' child.
    
    """

    fluent_name = "mechanical-apdl"

    argument_names = \
        ['name', 'thread_name_list']

    name: name = name
    """
    name argument of mechanical_apdl.
    """
    thread_name_list: thread_name_list = thread_name_list
    """
    thread_name_list argument of mechanical_apdl.
    """
