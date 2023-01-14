import re
import time
import xml
import xml.dom.minidom
import random

from itchat import config
from itchat.components.login import logger

UOS_PATCH_EXT_SPAM = "Go8FCIkFEokFCggwMDAwMDAwMRAGGvAESySibk50w5Wb3uTl2c2h64jVVrV7gNs06GFlWplHQbY/5FfiO++1yH4ykC" \
                     "yNPWKXmco+wfQzK5R98D3so7rJ5LmGFvBLjGceleySrc3SOf2Pc1gVehzJgODeS0lDL3/I/0S2SSE98YgKleq6Uqx6ndTy9yaL9qFxJL7eiA/R" \
                     "3SEfTaW1SBoSITIu+EEkXff+Pv8NHOk7N57rcGk1w0ZzRrQDkXTOXFN2iHYIzAAZPIOY45Lsh+A4slpgnDiaOvRtlQYCt97nmPLuTipOJ8Qc5p" \
                     "M7ZsOsAPPrCQL7nK0I7aPrFDF0q4ziUUKettzW8MrAaiVfmbD1/VkmLNVqqZVvBCtRblXb5FHmtS8FxnqCzYP4WFvz3T0TcrOqwLX1M/DQvcHa" \
                     "GGw0B0y4bZMs7lVScGBFxMj3vbFi2SRKbKhaitxHfYHAOAa0X7/MSS0RNAjdwoyGHeOepXOKY+h3iHeqCvgOH6LOifdHf/1aaZNwSkGotYnYSc" \
                     "W8Yx63LnSwba7+hESrtPa/huRmB9KWvMCKbDThL/nne14hnL277EDCSocPu3rOSYjuB9gKSOdVmWsj9Dxb/iZIe+S6AiG29Esm+/eUacSba0k8" \
                     "wn5HhHg9d4tIcixrxveflc8vi2/wNQGVFNsGO6tB5WF0xf/plngOvQ1/ivGV/C1Qpdhzznh0ExAVJ6dwzNg7qIEBaw+BzTJTUuRcPk92Sn6QDn" \
                     "2Pu3mpONaEumacjW4w6ipPnPw+g2TfywJjeEcpSZaP4Q3YV5HG8D6UjWA4GSkBKculWpdCMadx0usMomsSS/74QgpYqcPkmamB4nVv1JxczYIT" \
                     "IqItIKjD35IGKAUwAA=="

#
setattr(config, "UOS_PATCH_EXT_SPAM", UOS_PATCH_EXT_SPAM)


def get_qr_uuid(self):
    url = '%s/jslogin' % config.BASE_URL
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
        "lang": "zh_CN",
        '_': int(time.time()),
        "redirect_uri": "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?mod=desktop"
    }
    headers = {'User-Agent': config.USER_AGENT}
    r = self.s.get(url, params=params, headers=headers)
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
    data = re.search(regx, r.text)
    if data and data.group(1) == '200':
        self.uuid = data.group(2)
        return self.uuid


def process_login_info(core, loginContent):
    ''' when finish login (scanning qrcode)
     * syncUrl and fileUploadingUrl will be fetched
     * deviceid and msgid will be generated
     * skey, wxsid, wxuin, pass_ticket will be fetched
    '''
    regx = r'window.redirect_uri="(\S+)";'
    core.loginInfo['url'] = re.search(regx, loginContent).group(1)
    headers = {
        'User-Agent': config.USER_AGENT,
        "client-version": "2.0.0",
        "extspam": getattr(config, "UOS_PATCH_EXT_SPAM"),  # panic directly if not set
    }
    r = core.s.get(core.loginInfo['url'], headers=headers, allow_redirects=False)
    core.loginInfo['url'] = core.loginInfo['url'][:core.loginInfo['url'].rfind('/')]
    for indexUrl, detailedUrl in (
            ("wx2.qq.com", ("file.wx2.qq.com", "webpush.wx2.qq.com")),
            ("wx8.qq.com", ("file.wx8.qq.com", "webpush.wx8.qq.com")),
            ("qq.com", ("file.wx.qq.com", "webpush.wx.qq.com")),
            ("web2.wechat.com", ("file.web2.wechat.com", "webpush.web2.wechat.com")),
            ("wechat.com", ("file.web.wechat.com", "webpush.web.wechat.com"))):
        fileUrl, syncUrl = ['https://%s/cgi-bin/mmwebwx-bin' % url for url in detailedUrl]
        if indexUrl in core.loginInfo['url']:
            core.loginInfo['fileUrl'], core.loginInfo['syncUrl'] = \
                fileUrl, syncUrl
            break
    else:
        core.loginInfo['fileUrl'] = core.loginInfo['syncUrl'] = core.loginInfo['url']
    core.loginInfo['deviceid'] = 'e' + repr(random.random())[2:17]
    core.loginInfo['BaseRequest'] = {}
    for node in xml.dom.minidom.parseString(r.text).documentElement.childNodes:
        if node.nodeName == 'skey':
            core.loginInfo['skey'] = core.loginInfo['BaseRequest']['Skey'] = node.childNodes[0].data
        elif node.nodeName == 'wxsid':
            core.loginInfo['wxsid'] = core.loginInfo['BaseRequest']['Sid'] = node.childNodes[0].data
        elif node.nodeName == 'wxuin':
            core.loginInfo['wxuin'] = core.loginInfo['BaseRequest']['Uin'] = node.childNodes[0].data
        elif node.nodeName == 'pass_ticket':
            core.loginInfo['pass_ticket'] = core.loginInfo['BaseRequest']['DeviceID'] = node.childNodes[0].data
    if not all([key in core.loginInfo for key in ('skey', 'wxsid', 'wxuin', 'pass_ticket')]):
        logger.error('Your wechat account may be LIMITED to log in WEB wechat, error info:\n%s' % r.text)
        core.isLogging = False
        return False
    return True


def check_login(self, uuid=None):
    uuid = uuid or self.uuid
    url = '%s/cgi-bin/mmwebwx-bin/login' % config.BASE_URL
    localTime = int(time.time())
    tip = getattr(self, '_tip', '1')
    if tip == '1':
        setattr(self, '_tip', '0')
    params = 'loginicon=true&uuid=%s&tip=%s&r=%s&_=%s' % (
        uuid, int(-localTime / 1579), tip, localTime)
    headers = {'User-Agent': config.USER_AGENT}
    r = self.s.get(url, params=params, headers=headers)
    regx = r'window.code=(\d+)'
    data = re.search(regx, r.text)
    if data and data.group(1) == '200':
        if process_login_info(self, r.text):
            return '200'
        else:
            return '400'
    elif data:
        return data.group(1)
    else:
        return '400'


def push_login(core):
    cookiesDict = core.s.cookies.get_dict()
    if 'wxuin' in cookiesDict:
        url = '%s/cgi-bin/mmwebwx-bin/webwxpushloginurl?uin=%s&mod=desktop' % (
            config.BASE_URL, cookiesDict['wxuin'])
        headers = {'User-Agent': config.USER_AGENT}
        r = core.s.get(url, headers=headers).json()
        if 'uuid' in r and r.get('ret') in (0, '0'):
            core.uuid = r['uuid']
            return r['uuid']
    return False
