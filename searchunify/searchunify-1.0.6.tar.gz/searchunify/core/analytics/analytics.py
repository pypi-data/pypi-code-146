from searchunify.utils.constants.constants import AuthVariables
from searchunify.core.auth.auth_header_type import get_auth_header
from searchunify.utils.http_client.request_handler import *
from searchunify.utils.apis.apis import Apis
import json

API = Apis.get_apis('analytics')
AUTH_VARS = AuthVariables()

class Analytics:
    def get_tiles_data(**payload):
        url = AUTH_VARS.INSTANCE + API['tileData']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response

    def get_search_summary_chart(**payload):
        url = AUTH_VARS.INSTANCE + API['searchSummaryChart']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_all_search_query(**payload):
        url = AUTH_VARS.INSTANCE + API['searchQueryAll']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def get_search_queries_with_result(**payload):
        url = AUTH_VARS.INSTANCE + API['searchQueryWithResults']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response

    def search_queries_with_no_clicks(**payload):
        url = AUTH_VARS.INSTANCE + API['searchQueryWithNoClicks']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def search_queries_without_result(**payload):
        url = AUTH_VARS.INSTANCE + API['searchQueryWithoutResult']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def search_query_histogram(**payload):
        url = AUTH_VARS.INSTANCE + API['searchQueryHistogram']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def missed_query_histogram(**payload):
        url = AUTH_VARS.INSTANCE + API['missedQueryHistogram']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def search_session_by_case_uid_auth(**payload):
        url = AUTH_VARS.INSTANCE + API['searchSessionByCaseUidAuth']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_all_search_conversion(**payload):
        url = AUTH_VARS.INSTANCE + API['allSearchConversion']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def search_conversion_not_On_first_page(**payload):
        url = AUTH_VARS.INSTANCE + API['searchConversionNotOnFirstPage']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def search_conversion_with_filters(**payload):
        url = AUTH_VARS.INSTANCE + API['searchConversionWithFilters']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def search_conversion_by_sessionid(**payload):
        url = AUTH_VARS.INSTANCE + API['searchConversionBySessionId']
        url = url.replace("<searchSessionId>", str(payload['sessionId']), 1)
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def discussions_ready_to_become_article(**payload):
        url = AUTH_VARS.INSTANCE + \
            API['discussionsReadyToBecomeArticles']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def search_queries_in_sessions(**payload):
        url = AUTH_VARS.INSTANCE + API['searchSessionAllsearchQuery']
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def get_kcs_support_search_query(**payload):
        url = AUTH_VARS.INSTANCE + API['kcsSupport']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_search_session_by_case_uid(**payload):
        url = AUTH_VARS.INSTANCE + API['searchSessionByCaseUid']
        payload["caseUid"] = payload['caseUID']
        del payload['caseUID']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_search_session_by_search_sessionid(**payload):
        url = AUTH_VARS.INSTANCE + API['searchSessionBySearchSessionId']
        url = url.replace("<searchSessionId>", str(payload['sessionId']), 1)
        response = RequestManager.http_request(
            "GET", url, headers=get_auth_header(), params=payload)
        return response


    def get_case_created_articles(**payload):
        url = AUTH_VARS.INSTANCE + API['articlesCreatedCases']
        payload = re_modify_keys(**payload)
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_case_deflected_articles(**payload):
        url = AUTH_VARS.INSTANCE + API['articlesDeflectedCase']
        payload = re_modify_keys(**payload)
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_attached_articles(**payload):
        url = AUTH_VARS.INSTANCE + API['attachedArticles']
        payload = re_modify_keys(**payload)
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response


    def get_attached_on_case(**payload):
        url = AUTH_VARS.INSTANCE + API['attachedOnCase']
        payload = re_modify_keys(**payload)
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response

def re_modify_keys(**payload):
    payload["from"] = payload['startDate']
    payload["to"] = payload['endDate']
    payload["uid"] = payload['searchClientId']
    payload["limit"] = payload['count']
    del payload['startDate'],  payload['endDate'], payload['searchClientId'], payload['count']
    return payload

