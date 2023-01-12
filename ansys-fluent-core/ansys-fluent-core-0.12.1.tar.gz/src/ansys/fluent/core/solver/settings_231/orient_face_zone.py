#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .face_zone_id import face_zone_id
class orient_face_zone(Command):
    """
    Orient the face zone.
    
    Parameters
    ----------
        face_zone_id : int
            'face_zone_id' child.
    
    """

    fluent_name = "orient-face-zone"

    argument_names = \
        ['face_zone_id']

    face_zone_id: face_zone_id = face_zone_id
    """
    face_zone_id argument of orient_face_zone.
    """
