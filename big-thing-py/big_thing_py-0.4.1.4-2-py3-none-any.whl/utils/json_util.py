from big_thing_py.common import *
from big_thing_py.utils.log_util import *

import json


def json_string_to_dict(jsonstring: str) -> Union[str, Dict]:
    try:
        if type(jsonstring) in [str, bytes]:
            return json.loads(jsonstring)
        else:
            return jsonstring

    except json.JSONDecodeError as e:
        # TODO: will be removed if middleware ME/NOTIFY_CHANGE payload issue is fixed
        # print_error(e)
        # SOPLOG_DEBUG(
        #     f'[json_string_to_dict] input string must be json format string... return raw string...', 'red')
        return False


def dict_to_json_string(dict_object: dict) -> str:
    try:
        if type(dict_object) == dict:
            return json.dumps(dict_object, sort_keys=True, indent=4)
        elif type(dict_object) == list:
            return '\n'.join([json.dumps(item, sort_keys=True, indent=4) for item in dict_object])
        else:
            return str(dict_object)
    except Exception as e:
        SOPLOG_DEBUG('[dict_to_json_string] ' + str(e), 'red')
        return False
