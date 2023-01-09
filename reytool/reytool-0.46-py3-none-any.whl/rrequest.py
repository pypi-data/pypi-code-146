# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 11:07:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's request methods
"""


from typing import List, Dict, Tuple, Literal, Optional, Union
from faker import Faker
import requests
from requests import Response, JSONDecodeError

from .rbasic import error


# faker object
fake: Faker = Faker("zh_CN")

# Possible field names of Response code in Response data.
code_fields: List = ["code", "errno", "success"]

# Successful codes.
success_codes: List = [200, 204, 0, True]
success_codes_str = [str(code) for code in success_codes if type(code) == int]
success_codes.extend(success_codes_str)

def fake_headers() -> Dict:
    """
    Fake request headers.

    Returns
    -------
    Fake request headers.
    """

    headers = {}
    headers['user_agent'] = fake.android_platform_token()
    return headers

def check_response(
        response: Response,
        code_fields: List = code_fields,
        success_codes: List = success_codes,
        throw_error: bool = True
    ) -> Tuple[int, str]:
    """
    Check whether reponse is successful

    Parameters
    ----------
    response : Object from requests package.

    code_fields : Possible field names of Response code in Response data.

    success_codes : Successful codes.
    
    throw_error : Whether throw error.

    Returns
    -------
    Response code and Response message
    """

    reponse_code = response.status_code
    if reponse_code not in success_codes:
        check_info = reponse_code, response.text
        if throw_error:
            error(check_info)
        return check_info
    else:
        try:
            response_data = response.json()
        except JSONDecodeError:
            return 200, "success"
        if type(response_data) == dict:
            for field in code_fields:
                if field in response_data:
                    code = response_data[field]
                    if code in success_codes:
                        break
                    else:
                        check_info = code, response_data
                        if throw_error:
                            error(check_info)
                        return check_info
    return 200, "success"

def request(
    url: str,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Union[Dict, Literal["fake"]]] = None,
    timeout: Optional[Union[int, float]] = None,
    proxies: Optional[Dict[str, str]] = None,
    method: Optional[Literal["get", "post"]] = None,
    check: bool = True,
    code_fields: List = code_fields,
    success_codes: List = success_codes
    ) -> Response:
    """
    Send HTTP request.

    Parameters
    ----------
    url : Request URL.

    data : Request data. Parameter data and json conflict.

    json : Request data in JSON format. Parameter data and json conflict.

    headers : Request header.
        - Dict : Use dict as request header.
        - Literal['fake'] : Use fake request header.
        - None : No request header.

    timeout : Request maximun waiting time.
        - int, float : Use this value.
        - None : No limit.
    
    proxies : IP proxy setup.
        - Dict[str, str] : Name and use IP of each protocol.
        - None : 

    method : Request method.
        - None : Automatic judge.
            * When parameter data or json not has value, then request method is get.
            * When parameter data or json has value, then request method is post.
        - Literal['get'] : Request method is get.
        - Literal['post'] : Request method is post.

    check : Whether check response.

    code_fields : Possible field names of Response code in Response data.
    
    success_codes : Successful codes.

    Returns
    -------
    Response object of requests package.
    """
    
    if method == None:
        if data == None and json == None:
            method = "get"
        else:
            method = "post"
    if headers == "fake":
        headers = fake_headers()
    if method == "get":
        response = requests.get(url, data=data, json=json, headers=headers, timeout=timeout, proxies=proxies)
    elif method == "post":
        response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout, proxies=proxies)
    if check:
        check_response(response, code_fields, success_codes)
    return response