import time

from typing import Optional, Dict, Any

from ai_dashboard.api import endpoints, helpers
from ai_dashboard.dashboard import dashboard

from ai_dashboard import constants
from ai_dashboard import errors


class Client:
    def __init__(self, token: str) -> None:

        self._credentials = helpers.process_token(token)
        self._token = token
        self._endpoints = endpoints.Endpoints(credentials=self._credentials)

        try:
            response = self.list_deployables()
        except:
            raise errors.AuthException
        else:
            self._deployables = sorted(
                response["deployables"], key=lambda x: x["insert_date_"]
            )
            print(constants.WELCOME_MESSAGE.format(self._credentials.project))

    @property
    def deployables(self):
        response = self.list_deployables()
        self._deployables = sorted(
            response["deployables"], key=lambda x: x["insert_date_"]
        )
        return self._deployables

    def recent(self) -> dashboard.Dashboard:
        configuration = self.deployables[-1]
        dataset_id = configuration.get("dataset_id")
        deployable_id = configuration.get("deployable_id")
        project_id = configuration.get("project_id")
        return dashboard.Dashboard(
            endpoints=self._endpoints,
            dataset_id=dataset_id,
            deployable_id=deployable_id,
            configuration=configuration["configuration"],
            project_id=project_id,
        )

    def list_deployables(self, page_size: int = 1000):
        return self._endpoints._list_deployables(page_size=page_size)

    def create_deployable(
        self,
        dataset_id: Optional[str] = None,
        deployable_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        if deployable_id is None:
            if name is not None:
                configs = [
                    d
                    for d in self.deployables
                    if d["configuration"].get("deployable_name", "") == name
                    and d.get("dataset_id") == dataset_id
                ]
                try:
                    deployable_id = configs[0]["deployable_id"]
                except:
                    pass
                else:
                    return self._endpoints._get_deployable(
                        deployable_id=deployable_id,
                    )

            if config is None:
                config = {
                    "private": False,
                    "tabs": {},
                    "filters": {},
                    "dataset_name": dataset_id,
                    "type": "explorer",
                    "filterToggles": {},
                    "deployable_name": name,
                    "cacheTimestamp": int(time.time() * 1000),
                    "api_key": "",
                    "project_id": self._credentials.project,
                    "tabOrder": [],
                    "deployable_id": "",
                    "read_key": "",
                }
            return self._endpoints._create_deployable(
                dataset_id=dataset_id,
                config=config,
            )
        else:
            return self._endpoints._get_deployable(
                deployable_id=deployable_id,
            )

    def delete_deployable(self, deployable_id: str) -> None:
        return self._endpoints._delete_deployable(deployable_id=deployable_id)

    def Dashboard(
        self,
        dataset_id: Optional[str] = None,
        delpoyable_id: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> dashboard.Dashboard:
        assert (
            dataset_id is not None or delpoyable_id is not None
        ), "Set either `dataset_id` and `config` or `deployable_id`"
        response = self.create_deployable(
            dataset_id=dataset_id,
            deployable_id=delpoyable_id,
            config=config,
            name=name,
        )
        return dashboard.Dashboard(endpoints=self._endpoints, **response)
