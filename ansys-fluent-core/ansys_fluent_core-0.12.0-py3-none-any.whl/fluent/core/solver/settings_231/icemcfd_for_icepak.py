#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
class icemcfd_for_icepak(Command):
    """
    Write a binary ICEMCFD domain file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "icemcfd-for-icepak"

    argument_names = \
        ['name']

    name: name = name
    """
    name argument of icemcfd_for_icepak.
    """
