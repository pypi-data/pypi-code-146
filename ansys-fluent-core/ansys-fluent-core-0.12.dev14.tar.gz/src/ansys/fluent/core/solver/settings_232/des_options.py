#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .all_len_modified import all_len_modified
from .des_limiter_option import des_limiter_option
class des_options(Group):
    """
    'des_options' child.
    """

    fluent_name = "des-options"

    child_names = \
        ['all_len_modified', 'des_limiter_option']

    all_len_modified: all_len_modified = all_len_modified
    """
    all_len_modified child of des_options.
    """
    des_limiter_option: des_limiter_option = des_limiter_option
    """
    des_limiter_option child of des_options.
    """
