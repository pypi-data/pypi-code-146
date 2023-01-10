import json
import requests

# Remove file from ipfs (by CID)
def rem(api, content_hash, force=True):
    params = {
        'arg': content_hash,
        'force': force
    }

    response = requests.post('http://{endpoint}/api/v0/add'.format(endpoint=api.endpoint), params=params) 
    raw_json = response.text