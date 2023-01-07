import json

# data = {
#     "success_sound" : True,
#     "fail_sound" : True
#     }

# json_string = json.dumps(data)
# print(json_string)

# # Directly from dictionary
# with open('json_data.json', 'w') as outfile:
#     json.dump(json_string, outfile)
  
# # Using a JSON string
# with open('json_data.json', 'w') as outfile:
#     outfile.write(json_string)




# import json

# with open('json_data.json') as json_file:
#     data = json.load(json_file)
# info = json.loads(data)


def dump_as_json(data, path):
    with open(path, "w") as f: json.dump(json.dumps(data), f)
    
def get_from_json(path):
    with open(path) as f: data = json.load(f)
    info = json.loads(data)
    return info