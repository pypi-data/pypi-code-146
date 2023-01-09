#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .face_pressure_options import face_pressure_options
class face_pressure_controls(Group):
    """
    Enter the face pressure expert controls menu.
    """

    fluent_name = "face-pressure-controls"

    child_names = \
        ['face_pressure_options']

    face_pressure_options: face_pressure_options = face_pressure_options
    """
    face_pressure_options child of face_pressure_controls.
    """
