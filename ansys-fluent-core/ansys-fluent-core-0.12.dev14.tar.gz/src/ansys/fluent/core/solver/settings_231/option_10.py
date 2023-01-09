#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .min_max import min_max
from .in_range import in_range
from .except_in_range import except_in_range
from .top_value_cells import top_value_cells
from .low_value_cells import low_value_cells
from .less_than import less_than
from .more_than import more_than
from .between_std_dev import between_std_dev
from .outside_std_dev import outside_std_dev
from .less_than_std_dev import less_than_std_dev
from .more_than_std_dev import more_than_std_dev
class option(Group):
    """
    'option' child.
    """

    fluent_name = "option"

    child_names = \
        ['option', 'min_max', 'in_range', 'except_in_range',
         'top_value_cells', 'low_value_cells', 'less_than', 'more_than',
         'between_std_dev', 'outside_std_dev', 'less_than_std_dev',
         'more_than_std_dev']

    option: option = option
    """
    option child of option.
    """
    min_max: min_max = min_max
    """
    min_max child of option.
    """
    in_range: in_range = in_range
    """
    in_range child of option.
    """
    except_in_range: except_in_range = except_in_range
    """
    except_in_range child of option.
    """
    top_value_cells: top_value_cells = top_value_cells
    """
    top_value_cells child of option.
    """
    low_value_cells: low_value_cells = low_value_cells
    """
    low_value_cells child of option.
    """
    less_than: less_than = less_than
    """
    less_than child of option.
    """
    more_than: more_than = more_than
    """
    more_than child of option.
    """
    between_std_dev: between_std_dev = between_std_dev
    """
    between_std_dev child of option.
    """
    outside_std_dev: outside_std_dev = outside_std_dev
    """
    outside_std_dev child of option.
    """
    less_than_std_dev: less_than_std_dev = less_than_std_dev
    """
    less_than_std_dev child of option.
    """
    more_than_std_dev: more_than_std_dev = more_than_std_dev
    """
    more_than_std_dev child of option.
    """
