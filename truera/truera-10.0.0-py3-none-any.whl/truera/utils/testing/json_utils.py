import json


def json_load_for_test(str):
    try:
        return json.loads(str)
    except json.decoder.JSONDecodeError as e:
        print(f"JSON decoding failed on string: {str}")
        raise e
