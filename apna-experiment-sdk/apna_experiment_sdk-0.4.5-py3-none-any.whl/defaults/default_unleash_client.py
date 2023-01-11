from ..base import Configuration
import logging
import os
import json

UNLEASH = 'unleash'


# utils:
def _get_headers(headers_json: str) -> dict:
    # TODO: Deprecate this
    # Fetching headers:
    headers: dict = json.loads(headers_json)
    # Validation:
    if "Authorization" not in headers.keys():
        raise AttributeError(
            f"Enviornment variable 'AEXP_UNLEASH_HEADERS' should be a JSON string containing 'Authorization' header in it.")
    return headers


class DefaultUnleashConf(Configuration):
    """This is the default configuration for the unleash client.
    NOTE: To make changes in the default info over-ride this class.

    This requires the following parameters:
        'AEXP_UNLEASH_URL' (required*): host url of unleash.
        'AEXP_UNLEASH_APP_NAME' (required*): app_name for unleash and mixpanel to identify.
        'AEXP_UNLEASH_AUTH_HEADER' (required*): headers for unleash.
        'AEXP_UNLEASH_REFRESH_INTERVAL' (required*): refresh interval for unleash.
        'AEXP_UNLEASH_LOG_LEVEL' (optional): log level for unleash. Defaults to "info".
        'AEXP_UNLEASH_METRICS_INTERVAL' (required*): The average time where unleash will be sending the metrics to the unleash client.
        'AEXP_UNLEASH_CACHE_DIR' (required*): Default cache dir of unleash.

    More configurable options can be found at:
        https://github.com/Unleash/unleash-client-python#arguments
    """
    conf = dict(
        url=os.getenv("AEXP_UNLEASH_URL"),
        app_name=os.getenv("AEXP_UNLEASH_APP_NAME"),
        custom_headers={'Authorization': os.getenv(
            'AEXP_UNLEASH_AUTH_HEADER')},
        refresh_interval=int(os.getenv("AEXP_UNLEASH_REFRESH_INTERVAL", 900)),
        metrics_interval=int(os.getenv("AEXP_UNLEASH_METRICS_INTERVAL", 900)),
        verbose_log_level=logging.INFO if os.getenv(
            "AEXP_UNLEASH_LOG_LEVEL", "info") == "info" else logging.DEBUG,
        cache_directory=os.getenv("AEXP_UNLEASH_CACHE_DIR"),
        disable_registration=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().validate_conf(caller=type(self).__name__)
