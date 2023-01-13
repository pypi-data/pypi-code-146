import goog_stats.consts as consts
import requests
import logging

LOGGER = logging.getLogger(__name__)


def record_event(conf, event_subject, event_details):
    url = f"{conf[consts.API_URL]}?v=1"
    query_params = f"&tid={conf[consts.TARGET_ID]}&cid={conf[consts.CLIENT_ID]}&"
    query_params = query_params + f"t={conf[consts.TARGET]}&dp={event_subject}&ul={conf[consts.USER_LANG]}&" \
                                  f"dt={event_details}"

    LOGGER.info("recording analytics event")
    api_url = "{}{}".format(url, query_params)

    payload = {}
    headers = {
        'User-Agent': 'pypip'
    }

    return requests.request("POST", api_url, headers=headers, data=payload)
