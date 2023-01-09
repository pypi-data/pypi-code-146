#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .moment_child import moment_child

class moment(NamedObject[moment_child], _CreatableNamedObjectMixin[moment_child]):
    """
    'moment' child.
    """

    fluent_name = "moment"

    child_object_type: moment_child = moment_child
    """
    child_object_type of moment.
    """
