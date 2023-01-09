import json

with open('/Users/kishore/Downloads/single_item_found/docs_vec.csv', 'w') as wf:
    with open('/Users/kishore/Downloads/single_item_found/docs.jsonl') as rf:
        for line in rf:
            try:
                doc = json.loads(line)
                if not "vectorClipV1" in doc:
                    continue

                print(doc)
                is_valid = (doc["accessLevel"] == "PUBLIC" and doc["hideFromDiscovery"] != True)
                doc["is_valid"] = is_valid
                value_str = ','.join([str(i) for i in doc["vectorClipV1"]])
                value_str += ',1' if is_valid else ',0'
                wf.write(value_str + "\n")
            except:
                pass
