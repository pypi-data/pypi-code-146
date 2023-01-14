import base64
import json
import requests

# This tool connects to the cat-cfs/ciri_info repo, accessing the designated file(s) (in this case, just classifiers.json)
# and then copies the contents to an output.json file.

CIRI_INFO = "https://api.github.com/repos/cat-cfs/ciri_info"
CONTENTS = "/contents"
JSON = "/lookups.json"
REPO_URL = CIRI_INFO + CONTENTS + JSON
TOKEN = "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" #EXPIRES DEC. 17, 2022

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v4+raw"
}

response = requests.get(REPO_URL, headers=headers)

if response and response.status_code == 200:
    binary_content = base64.b64decode(response.json()["content"])
    content = binary_content.decode("utf-8")
    json_loads = json.loads(content)
    json_dumps = json.dumps(json_loads, indent=4)

    with open("./githubReader/output.json", "w") as outfile:
        outfile.write(json_dumps)
    
else:
    print(response)