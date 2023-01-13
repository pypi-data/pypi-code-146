from typing import Dict, Any

from filum_utils.clients.common import BaseClient
from filum_utils.config import config
from filum_utils.enums import Organization


class SubscriptionClient(BaseClient):
    def __init__(self, subscription_id: int):
        super().__init__(
            base_url=config.SUBSCRIPTION_BASE_URL,
            username=config.SUBSCRIPTION_USERNAME,
            password=config.SUBSCRIPTION_PASSWORD
        )

        self.subscription = self._request(
            method="GET",
            endpoint=f"/internal/subscriptions/{subscription_id}"
        )

    def get_action_id(self):
        if self.subscription["subscriber_type"] != "action":
            return None

        return self.subscription["subscriber_id"]

    def get_data(self):
        return self.subscription["data"]

    def get_object_id(self):
        return self.subscription["object_id"]

    def get_object_type(self):
        return self.subscription["object_type"]

    def get_organization(self) -> Organization:
        return {
            "id": self.subscription["organization_id"],
            "slug": self.subscription["organization_slug"]
        }

    def update_data(self, updated_data: Dict[str, Any]):
        self._request(
            method="PUT",
            endpoint=f"internal/subscriptions/{self.subscription['id']}/data",
            data=updated_data
        )
