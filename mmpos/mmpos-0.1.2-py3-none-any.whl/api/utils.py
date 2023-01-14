MMPOS_API_URL = "https://api.mmpos.eu"
MAX_THREAD_COUNT = 15

import json
import urllib
import os
from requests_cache import CachedSession


def call_api(path, params={"limit": 100}, data={}, method="GET"):
    session = CachedSession(
        cache_name="mmpos_cache",
        backend="filesystem",
        serializer="json",
        expire_after=360,  # 5 minutes
        allowable_methods=["GET"],
        use_cache_dir=True,
    )
    headers = {
        "X-API-Key": os.environ["MMPOS_API_TOKEN"],
        "Content-Type": "application/json",
    }
    url = urllib.parse.urljoin(MMPOS_API_URL, f"api/v1/{path}")
    try:
        if method == "GET":
            response = session.get(
                url, params=params, headers=headers, data=json.dumps(data)
            )
        elif method == "POST":
            response = session.post(
                url, params=params, headers=headers, data=json.dumps(data)
            )
        else:
            # method not supported
            raise Exception(f"method {method} is not supported")

        data = response.json()

    except json.decoder.JSONDecodeError:
        if response.ok:
            data = response.content

    return data


def flatten(x):
    return [i for row in x for i in row]


def current_thread_count(items):
    active_threads = 0
    for item in items:
        if item.is_alive():
            active_threads = active_threads + 1

    return active_threads
