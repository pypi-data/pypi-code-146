from .connection import get_request, post_request_with_token, get_request_by_pk, patch_request_with_token, \
    get_request_int
from .decorator import cache_it
from .response_data import DataFactory

GET = "get"
POST = "post"
DELETE = "delete"
PATCH = "patch"
PUT = "put"

API_METHOD_INFO = [
    {
       "name": "parameter",
       "keyword": "parameter/",
       "actions": [GET, POST, PATCH]
    },
    {
        "name": "data_logger",
        "keyword": "data_logger/",
        "actions": [GET, POST, PATCH]
    },
    {
        "name": "sensor_on_data_logger",
        "keyword": "sensor_on_data_logger/",
        "actions": [GET, POST, PATCH]
    },
    {
        "name": "instrument_on_data_logger",
        "keyword": "instrument_on_data_logger/",
        "actions": [GET, POST, PATCH]
    },
    {
        "name": "data_logger_on_platform",
        "keyword": "data_logger_on_platform/",
        "actions": [GET, POST, PATCH]
    },
    {
        "name": "calibration",
        "keyword": "calibration/",
        "actions": [GET, POST, PATCH]
    },
    {
        "name": "calibration_event",
        "keyword": "calibration_event/",
        "actions": [GET, POST, PATCH]
    },
    {
        "name": "institution",
        "keyword": "institution/",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "project",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "manufacturer",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "instrument",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "instrument_on_platform",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "sensor",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "platform_type",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "platform",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "power",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "deployment",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "deployment_comment",
        "actions": [GET]
    },
    {
        "keyword": "platform_comment",
        "actions": [GET]
    },
    {
        "keyword": "sensor_on_instrument",
        "actions": [GET, POST, PATCH]
    },
    {
        "keyword": "deployment_hierarchy",
        "actions": [GET]
    }
]


def make_api_methods(sensor_tracker_api, api_info):
    for a in api_info:
        method_instance = api_method_factory(a)
        setattr(sensor_tracker_api, method_instance.__name__, method_instance)


class BaseAPIMethod:
    def __init__(self, api_info):
        self.api_key_word = api_info["keyword"]
        self._info = api_info

    def get(self, *args, **kwargs):
        if hasattr(self, "_get"):
            if args:
                payload = args[0]
                if type(payload) is not int:
                    payload["format"] = 'json'
            else:
                payload = {"format": 'json'}
            args = (payload,)
            return self._get(self, *args, **kwargs)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self, 'get'))

    def post(self, *args, **kwargs):
        if hasattr(self, "_post"):
            return self._post(self, *args, **kwargs)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__name__, 'post'))

    def patch(self, *args, **kwargs):
        if hasattr(self, "_patch"):
            return self._patch(self, *args, **kwargs)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__name__, 'patch'))
    #
    # def delete(self, *args, **kwargs):
    #     if hasattr(self, "_delete"):
    #         return self._delete(self, *args, **kwargs)
    #     else:
    #         raise AttributeError("'{}' object has no attribute '{}'".format(self, 'delete'))


def api_method_factory(api_info):
    method_name = api_info["name"] if "name" in api_info else api_info["keyword"]

    @cache_it(api_info["keyword"])
    def get(self, payload=None):
        type_of_payload = type(payload)
        if type_of_payload is dict:
            # todo: make a input argument parser here?
            r = get_request(self.api_key_word, payload)
        elif type_of_payload is int:
            r = get_request_int(self.api_key_word, payload)
        else:
            msg = "Payload should be either dictionary or integer"
            raise AttributeError(msg)
        return DataFactory(r).generate()

    def post(self, payload):
        return post_request_with_token(self.api_key_word, payload)

    def patch(self, target_obj_id, payload):
        return patch_request_with_token(self.api_key_word, target_obj_id, payload)

    i = BaseAPIMethod(api_info)
    i.__name__ = method_name
    for action in api_info["actions"]:
        if GET is action:
            setattr(i, "_" + GET, get)

        if POST is action:
            setattr(i, "_" + POST, post)

        if PATCH is action:
            setattr(i, "_" + PATCH, patch)

    return i
