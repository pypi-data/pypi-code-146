from typing import Dict, Any, TypedDict, Optional

from filum_utils.clients.common import BaseClient
from filum_utils.config import config


class ActionError(TypedDict, total=False):
    type: str
    message: str
    data: str
    notification_message: Optional[str]


class ActionClient(BaseClient):
    def __init__(self, action_id: int = None, action: Dict[str, Any] = None):
        super().__init__(
            base_url=config.APPSTORE_BASE_URL,
            username=config.APPSTORE_USERNAME,
            password=config.APPSTORE_PASSWORD
        )

        if action:
            self.action = action

        else:
            self.action = self._request(
                method="GET",
                endpoint=f"/source/actions/{action_id}"
            )

    def get_data(self, key):
        data = self.action.get("data")
        return data and data.get(key)

    def update_data(self, updated_data: Dict[str, Any]):
        self.action = self._request(
            method="PUT",
            endpoint=f"/source/actions/{self.action['id']}/data",
            data=updated_data
        )

    def sync(self, request_data: Dict[str, Any]):
        self._request(
            method="POST",
            endpoint=f"/internal/actions/{self.action['id']}/sync",
            data={"request_data": request_data}
        )
