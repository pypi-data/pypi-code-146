import json
import requests

# Renames key
def rename(api, key_name, new_name):
    params = {
        'arg': [
            key_name,
            new_name,
        ],
    }
    response = requests.post('http://{endpoint}/api/v0/key/rename'.format(endpoint=api.endpoint), params=params)
    raw_json = response.text
    return json.loads(raw_json)