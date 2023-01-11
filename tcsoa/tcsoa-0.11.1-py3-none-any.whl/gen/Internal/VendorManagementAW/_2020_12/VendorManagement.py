from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from tcsoa.gen.Internal.VendorManagementAW._2019_12.VendorManagement import ViewModelObject
from dataclasses import dataclass


@dataclass
class FilterCriteriaInput(TcBaseObj):
    """
    A structure representing the input filter criteria for columns.
    
    :var columnName: Internal name of the property on which column filter is applied.
    :var operation: The type of column filter operation applied. The supported operations are: "CONTAINS", "EQUAL",
    "GREATER THAN", "LESS THAN" and "BETWEEN".
    :var values: A list of values to filter. These are not a fixed set of values like operation.
    The "BETWEEN" operation is used only for Date type. It requires two values and the result will be the rows between
    the range given including min and max value. For example if min date is 2020-03-01T00:00:00+0530 and max date is
    2020-03-05T00:00:00+0530, then the result will be shown from date 2020-03-01T00:00:00+0530 to
    2020-03-05T00:00:00+0530.
    """
    columnName: str = ''
    operation: str = ''
    values: List[str] = ()


@dataclass
class OrderedViewModelInput(TcBaseObj):
    """
    The OrderedViewModelInput structure holds the information about the ViewModelObject structures and the information
    about filter criteria and sort criteria.
    
    :var viewModelRows: A list of view model rows for each &bull; displayed node in a table.
    :var columnFilters: A list of filters to be applied on the columns. The must be internal name of the properties on
    which filtering to be applied along with values of the filter must be sent as input.
    :var sortCriteria: A list of columns and the sort direction. The must be internal name of the property on which
    sorting to be applied along with sort direction.
    """
    viewModelRows: List[ViewModelObject] = ()
    columnFilters: List[FilterCriteriaInput] = ()
    sortCriteria: List[SortCriteria] = ()


@dataclass
class SortCriteria(TcBaseObj):
    """
    Stores column internal name and the direction in which column should be sorted.
    
    :var fieldName: The name of the property on which to perform the sorting.
    :var sortingOrder: The order of sorting of the column. Valid sorting orders are integer values between 1 and
    maximum number of displayed columns. If supplied value is not in this range, then column would not participate in
    sorting.
    :var isAscending: If true, columns will be sorted in ascending direction else it will be sorted in descending
    direction.
    """
    fieldName: str = ''
    sortingOrder: int = 0
    isAscending: bool = False
