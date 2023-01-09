import json
import requests

# Lists all IPNS keys
def list(api):
    response = requests.post('http://{endpoint}/api/v0/key/list'.format(endpoint=api.endpoint))
    raw_json = response.text
    try:
        return json.loads(raw_json)['Keys']
    except KeyError:
        raise Exception(response['Message'])