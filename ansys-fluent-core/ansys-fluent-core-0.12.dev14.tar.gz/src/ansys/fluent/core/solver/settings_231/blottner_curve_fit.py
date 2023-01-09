#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .a import a
from .b import b
from .c import c
class blottner_curve_fit(Group):
    """
    'blottner_curve_fit' child.
    """

    fluent_name = "blottner-curve-fit"

    child_names = \
        ['a', 'b', 'c']

    a: a = a
    """
    a child of blottner_curve_fit.
    """
    b: b = b
    """
    b child of blottner_curve_fit.
    """
    c: c = c
    """
    c child of blottner_curve_fit.
    """
