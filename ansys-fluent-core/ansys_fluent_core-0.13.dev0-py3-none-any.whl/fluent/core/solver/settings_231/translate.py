#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .offset import offset
class translate(Command):
    """
    Translate the mesh.
    
    Parameters
    ----------
        offset : typing.Tuple[real, real, real]
            'offset' child.
    
    """

    fluent_name = "translate"

    argument_names = \
        ['offset']

    offset: offset = offset
    """
    offset argument of translate.
    """
