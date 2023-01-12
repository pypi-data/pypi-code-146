from typing import Optional, Dict, Any, List

from ai_dashboard.api import endpoints
from ai_dashboard.tabs import abstract_tab


class CategoryView(abstract_tab.Tab):
    ID = "CLUSTER_VIEW"

    BLANK: Dict[str, Any] = {
        "activeFilterGroup": "",
        "color": None,
        "configuration": {},
        "name": "",
        "type": ID,
    }

    def __init__(
        self,
        endpoints: endpoints.Endpoints,
        dataset_id: str,
        title: Optional[str] = None,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        self._endpoints = endpoints

        if config is not None:
            self._config = config
        else:
            self.reset()

        self.dataset_id = dataset_id
        self.config["colour"] = colour
        self.config["configuration"]["title"] = self.ID if title is None else title
        self.config["name"] = name

    @classmethod
    def from_fields(
        cls,
        cluster_field: str,
        primary_field: str = None,
        secondary_field: str = None,
        other_metadata: List[str] = None,
        subcluster_field: str = "",
        layout_template: str = "custom",
        title: Optional[str] = None,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        sort_by_metric: str = "frequency",
        overview_chart_type: str = "grid",
        sentiment_field: str = "",
        timeseries_interval: str = "monthly",
        timeseries_field: str = "insert_date_",
        metrics: list = None,
        sort_by_direction: str = "desc",
        results_mode: str = "summary",
    ):
        category_view = cls(name=name, title=title, colour=colour)
        fields = []
        if primary_field is not None:
            fields.append(
                {
                    "id": "primary",
                    "value": primary_field,
                },
            )
        if secondary_field is not None:
            fields.append(
                {
                    "id": "secondary",
                    "value": secondary_field,
                }
            )
        if other_metadata is not None:
            fields.append(
                {
                    "id": "multiple-fields",
                    "value": other_metadata,
                }
            )
        category_view.config = {
            "activeFilterGroup": "",
            "color": colour,
            "configuration": {
                "previewDocumentCardConfiguration": {
                    "layoutTemplateConfiguration": {"fields": fields},
                    "layoutTemplate": layout_template,
                    "fields": fields,
                },
                "subclusterField": subcluster_field,
                "categoryMetrics": {
                    "sortByMetric": sort_by_metric,
                    "overviewChartType": overview_chart_type,
                    "sentimentField": sentiment_field,
                    "timeseriesInterval": timeseries_interval,
                    "timeseriesField": timeseries_field,
                    "metrics": [] if metrics is not None else metrics,
                    "sortByDirection": sort_by_direction,
                    "resultsMode": results_mode,
                },
                "clusterField": cluster_field,
            },
            "name": name,
            "type": cls.ID,
        }
        return category_view

    def set_view(
        self,
        cluster_field: str,
        primary_field: str = None,
        secondary_field: str = None,
        other_metadata: List[str] = None,
        subcluster_field: str = "",
        layout_template: str = "custom",
        sort_by_metric: str = "frequency",
        overview_chart_type: str = "grid",
        sentiment_field: str = "",
        timeseries_interval: str = "monthly",
        timeseries_field: str = "insert_date_",
        metrics: list = None,
        sort_by_direction: str = "desc",
        results_mode: str = "summary",
    ):
        self.config["configuration"] = {
            "previewDocumentCardConfiguration": {
                "layoutTemplateConfiguration": {"fields": []},
                "layoutTemplate": layout_template,
            },
            "subclusterField": subcluster_field,
            "clusterField": cluster_field,
        }
        if primary_field is not None:
            self.config["configuration"]["previewDocumentCardConfiguration"][
                "layoutTemplateConfiguration"
            ]["fields"].append(
                {
                    "id": "primary",
                    "value": primary_field,
                }
            )
        if secondary_field is not None:
            self.config["configuration"]["previewDocumentCardConfiguration"][
                "layoutTemplateConfiguration"
            ]["fields"].append(
                {
                    "id": "secondary",
                    "value": secondary_field,
                }
            )
        if other_metadata is not None:
            self.config["configuration"]["previewDocumentCardConfiguration"][
                "layoutTemplateConfiguration"
            ]["fields"].append(
                {
                    "id": "multiple-fields",
                    "value": other_metadata,
                }
            )
        self.config["configuration"]["categoryMetrics"] = {
            "sortByMetric": sort_by_metric,
            "overviewChartType": overview_chart_type,
            "sentimentField": sentiment_field,
            "timeseriesInterval": timeseries_interval,
            "timeseriesField": timeseries_field,
            "metrics": [] if metrics is not None else metrics,
            "sortByDirection": sort_by_direction,
            "resultsMode": results_mode,
        }
