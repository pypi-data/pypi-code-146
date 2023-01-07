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

import requests
import traceback
import os

env = os.getenv('env', 'prd')
gw_env = os.getenv('gw_env', 'prd')

if env == 'prd' or (env == 'local' and gw_env == 'prd'):
    server = ('10.22.220.82', 80, 'api.wmcloud.com', 443)
    URL_PREFIX = 'https://{}.datayes.com'
    EXT_MFHANDLER_HOST = 'https://gw.datayes.com/mercury_ops'
    BRAIN_HOST = 'https://gw.datayes.com/mercury_brain'
    PING_URL = "https://{}.datayes.com/mercury_community/w/ping"
else:
    server = ('10.22.220.42', 80, 'api.wmcloud-stg.com', 443)
    URL_PREFIX = 'https://{}.wmcloud-stg.com'
    EXT_MFHANDLER_HOST = 'https://gw.wmcloud-stg.com/mercury_ops'
    BRAIN_HOST = "https://gw.datayes-stg.com/mercury_brain"
    PING_URL = 'https://{}.datayes-stg.com/mercury_community/w/ping'


FOLDERS = []
LOCAL_PATH = './'

### URL Config
URL = {}
URL_TEMPLATE = {}

### NOTEBOOK, DATA
update = URL_TEMPLATE.update(
    {
        # 'AUTHORIZE_URL': "/usermaster/authenticate/v1.json",
        'TOKEN_URL': "/usermaster/whitelist/token/permanent.json?isUqer=true",
        'MERCURY_URL': '/mercury/api/databooks', 'UQER_AUTH_URL': '/cloud/identity/uqer.json',
        'DATA_URL': '/mercury/databooks', 'NOTEBOOK_URL': '/mercury/api/notebooks?recursion',
        'NOTEBOOK_DELETE': '/mercury/api/notebooks/{}?force=1', 'DOWN_NOTEBOOK_URL': '/mercury/files',
        'SDK_URL': "/mercury_community",
        'PROFILE_URL': "/mercury_community/profile",
        'OPS_URL': '/mercury_ops/uqer/authorization'
    }
)

SDK_STATIC_URL = 'http://uqer.datayes.com/pro/download/sdk/uqer_sdk.zip'


### Live Trading
URL_TEMPLATE.update({
    'Live_Trading_URL' : "/mercury_trade/strategy",
    'Live_Order_URL' : "/mercury_trade/strategy/{}/order",
    'Live_Access_URL': '/mercury_trade/api/uqer_data/authorizaiton'
})

### User factor
URL_TEMPLATE.update({
    'Create_Factor': '/mercury_trade/customfactor',
    'Upload_FactorData': '/mercury_trade/customfactordata',
    'Get_Factor': '/mercury_trade/customfactor'
})

def check_gateway(gw=None):
    
    GATEWAY = ['gw', 'gw01', 'gw02', 'gw03']

    global URL, URL_TEMPLATE, URL_PREFIX, PING_URL
    ### 检查是否自定义网关
    if gw:
        good_gw = gw
    else:
        ### 网关检测
        good_gw = 'gw'
        for _gw in GATEWAY:
            _url = PING_URL.format(_gw)
            try:
                r = requests.get(_url)
                if r.ok:
                    good_gw = _gw
                    break
            except:
                print ('网关测试过程发生错误，错误信息如下：')
                traceback.print_exc()
                continue

    URL_PREFIX = URL_PREFIX.format(good_gw)

    ### 配置 URL
    for k,v in URL_TEMPLATE.items():
        URL[k] = URL_PREFIX + v

    return URL


URL = check_gateway()


def get_url(url_name):
    """利用此函数实现动态 url
    """
    global URL
    url = URL.get(url_name, '')

    if not url:
        print ('url 获取失败')
        print ('url 名字: {}'.format(url_name))
        print ('当前 url 池: {}'.format(url_name))
        raise ValueError('Error')
    else:
        return url

# AUTHORIZE_URL = get_url('AUTHORIZE_URL')
TOKEN_URL = get_url('TOKEN_URL')
MERCURY_URL = get_url('MERCURY_URL')
PROFILE_URL = get_url('PROFILE_URL')
UQER_AUTH_URL = get_url('UQER_AUTH_URL')
NOTEBOOK_URL = get_url('NOTEBOOK_URL') 
NOTEBOOK_DELETE = get_url('NOTEBOOK_DELETE') 
DATA_URL = get_url('DATA_URL') 
DOWN_NOTEBOOK_URL = get_url('DOWN_NOTEBOOK_URL') 
SDK_URL = get_url('SDK_URL')
Live_Trading_URL = get_url('Live_Trading_URL') 
Live_Order_URL = get_url('Live_Order_URL') 
Create_Factor = get_url('Create_Factor') 
Upload_FactorData = get_url('Upload_FactorData') 
Get_Factor = get_url('Get_Factor')
OPS_URL = get_url('OPS_URL')
Live_Access_URL = get_url('Live_Access_URL')



### python 3.x unicode
try:
    unicode
except:
    unicode = str


