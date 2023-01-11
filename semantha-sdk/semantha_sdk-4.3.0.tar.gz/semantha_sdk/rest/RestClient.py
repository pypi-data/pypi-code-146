from __future__ import annotations

from requests import Request

from semantha_sdk.request import SemanthaRequest


class RestClient:

    def __init__(self, server_url: str, api_key: str):
        self.__server_url = server_url
        self.__api_key = api_key

    def __build_headers_for_json_request(self) -> dict[str, str]:
        return {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.__api_key}'
        }

    def __request(self,
                  method,
                  url,
                  headers=None,
                  files=None,
                  data=None,
                  params=None,
                  auth=None,
                  cookies=None,
                  hooks=None,
                  json=None
                  ) -> SemanthaRequest:
        if headers is None:
            headers = self.__build_headers_for_json_request()
        request = Request(
            method=method,
            url=self.__server_url + url,
            headers=headers,
            files=files,
            data=data,
            params=params,
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            json=json
        )
        prepared_request = request.prepare()
        return SemanthaRequest(prepared_request)

    def get(self, url: str, q_params: dict[str, str] = None) -> SemanthaRequest:
        return self.__request("GET", url, params=q_params)

    def post(self, url: str, body: dict = None, json: dict = None, q_params: dict[str, str] = None) -> SemanthaRequest:
        if body is None and json is None:
            raise ValueError("Either a body (files/form-data) or a json must be provided!")
        return self.__request("POST", url, files=body, json=json, params=q_params)

    # TODO: Needs to accept list of dicts as well!
    def delete(self, url: str, q_params: dict[str, str] = None) -> SemanthaRequest:
        return self.__request("DELETE", url, params=q_params)

    def patch(self, url: str, body: dict = None, json: dict = None, q_params: dict[str, str] = None) -> SemanthaRequest:
        if body is None and json is None:
            raise ValueError("Either a body (files/form-data) or a json must be provided!")
        return self.__request("PATCH", url, files=body, json=json, params=q_params)

    def put(self, url: str, body: dict = None, json: dict = None, q_params: dict[str, str] = None) -> SemanthaRequest:
        if body is None and json is None:
            raise ValueError("Either a body (files/form-data) or a json must be provided!")
        return self.__request("PUT", url, files=body, json=json, params=q_params)
