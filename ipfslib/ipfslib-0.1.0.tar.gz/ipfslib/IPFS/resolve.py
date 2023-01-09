import json
import requests

# Resolve IPNS name
def resolve(api, ipns_name):
    params = {
        'arg': ipns_name,
    }

    response = requests.post('http://{endpoint}/api/v0/add'.format(endpoint=api.endpoint), params=params)
    raw_json = response.text
    return json.loads(raw_json)['Path']