import json
import requests

# Adds file to ipfs
def add(api, filepath):
    files = {
        'file': open(filepath, 'r'),
    }
    response = requests.post('http://{endpoint}/api/v0/add'.format(endpoint=api.endpoint), files=files)
    raw_json = response.text
    return json.loads(raw_json)["Hash"]