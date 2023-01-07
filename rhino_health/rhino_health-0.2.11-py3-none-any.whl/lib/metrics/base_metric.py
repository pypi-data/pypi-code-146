import json
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from rhino_health.lib.metrics.filter_variable import FilterBetweenRange, FilterType


class DataFilter(BaseModel):
    """
    A filter to be applied on the entire Cohort
    """

    filter_column: str
    """The column in the remote cohort df to check against"""
    filter_value: Union[Any, FilterBetweenRange]
    """The value to match against or a FilterBetweenRange if filter_type is FilterType.BETWEEN"""
    filter_type: Optional[FilterType] = FilterType.EQUAL
    """The type of filtering to perform. Defaults to FilterType.EQUAL"""


class GroupingData(BaseModel):
    """
    Configuration for grouping metric results

    See Also
    --------
    pandas.groupby : Implementation used for grouping. `See documentation <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html>`_
    """

    groupings: List[str] = []
    """
    A list of columns to group metric results by
    """
    dropna: Optional[bool] = True
    """
    Should na values be dropped if in a grouping key
    """


class BaseMetric(BaseModel):
    """
    Parameters available for every metric
    """

    data_filters: Optional[List[DataFilter]] = []  # We will filter in the order passed in
    group_by: Optional[GroupingData] = None
    timeout_seconds: Optional[
        float
    ] = 600.0  # Metric calculations that take longer than this time will timeout

    def metric_name(self):
        """
        @autoapi False
        Each metric should define this so the backend cloud knows how to handle things.
        """
        raise NotImplementedError

    def data(self):
        data = {
            "metric": self.metric_name(),
            "arguments": self.json(exclude_none=True, exclude={"timeout_seconds"}),
        }
        if self.timeout_seconds is not None:
            data["timeout_seconds"] = self.timeout_seconds
        return data


MetricResultDataType = Dict[str, Any]
"""
Dict[str, Any]
"""


class MetricResponse(BaseModel):
    """
    Standardized response from querying metrics against a Cohort
    """

    # TODO: objects for specific endpoints
    output: MetricResultDataType  # if group_by is specified in the arguments, is a map of group: output

    def __init__(self, **data):
        status = data.get("status", None)
        if status == "error":
            data["output"] = {"error": data["data"]}
        else:
            if isinstance(data["output"], str):
                data["output"] = json.loads(data["output"])
            if "null" in data["output"].keys() and len(data["output"].keys()) == 1:
                data["output"] = data["output"]["null"]

        super(MetricResponse, self).__init__(**data)
