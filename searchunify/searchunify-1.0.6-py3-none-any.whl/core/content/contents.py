from searchunify.utils.http_client.request_handler import RequestManager
from searchunify.core.auth.auth_header_type import get_auth_header
from searchunify.utils.constants.constants import AuthVariables
from searchunify.utils.apis.apis import Apis
import urllib.parse
import re
import json

API = Apis.get_apis('content')
AUTH_VARS = AuthVariables()

def replace_all(url, replacedObject):
    rep = dict((re.escape(k), urllib.parse.quote_plus(urllib.parse.quote_plus(v))) for k, v in replacedObject.items())
    pattern = re.compile("|".join(rep.keys()))
    url = pattern.sub(lambda m: rep[re.escape(m.group(0))], url)
    return url

class Content:
    def get_content_sources():
        url = AUTH_VARS.INSTANCE + API['contentSources']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header())
        return response


    def get_content_source_by_id(**payload):
        url = AUTH_VARS.INSTANCE + \
            API['contentSourceByID'] + "/" + str(payload['contentSourceId'])
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header())
        return response


    def get_object_and_fields(**payload):
        url = AUTH_VARS.INSTANCE + API['objectAndFields']
        url = url.replace("<contentSourceId>", str(payload['contentSourceId']), 1)
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header())
        return response


    def get_object_specific_data(**payload):
        url = AUTH_VARS.INSTANCE + API['objectData']
        replacedObject = {"<contentSourceId>": str(
            payload['contentSourceId']), "<objectId>": str(payload['objectId'])}
        url = replace_all(url, replacedObject)
        if payload.get("offset"):
            payload["from"] = payload.get("offset")
            del payload["offset"]
        del payload["contentSourceId"], payload["objectId"]
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def get_object_specific_data_with_id(**payload):
        url = AUTH_VARS.INSTANCE + API['objectDataWithId']
        replacedObject = {"<contentSourceId>": str(payload['contentSourceId']), "<objectId>": str(
            payload['objectId']), "<documentId>": str(payload['documentId'])}
        url = replace_all(url, replacedObject)
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def update_doucment_by_id(**payload):
        url = AUTH_VARS.INSTANCE + API['updateDoucmentById']
        replacedObject = {"<contentSourceId>": str(payload['contentSourceId']), "<objectId>": str(
            payload['objectId']), "<documentId>": str(payload['documentId'])}
        url = replace_all(url, replacedObject)
        payload = json.dumps(payload['data'])
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def upload_data(**payload):
        url = AUTH_VARS.INSTANCE + API['bulkUpload']
        replacedObject = {"<contentSourceId>": str(
            payload['contentSourceId']), "<objectId>": str(payload['objectId'])}
        url = replace_all(url, replacedObject)
        payload = {
            "bulkData": payload['data']
        }
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response
