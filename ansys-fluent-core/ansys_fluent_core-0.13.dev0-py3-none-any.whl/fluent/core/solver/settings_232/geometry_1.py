#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .geometry_child import geometry_child

class geometry(NamedObject[geometry_child], _CreatableNamedObjectMixin[geometry_child]):
    """
    Main menu to define a disk-section:
    
     - delete : delete a disk-section% - edit   : edit a disk-section
     - new    : create a new disk-section
     - rename : rename a vbm disk-section.
    
    """

    fluent_name = "geometry"

    child_object_type: geometry_child = geometry_child
    """
    child_object_type of geometry.
    """
