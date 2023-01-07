# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


import os
import sys
import requests
from requests import utils
from .version import __version__
utils.default_user_agent = lambda: 'mercury-sdk/%s' % __version__

from . import uqer
from .uqer import Client
from .mfclient import neutralize, standardize, winsorize, simple_long_only, long_only, neutralize_pit
from . import DataAPI

from .utils import format_print

from .DataAPI import retry_interval, max_retries
from .DataAPI.api_base import __getConn__


def get_user_traffic():
    principal_name = os.environ['DatayesPrincipalName']
    user_traffic = {}
    try:
        server = __getConn__()
        url = 'https://{}:{}/data/v1/api/getUserTraffic?user={}'.format(server[2], server[3], principal_name)
        response = requests.get(url=url, timeout=5)
        if response.status_code != 200:
            raise Exception(response.text)

        response = response.json()
        if response['success'] is False:
            raise Exception(response)

        for item in response['data']:
            if item['prd_src'] == 'mercury_sdk':
                user_traffic['bytes_limit'] = item['bytes_limit']
                user_traffic['bytes_current'] = item['bytes_current']
                break

        if len(user_traffic) == 0:
            # 异常情况先置空
            user_traffic['bytes_limit'] = 0
            user_traffic['bytes_current'] = 0

        return user_traffic
    except Exception as e:
        raise e


try:
    DataAPI.api_base.replace_api_files()
    for e in list(sys.modules.keys()):
        if e.startswith('DataAPI') or e.startswith('uqer.DataAPI'):
            del sys.modules[e]
    from . import DataAPI
    DataAPI.get_user_traffic = get_user_traffic
except:
    import traceback
    format_print(traceback.format_exc(), with_date=True)
    format_print('upgrade fail.', with_date=True)
