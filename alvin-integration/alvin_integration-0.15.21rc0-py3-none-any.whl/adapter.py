import logging
import os

import requests

from alvin_integration.helper import AlvinLoggerAdapter, log_verbose


class AlvinLineageBackendAdapter:
    def __init__(self, alvin_base_url=None, alvin_api_key=None):
        self.alvin_base_url = os.environ.get("ALVIN_URL", alvin_base_url)

        self.alvin_api_key = os.environ.get("ALVIN_API_KEY", alvin_api_key)

        self.log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

    def send_data(self, payload, resource):
        try:
            requests.post(
                f"{self.alvin_base_url}/{resource}",
                json=payload,
                headers={"X-API-KEY": self.alvin_api_key},
            )
        except Exception as err:
            log_verbose(f"Error sending message to Alvin backend. Error: {err}.")
