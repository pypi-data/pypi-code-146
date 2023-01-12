from typing import Optional, List, Dict, Any
from ai_dashboard.tabs.data_report.blocks.base import BaseBlock


def _convert_to_bulk_editor_filters(filters: List[Dict[str, Any]]):
    filters = [{"filter_type": "or", "condition_value": filter} for filter in filters]
    filters[-1]["group"] = "end"
    return filters


class ConnectedChart(BaseBlock):
    def __init__(
        self,
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

        self.block = {
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
        }


class ConnectedMetric(BaseBlock):
    def __init__(
        self,
        query: List[Dict[str, Any]],
        title: Optional[str] = None,
        show_frequencies: bool = False,
        sort_direction: str = "Descending",
    ):
        """
        Example for aggregates
        [
            {
                "agg": "category",
                "field": "_cluster_.desc_all-mpnet-base-v2_vector_.kmeans-8",
                "name": "category _cluster_.desc_all-mpnet-base-v2_vector_.kmeans-8",
                "aggType": "groupby",
            },
            {
                "agg": "avg",
                "field": "_sentiment_.desc.cardiffnlp-twitter-roberta-base-sentiment.overall_sentiment_score",
                "name": "avg desc (Sentiment Score)",
                "aggType": "metric",
            },
        ]
        """
        assert sort_direction in {"Descending", "Ascending"}

        for q in query:
            q["aggType"] = "metric"

        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "metricAggregation",
                    "attrs": {
                        "displayType": "column",
                        "sortDirection": sort_direction,
                        "showFrequencies": show_frequencies,
                        "datasetId": "cat_and_dogs",
                        "aggregates": query,
                        "sortBy": "",
                        "title": "" if title is None else title,
                    },
                }
            ],
        }
