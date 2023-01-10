import json
import requests

# Adds file to ipfs
def add(api, filepath, mode='t'):
    if mode == 't':
        read_mode = 'r'
    elif mode == 'b':
        read_mode = 'rb'
    else:
        raise ValueError("Mode has to be either 't' or 'b'.")
    files = {
        'file': open(filepath, read_mode),
    }
    response = requests.post('http://{endpoint}/api/v0/add'.format(endpoint=api.endpoint), files=files)
    raw_json = response.text
    try:
        return json.loads(raw_json)["Hash"]
    except KeyError:
        raise Exception(response['Message'])