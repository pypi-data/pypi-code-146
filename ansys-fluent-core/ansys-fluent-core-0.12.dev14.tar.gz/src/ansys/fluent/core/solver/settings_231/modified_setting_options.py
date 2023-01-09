#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .modified_setting import modified_setting
from .write_user_setting import write_user_setting
class modified_setting_options(Group):
    """
    'modified_setting_options' child.
    """

    fluent_name = "modified-setting-options"

    command_names = \
        ['modified_setting', 'write_user_setting']

    modified_setting: modified_setting = modified_setting
    """
    modified_setting command of modified_setting_options.
    """
    write_user_setting: write_user_setting = write_user_setting
    """
    write_user_setting command of modified_setting_options.
    """
