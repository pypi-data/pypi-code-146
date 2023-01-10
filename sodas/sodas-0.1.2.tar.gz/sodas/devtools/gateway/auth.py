import os
import json

import requests


def _get_access_token(base_url: str, id:str, refreshToken:str) :
    optionUserLogin = {
        'url': 'http://' + base_url + '/api/v1/gateway/authentication/user/refreshUser',
        'data': {
            'id' : id,
            'refreshToken' : refreshToken
        }
    }

    try :
        res = requests.post(optionUserLogin['url'],
                        data=optionUserLogin['data']
                        )

        if res.status_code != 201:
            raise Exception(res.status_code)
        else :
            res = res.json()
    except Exception as e:
        print(e)

    return res['accessToken']

def get_refresh_token(base_url: str, id: str, password: str) -> str:
    """User의 ID와 Password를 넣으면 refresh token을 얻을 수 있도록 함

    Args:
        base_url (str): Base URL
        id (str): User ID
        password (str): User Password

    Raises:
        Exception: Fail to login

    Returns:
        str: User's Refresh Token
    """

    optionUserLogin = {
        'url': 'http://' + base_url + '/api/v1/gateway/authentication/user/login',
        'data': {
            'id' : id,
            'password': password,
            'offline': 'false'
        },
    }

    try :
        res = requests.post(optionUserLogin['url'],
                    data=optionUserLogin['data'])

        if res.status_code != 201:
            raise Exception(res.status_code)
        else :
            res = res.json()
    except Exception as e:
        print(e)

    return res['refreshToken']