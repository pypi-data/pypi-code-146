from typing import Optional, Dict, Any, List

from ai_dashboard.api import endpoints
from ai_dashboard.tabs import abstract_tab


class DocumentView(abstract_tab.Tab):
    ID = "SEARCH_VIEW"

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
    def from_metric(
        cls,
        title: str,
        metric: str,
        layout_mode: Optional[str] = None,
        layout_template: Optional[str] = None,
        ids_to_filter: Optional[List[str]] = None,
        sort_by_direction: Optional[str] = None,
        name: Optional[str] = None,
        colour: Optional[str] = None,
    ):
        document_view = cls(name=name, title=title, colour=colour)
        document_view.config = {
            "activeFilterGroup": "",
            "color": colour,
            "configuration": {
                "title": title,
                "configuration": {
                    "sortByMetric": metric,
                    "documentViewConfiguration": {
                        "layoutMode": "grid" if layout_mode is None else layout_mode,
                        "layoutTemplate": "text-analysis"
                        if layout_template is None
                        else layout_template,
                    },
                    "page": 1,
                    "documentIdsToFilterOut": ids_to_filter
                    if ids_to_filter is not None
                    else [],
                    "sortByDirection": "desc"
                    if sort_by_direction is None
                    else sort_by_direction,
                },
            },
            "name": name,
            "type": cls.ID,
        }
        return document_view

    def set_metric(
        self,
        metric: str,
        layout_mode: Optional[str] = None,
        layout_template: Optional[str] = None,
        ids_to_filter: Optional[List[str]] = None,
        sort_by_direction: Optional[str] = None,
    ):
        self.config["configuration"] = {
            **self.config["configuration"],
            "configuration": {
                "sortByMetric": metric,
                "documentViewConfiguration": {
                    "layoutMode": "grid" if layout_mode is None else layout_mode,
                    "layoutTemplate": "text-analysis"
                    if layout_template is None
                    else layout_template,
                },
                "page": 1,
                "documentIdsToFilterOut": ids_to_filter
                if ids_to_filter is not None
                else [],
                "sortByDirection": "desc"
                if sort_by_direction is None
                else sort_by_direction,
            },
        }
