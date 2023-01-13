import csv
from typing import List

from filum_utils.clients.common import BaseClient
from filum_utils.config import config
from filum_utils.enums import Organization


class FilumClient(BaseClient):
    def __init__(self):
        super().__init__(
            base_url=config.FILUM_BASE_URL,
            username=config.FILUM_USERNAME,
            password=config.FILUM_PASSWORD,
        )

    def get_automated_action(self, automated_action_id: int):
        return self._request(
            method="GET",
            endpoint=f"/internal/automated-actions/{automated_action_id}"
        )

    def get_campaign(self, campaign_id: int):
        return self._request(
            method="GET",
            endpoint=f"/internal/survey-campaigns/{campaign_id}"
        )

    def get_segment(self, segment_id: str, organization: Organization):
        return self._request(
            method="GET",
            endpoint=f"/internal/segments/{segment_id}",
            params={
                "organization_id": organization["id"],
                "organization_slug": organization["slug"]
            }
        )

    def get_user_csv_reader(
        self,
        properties: List[str],
        object_ids: List[str],
        object_type: str,
        organization: Organization,
        required_properties: List[List[str]] = None,
        last_synced_at: str = None,
        limit: int = config.SEGMENT_RECORD_LIMIT,
        offset: int = 0
    ):
        response_content = self._request(
            method="POST",
            endpoint="/internal/users/export",
            data={
                "object_ids": object_ids,
                "object_type": object_type,
                "organization_id": organization["id"],
                "organization_slug": organization["slug"],
                "last_synced_at": last_synced_at,
                "properties": properties,
                "required_properties": required_properties,
                "offset": offset,
                "limit": limit
            }
        )

        decoded_content = response_content.decode("utf-8")
        return csv.DictReader(decoded_content.splitlines(), skipinitialspace=True, delimiter=",")
