#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .setting_type import setting_type
class modified_setting(Command):
    """
    Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.
    
    Parameters
    ----------
        setting_type : typing.List[str]
            'setting_type' child.
    
    """

    fluent_name = "modified-setting"

    argument_names = \
        ['setting_type']

    setting_type: setting_type = setting_type
    """
    setting_type argument of modified_setting.
    """
