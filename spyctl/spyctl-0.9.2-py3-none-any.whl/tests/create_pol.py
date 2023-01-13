import argparse
import json
import sys

import requests
import yaml

TIMEOUT = (6.10, 300)


def post(url, data, key):
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.post(url, data, headers=headers, timeout=TIMEOUT)
    if r.status_code != 200:
        print(r.status_code, r.reason, str(r.headers), r.text)
    else:
        print("Success!")


def put(url, data, key):
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.put(url, json=data, headers=headers, timeout=TIMEOUT)
    if r.status_code != 200:
        raise RuntimeError(r.status_code, r.reason)
    else:
        print("Success!")
    return r


def post_new_policy(api_url, api_key, org_uid, data):
    url = f"{api_url}/api/v1/org/{org_uid}/analyticspolicy/"
    resp = post(url, data, api_key)
    return resp


def load_resource_file(filename):
    try:
        with open(filename) as f:
            resrc_data = yaml.load(f, yaml.Loader)
    except Exception:
        try:
            resrc_data = json.load(filename)
        except Exception:
            err_exit("Unable to load resource file.")
    if not isinstance(resrc_data, dict):
        err_exit("Resource file does not contain a dictionary.")
    return resrc_data


def err_exit(message: str):
    sys.stderr.write(f"Error: {message}\n")
    exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("api_key")
    parser.add_argument("api_url")
    parser.add_argument(
        "-o", "--org_uid", default="spyderbatuid", required=False
    )
    args = parser.parse_args()
    return args


options = parse_args()
filename = options.filename
resource_data = load_resource_file(filename)
api_url = options.api_url
api_key = options.api_key
org_uid = options.org_uid
post_new_policy(api_url, api_key, org_uid, resource_data)
