#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .face_name import face_name
class list_face(Command):
    """
    'list_face' command.
    
    Parameters
    ----------
        face_name : str
            'face_name' child.
    
    """

    fluent_name = "list-face"

    argument_names = \
        ['face_name']

    face_name: face_name = face_name
    """
    face_name argument of list_face.
    """
