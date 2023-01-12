import json
import requests
from qbeast.config import ENDPOINT, get_bearer_token


def send_post(path, json_data):
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bearer {get_bearer_token()}"
    headers["Content-Type"] = "application/json"

    req = requests.post(f"{ENDPOINT}{path}",
                        headers=headers,
                        json=json_data)
    try:
        response_msg = req.json()
    except json.JSONDecodeError as e:
        response_msg = req.text

    return req.status_code in [200, 201], response_msg


def send_get(path):
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bearer {get_bearer_token()}"

    req = requests.get(f"{ENDPOINT}{path}",
                       headers=headers)
    try:
        response_msg = req.json()
    except json.JSONDecodeError as e:
        response_msg = req.text

    return req.status_code == 200, response_msg
