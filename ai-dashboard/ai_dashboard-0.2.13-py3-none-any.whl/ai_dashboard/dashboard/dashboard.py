import json

from copy import deepcopy
from typing import Optional, Union, Dict, Any, List

from ai_dashboard.json_encoder import json_encoder
from ai_dashboard.api import endpoints
from ai_dashboard.tabs import (
    abstract_tab,
    data_report,
    category_view,
)
from ai_dashboard.tabs.chart_view import chart_view
from ai_dashboard.tabs.document_view import document_view


class Dashboard:
    def __init__(
        self,
        endpoints: endpoints.Endpoints,
        dataset_id: str,
        deployable_id: str,
        project_id: str,
        configuration: Optional[Dict[str, Any]] = None,
        private: bool = False,
        _id: Optional[str] = None,
        api_key: Optional[str] = None,
        insert_date_: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self._endpoints = endpoints
        self._dataset_id = dataset_id
        self._deployable_id = deployable_id
        self._project_id = project_id
        self._config = {} if configuration is None else configuration
        self._private = private
        self._id = _id
        self._api_key = api_key
        self._insert_date_ = insert_date_
        self._updated_at = updated_at
        self._tabs = self._init_tabs()

    def _init_tabs(self):
        tabs = {}
        for deployable_id, config in self.config["tabs"].items():
            if config["type"] == "REPORT":
                tab = data_report.DataReport(
                    endpoints=self._endpoints,
                    dataset_id=self._dataset_id,
                    config=config,
                )
            if config["type"] == "CLUSTER_VIEW":
                tab = category_view.CategoryView(
                    endpoints=self._endpoints,
                    dataset_id=self._dataset_id,
                    config=config,
                )
            if config["type"] == "CHART_VIEW":
                tab = chart_view.ChartView(
                    endpoints=self._endpoints,
                    dataset_id=self._dataset_id,
                    config=config,
                )
            if config["type"] == "SEARCH_VIEW":
                tab = document_view.DocumentView(
                    endpoints=self._endpoints,
                    dataset_id=self._dataset_id,
                    config=config,
                )
            tabs[deployable_id] = tab
        return tabs

    def DataReport(
        self,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        return data_report.DataReport(
            endpoints=self._endpoints,
            dataset_id=self._dataset_id,
            title=title,
            name=name,
            colour=colour,
            config=config,
        )

    def CategoryView(
        self,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        return category_view.CategoryView(
            endpoints=self._endpoints,
            dataset_id=self._dataset_id,
            title=title,
            name=name,
            colour=colour,
            config=config,
        )

    def ChartView(
        self,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        return chart_view.ChartView(
            endpoints=self._endpoints,
            dataset_id=self._dataset_id,
            title=title,
            name=name,
            colour=colour,
            config=config,
        )

    def DocumentView(
        self,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        return document_view.DocumentView(
            endpoints=self._endpoints,
            dataset_id=self._dataset_id,
            title=title,
            name=name,
            colour=colour,
            config=config,
        )

    @property
    def config(self):
        return self._config

    @property
    def tabs(self) -> List[abstract_tab.Tab]:
        return self._tabs

    def __getitem__(self, index: Union[str, int]) -> abstract_tab.Tab:
        if isinstance(index, int):
            deployable_id = self.config["tabOrder"][index]
        elif isinstance(index, str):
            deployable_id = index
        else:
            raise ValueError

        tab = self.config["tabs"][deployable_id]
        return tab

    def __setitem__(self, index: Union[str, int], tab: abstract_tab.Tab):
        assert issubclass(type(tab), abstract_tab.Tab)
        deployable_id = tab.deployable_id
        if isinstance(index, int):
            assert index < len(self.config["tabOrder"]), "index must exist"
            self.config["tabs"][deployable_id] = tab
            self.config["tabOrder"][index] = deployable_id
        elif isinstance(index, str):
            try:
                list_ind = self.config["tabOrder"].index(index)
            except IndexError:
                self.config["tabOrder"].append(deployable_id)
            else:
                self.config["tabOrder"][list_ind] = deployable_id

            self.config["tabs"][deployable_id] = tab.json()
            self.config["filters"][deployable_id] = {
                "timeRangeFilter": {
                    "field": "insert_date_",
                    "from": "",
                    "to": "",
                },
                "facetableFields": [],
                "selectedFacetValues": {},
                "advancedFilters": [],
                "searchFilter": {
                    "minimumRelevance": 0.1,
                    "file": "",
                    "vectorModels": {},
                    "noHighlighting": False,
                    "questionAnswer": False,
                    "query": "",
                    "textFieldsToSearch": [],
                    "type": "text",
                    "vectorFieldsToSearch": [],
                    "largeInlineFilters": False,
                },
            }
            self.config["filterToggles"][deployable_id] = True
        else:
            raise ValueError

    def pull(self):
        response = self._endpoints._get_deployable(self._deployable_id)
        for attr, value in response.items():
            if attr == "configuration":
                setattr(self, f"_config", value)
            else:
                setattr(self, f"_{attr}", value)

    def push(self):
        config = deepcopy(self.config)
        config["tabs"] = {id: value.json() for id, value in self.tabs.items()}
        config = json_encoder(config)
        assert json.dumps(config), "self.config must be json serializeable"
        return self._endpoints._update_deployable(
            deployable_id=self._deployable_id,
            dataset_id=self._dataset_id,
            configuration=config,
        )

    def append(self, tab: abstract_tab.Tab) -> None:
        assert isinstance(tab, abstract_tab.Tab)
        deployable_id = tab.deployable_id
        self.config["tabs"][deployable_id] = tab.json()
        self.config["tabOrder"].append(deployable_id)
        self.config["filters"][deployable_id] = {
            "timeRangeFilter": {
                "field": "insert_date_",
                "from": "",
                "to": "",
            },
            "facetableFields": [],
            "selectedFacetValues": {},
            "advancedFilters": [],
            "searchFilter": {
                "minimumRelevance": 0.1,
                "file": "",
                "vectorModels": {},
                "noHighlighting": False,
                "questionAnswer": False,
                "query": "",
                "textFieldsToSearch": [],
                "type": "text",
                "vectorFieldsToSearch": [],
                "largeInlineFilters": False,
            },
        }
        self.config["filterToggles"][deployable_id] = True
        self._tabs[deployable_id] = tab

    def delete_all(self):
        self.config["tabs"] = {}
        self.config["tabOrder"] = []

    def delete(self):
        self._endpoints._delete_deployable(self._deployable_id)

    def set_private(self, private: bool):
        if private:
            self._endpoints._share_dashboard(self._deployable_id)
        else:
            self._endpoints._unshare_dashboard(self._deployable_id)
