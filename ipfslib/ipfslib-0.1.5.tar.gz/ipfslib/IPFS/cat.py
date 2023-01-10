import json
import requests

# Get content from IPFS by IPFS Path
def cat(api, ipfs_path, mode="t"):
    if ipfs_path[0:6] == '/ipfs/':
        content_hash = ipfs_path[6:]
    elif ipfs_path[0:6] == '/ipns/':
        ipns_name = {'arg': ipfs_path[6:]}
        raw_json = requests.post('http://{endpoint}/api/v0/name/resolve'.format(endpoint=api.endpoint), params=ipns_name).text
        content_hash = json.loads(raw_json)['Path'][6:]
    else:
        raise ValueError("IPFS Path has to start with '/ipfs/' or '/ipns/'")
    
    url = "http://{endpoint}/api/v0/block/get?arg={cid}".format(endpoint=api.endpoint, cid=content_hash)
    response = requests.post(url)
    if mode == "t":
        return response.text[6:-2]
    elif mode == "b":
        return response.content[6:-2]
    else:
        raise ValueError("mode has to bei either 't' (Text) or 'b' (Binary). Standard is 't'.")