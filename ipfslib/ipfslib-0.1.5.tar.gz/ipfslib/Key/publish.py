import json
import requests

# Publishes content to IPNS key
def publish(api, content_hash, key_name="self", lifetime="24h"):
    params = {
        'arg': content_hash,
        'resolve': 'true',
        'lifetime': lifetime,
        'key': key_name,
        'allow-offline': 'true',
        'ipns-base': 'base36'
    }
    response = requests.post('http://{endpoint}/api/v0/name/publish'.format(endpoint=api.endpoint), params=params)
    response = json.loads(response.text)
    try:
        return [response['Name'], response['Value']]
    except KeyError:
        raise Exception(response['Message'])