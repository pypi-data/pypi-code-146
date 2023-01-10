import json
import requests

def get(api, content_hash, mode="t"):
    url = "http://{endpoint}/api/v0/block/get?arg={cid}".format(endpoint=api.endpoint, cid=content_hash)
    response = requests.post(url)
    if mode == "t":
        return response.text[6:-2]
    elif mode == "b":
        return response.content[8:-2]
    else:
        raise ValueError("mode has to bei either 't' (Text) or 'b' (Binary). Standard is 't'.")
