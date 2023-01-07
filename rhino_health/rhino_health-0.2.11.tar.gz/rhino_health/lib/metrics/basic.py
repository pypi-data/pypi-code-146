from rhino_health.lib.metrics.base_metric import BaseMetric
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class Count(BaseMetric):
    """
    Returns the count of entries for a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def metric_name(self):
        return "count"


class Mean(BaseMetric):
    """
    Returns the mean value of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def metric_name(self):
        return "mean"


class StandardDeviation(BaseMetric):
    """
    Returns the standard deviation of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def metric_name(self):
        return "std"


class Sum(BaseMetric):
    """
    Returns the sum of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def metric_name(self):
        return "sum"
