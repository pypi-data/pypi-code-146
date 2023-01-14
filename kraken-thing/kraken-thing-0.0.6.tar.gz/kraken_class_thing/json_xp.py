import json
import datetime

def default_json(obj):

    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj:
            new_obj[key] = default_json(value)
    elif isinstance(obj, list):
        new_obj = []
        for item in obj:
            new_obj.append(default_json(item))
    elif isinstance(obj, (datetime.date, datetime.datetime)):
        new_obj = obj.isoformat()
    else:
        new_obj = obj

    return new_obj

def convert_string_to_dates(record):

    if isinstance(record, dict):
        new_record = {}
        for key, value in record.items():
            new_record[key] = convert_string_to_dates(value)

    elif isinstance(record, list):
        new_record = []
        for item in record:
            new_record.append(convert_string_to_dates(item))
    else:
        new_record = record
        try:
            if record:
                new_record = datetime.datetime.fromisoformat(record)
        except Exception as e:
            a=1
    return new_record


def dumps(record):
    return json.dumps(record, default=default_json, indent=4)

def loads(string):
    record = json.loads(string)
    return convert_string_to_dates(record)

