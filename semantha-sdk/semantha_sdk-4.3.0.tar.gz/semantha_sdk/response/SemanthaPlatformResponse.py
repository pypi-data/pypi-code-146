from __future__ import annotations

import json
from typing import Dict

from requests import Response
from requests.structures import CaseInsensitiveDict

from semantha_sdk.response.SemanthaPlatformError import SemanthaPlatformError


class SemanthaPlatformResponse:
    def __init__(self, response: Response) -> None:
        self.__raw_response = response
        self.__content = _check_and_translate_errors(self.__raw_response).content

    def get_status_code(self) -> int:
        return self.__raw_response.status_code

    # TODO: we should parse the Dict and return something more simple
    def get_headers(self) -> CaseInsensitiveDict[str]:
        return self.__raw_response.headers

    def as_dict(self) -> Dict:
        response_as_dict = json.loads(self.__content.decode())
        if type(response_as_dict) is dict:
            return response_as_dict
        else:
            raise ValueError(f"Response content could not be converted to type 'dict':\n{self.__str__()}")

    def as_dict_or_none(self):
        try:
            return self.as_dict()
        except ValueError:
            return None

    def as_list(self) -> list:
        response_as_list = json.loads(self.__content.decode())
        if type(response_as_list) is list:
            return response_as_list
        else:
            raise ValueError(f"Response content could not be converted to type 'list':\n{self.__str__()}")

    def as_list_or_none(self):
        try:
            return self.as_list()
        except ValueError:
            return None

    # TODO: type hint via interface
    def to(self, dto_type):
        try:
            as_dict = self.as_dict_or_none()
            if as_dict is not None:
                return dto_type(as_dict)
            as_list = self.as_list_or_none()
            if as_list is not None:
                return dto_type(as_list)
        except ValueError:
            raise ValueError(f"The content of the semantha platform server response could not be converted to type "
                             f"'{dto_type.__str__()}'")

    def __str__(self) -> str:
        return self.__raw_response.__str__()


def _check_and_translate_errors(response: Response) -> Response:
    if response.status_code in [200, 201, 204]:
        return response
    else:
        if response.status_code == 400:
            raise ValueError(response.status_code, response.text)
        elif response.status_code == 401:
            raise PermissionError(response.status_code, response.text)
        elif response.status_code == 404:
            raise FileNotFoundError(response.status_code, response.text)
        elif response.status_code == 405:
            raise NotImplementedError(response.status_code, response.text)
        elif response.status_code == 408:
            raise TimeoutError(response.status_code, response.text)
        elif response.status_code == 500:
            raise SemanthaPlatformError(response.status_code, response.text)
        # elif response.status_code == 503:
        #     raise BusyError(response.status_code, response.text)
        else:
            raise RuntimeError(response.status_code, response.text)
