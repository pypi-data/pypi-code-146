from typing import Optional, List, Dict, Any


def _convert_to_bulk_editor_filters(filters: List[Dict[str, Any]]):
    filters = [{"filter_type": "or", "condition_value": filter} for filter in filters]
    filters[-1]["group"] = "end"
    return filters


def aggregation_chart(
    groupby: List[Dict[str, Any]],
    metric: List[Dict[str, Any]],
    chart_type: str = "column",
    title: Optional[str] = None,
    page_size: int = 20,
    show_frequencies: bool = False,
    sentiment_field: str = "",
    y_axis_sort_field: str = "",
    sort_direction: str = "desc",
    filters: Optional[List[Dict[str, Any]]] = None,
    convert_filters: bool = True,
):
    """
    Example for groupby
    [
        {
            "agg": "max",
            "field": "score",
            "color": "",
            "name": "max thumbsUpCount",
            "lowerIsBetter": false
        }
    ]
    Example for metric
    [
        {
            "agg": "category",
            "field": "content"
        }
    ]
    """
    assert sort_direction in {"desc", "asc"}

    for query in groupby:
        query["aggType"] = "groupby"

    for query in metric:
        query["aggType"] = "metric"

    if filters is None:
        filters = []

    if filters and convert_filters:
        filters = _convert_to_bulk_editor_filters(filters)

    return [
        {
            "type": "appBlock",
            "content": [
                {
                    "type": "datasetAggregation",
                    "attrs": {
                        "uid": "",
                        "title": title,
                        "chartType": chart_type,
                        "filters": filters,
                        "xAxis": {
                            "fields": groupby,
                            "numResults": page_size,
                            "resortAlphanumerically": False,
                        },
                        "yAxis": {
                            "fields": metric,
                            "showFrequency": show_frequencies,
                            "sortBy": y_axis_sort_field,
                            "sortDirection": sort_direction,
                        },
                        "timeseries": {
                            "field": "insert_date_",
                            "interval": "monthly",
                        },
                        "sentiment": {
                            "field": sentiment_field,
                            "mode": "overview",
                            "interval": "monthly",
                        },
                        "wordCloud": {"mode": "cloud"},
                    },
                }
            ],
        },
    ]
