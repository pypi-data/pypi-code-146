from typing import Optional, List, Dict, Any


def metric(
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

    return [
        {
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
    ]
