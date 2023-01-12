#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_type import report_type
from .realcomponent import realcomponent
from .nodal_diameters import nodal_diameters
from .normalization import normalization
from .integrate_over import integrate_over
from .average_over import average_over
from .per_zone import per_zone
from .old_props import old_props
from .thread_names import thread_names
from .thread_ids import thread_ids
class aeromechanics_child(Group):
    """
    'child_object_type' of aeromechanics.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['report_type', 'realcomponent', 'nodal_diameters', 'normalization',
         'integrate_over', 'average_over', 'per_zone', 'old_props',
         'thread_names', 'thread_ids']

    report_type: report_type = report_type
    """
    report_type child of aeromechanics_child.
    """
    realcomponent: realcomponent = realcomponent
    """
    realcomponent child of aeromechanics_child.
    """
    nodal_diameters: nodal_diameters = nodal_diameters
    """
    nodal_diameters child of aeromechanics_child.
    """
    normalization: normalization = normalization
    """
    normalization child of aeromechanics_child.
    """
    integrate_over: integrate_over = integrate_over
    """
    integrate_over child of aeromechanics_child.
    """
    average_over: average_over = average_over
    """
    average_over child of aeromechanics_child.
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of aeromechanics_child.
    """
    old_props: old_props = old_props
    """
    old_props child of aeromechanics_child.
    """
    thread_names: thread_names = thread_names
    """
    thread_names child of aeromechanics_child.
    """
    thread_ids: thread_ids = thread_ids
    """
    thread_ids child of aeromechanics_child.
    """
