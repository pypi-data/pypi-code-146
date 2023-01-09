# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import requests, warnings, os, requests, pdb

defaul_url = 'https://ultronsandbox.oss-cn-hangzhou.aliyuncs.com/version/jdw.json'
version_url = os.environ.get('jdw_version_url', defaul_url)

if 'MQ_URL' not in os.environ:
    warnings.warn('if use distributed calculating, please configure MQ_URL')
    os.environ['MQ_URL'] = 'guet:guet@127.0.0.1:12345'

if 'NTN_URL' not in os.environ:
    warnings.warn('if use distributed calculating, please configure NTN_URL')
    os.environ['NTN_URL'] = 'guet:guet@127.0.0.1:12345/jdw'

if 'KN_MG' not in os.environ:
    warnings.warn('if use memory database, please configure KN_MG')
    os.environ['KN_MG'] = 'guet:guet@127.0.0.1:12345/jdw'

if 'DB_URL' not in os.environ:
    warnings.warn('if use sql database, please configure DB_URL')
    os.environ['DB_URL'] = 'guet:guet@127.0.0.1:12345/jdw'

if 'ATL_URL' not in os.environ:
    warnings.warn('if use trader, please configure ATL_URL')
    os.environ['ATL_URL'] = 'guet:guet@127.0.0.1:12345/jdw'

if 'IREY_URL' not in os.environ:
    warnings.warn('if use trader, please configure IREY_URL')
    os.environ['IREY_URL'] = 'guet:guet@127.0.0.1:12345/jdw'

try:
    import jdw.mfc.oss as OSSAPI
except ImportError:
    warnings.warn("pip install --upgrade oss")
try:
    import jdw.data.DataAPI.mg as MGAPI
except ImportError:
    warnings.warn("pip install --upgrade pymongo")

try:
    import jdw.data.DataAPI.db as DBAPI
except ImportError:
    warnings.warn("pip install --upgrade SQLCharmy")

import jdw.data.SurfaceAPI as SurfaceAPI

try:
    import jdw.mfc.experimental.DataAPI.mg as ExperimentalAPI
    import jdw.mfc.irey as IreyAPI
    import jdw.mfc.deckard as DeckardAPI
    import jdw.mfc.lombard as LombardAPI
    import jdw.data.ExternalAPI as ExternalAPI
    import jdw.mfc.entropy as EntropyAPI
    #from jdw.mfc.neutron.factory import Factory
    #NeutronAPI = Factory()
except ImportError:
    warnings.warn("pip install --upgrade  Jindowin")
#try:
#    import jdw.mfc.anode as AnodeAPI
#except ImportError:
#    warnings.warn("the environment cannot be traded")

from .version import __version__

try:
    unicode
except:
    unicode = str

session = requests.Session()


def get_version():
    res = requests.get(version_url).json()
    if res.get('code') != 200:
        return '', ''

    remote_version = res['data']['version']
    content = res['data']['content']

    return remote_version, content


def check_version():
    remote_version, content = get_version()
    if not remote_version or remote_version <= __version__:
        return
    print(
        'JinDowin version is upgraded from %s to %s, upgrade content %s, execute pip install --upgrade Finance-Jindowin'
        % (__version__, remote_version, content))


check_version()