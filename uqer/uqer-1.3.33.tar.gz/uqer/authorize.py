# -*- coding: utf-8 -*-
# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2022
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2022 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.
from __future__ import unicode_literals
from __future__ import print_function

import sys
import requests
import traceback
import os

from .config import *
from .utils import format_print


class Authorize(object):
    """优矿
    """
    def __init__(self, token='', session=None):
        self.__token = token
        self.session = session


    def _authorize(self):
        """账户验证
        """
        token = self.__token
        if token:
            try:
                self._isvalid, is_network_ok = self.__is_token_valid(token)
            except SystemExit:
                raise
            if not is_network_ok:
                format_print('网络异常，无法验证token，请检查当前网络连通性', with_date=True)
            elif not self._isvalid:
                format_print('抱歉，您的 token 验证失败：{}'.format(token), with_date=True)
            else:
                token = self.__get_permanent_token_and_set_to_cookie(token=token)
                username = os.environ.get('DatayesPrincipalName', 'unknow')
                format_print('{} 账号登录成功'.format(username))


    def __get_permanent_token_and_set_to_cookie(self, token='', cookies={}):
        if not token:
            ret_json = requests.post(TOKEN_URL, data={'grant_type':'permanent'}, cookies=cookies).json()
            token = ret_json.get('access_token')

        self.__set_token_to_cookie(token)

        return token


    def __set_token_to_cookie(self, token):

        os.environ['access_token'] = token

        cookie_dict = {'cloud-sso-token': token}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
        return token


    # def __authorize_user(self, user, pwd):
    #
    #     ### 2 user type
    #     data_type = dict(username=user, password=pwd, app='mercury_sdk')
    #
    #     def user_type(data=None):
    #         res = self.session.post(AUTHORIZE_URL, data)
    #
    #         if not res.ok or not res.json().get('content', {}).get('accountId', 0):
    #             return False, None
    #         else:
    #             result = res.json()
    #             token = result.get('content', {}).get('token', {}).get('tokenString', '')
    #             principal_name = result.get('content', {}).get('principalName', '')
    #             os.environ['DatayesPrincipalName'] = principal_name
    #             return True, token
    #
    #     valid, token = user_type(data_type)
    #
    #     if not valid:
    #         return False, None
    #     else:
    #         os.environ['cloud_sso_token'] = token
    #         return True, token


    def __is_token_valid(self, token):
        """
        检验 token 是否有效
        Args:
             token: str
                用户token
        Returns: tuple
                 is_token_valid, is_network_ok
        """
        try:
            r = None
            r = self.session.get(PROFILE_URL, cookies={'cloud-sso-token': token})
            r_json = r.json()

            if type(r_json) == dict and r_json.get('code', 0) == 200:
                r = self.session.get(UQER_AUTH_URL, cookies={'cloud-sso-token': token})
                r_json = r.json()

                os.environ['DatayesPrincipalName'] = r_json['user']['principalName']
                # 校验用户是否有uqer.sdk.data的权限，若没有，则直接退出
                url = OPS_URL
                res = self.session.get(url, headers={'DatayesPrincipalName': os.environ['DatayesPrincipalName']},
                                       cookies={'cloud-sso-token': token})
                r_json = res.json()
                if r_json['code'] != 200:
                    format_print('获取用户权限数据异常', with_date=True)
                    return False, True

                if r_json['data'].get('uqer.sdk.data') is True:
                    for key, value in r_json['data'].items():
                        os.environ[key] = '1' if value is True else '0'
                    return True, True

                format_print('无UQER SDK权限，可以联系4000 820 386进行购买。')
                sys.exit(0)
            elif type(r_json) == dict and r_json.get('code', 0) == -403:
                format_print('token {} 无效或过期'.format(token), with_date=True)
                return False, True
            else:
                format_print('token 验证异常: {}'.format(r.text), with_date=True)
                return False, True
        except SystemExit:
            raise
        except:
            format_print('网络异常, 无法验证token', with_date=True)
            format_print('-' * 80)
            if r:
                format_print('Check token failed: url is %s, http code is %s, data is %s' % (PROFILE_URL, r.status_code, r.text), with_date=True)
            else:
                format_print('Check token failed: url is %s' % (PROFILE_URL), with_date=True)
            traceback.print_exc()
            format_print('-' * 80)
            return False, False









