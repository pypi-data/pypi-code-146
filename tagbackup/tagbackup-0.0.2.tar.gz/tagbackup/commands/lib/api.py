from datetime import datetime
from hashlib import sha256
import requests

from .constants import API_URL, PREFIX, SUFFIX
from .identity import get_machine_id


def generate_hash(timestamp, device_id):
    prehash = "::".join([PREFIX, timestamp, get_machine_id(), device_id, SUFFIX])
    return sha256(prehash.encode("utf-8")).hexdigest()


def get_timestamp():
    return str(round(datetime.utcnow().timestamp()))


def api_post(url, device_id, data, add_headers):
    timestamp = get_timestamp()
    headers = {}
    if add_headers:
        headers = {
            "tagbackup-device": device_id,
            "tagbackup-timestamp": timestamp,
            "tagbackup-hash": generate_hash(timestamp, device_id),
        }

    try:
        r = requests.post(f"{API_URL}{url}", json=data, headers=headers)
        response = r.json()
        if response and "isValid" in response:
            return response
    except:
        pass

    raise Exception("Error: there was a problem communicating with TagBackup")
