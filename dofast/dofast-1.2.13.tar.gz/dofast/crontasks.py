''' crontab tasks. '''
from abc import ABC, abstractmethod
import enum
import socket
import time
import urllib.parse

import codefast as cf
import pydantic
from apscheduler.schedulers.background import BackgroundScheduler
from .toolkits.telegram import Channel
import os
from dofast.auth import auth 
socket.setdefaulttimeout(30)

postman = Channel('messalert')

class consts(object):
    INITIAL_COST = 0


class ExpendData(pydantic.BaseModel):
    name: pydantic.constr(strip_whitespace=True)
    expDate: str
    amount: str
    discountFee: str
    isSpecial: str

    def __str__(self):
        return f"<p> {self.name} | {self.amount} </p>"


class MobileEndpoints(enum.Enum):
    balance = 'https://h5.ha.chinamobile.com/h5-rest/balance/data'
    flow = 'https://h5.ha.chinamobile.com/h5-rest/flow/data'
    action = 'https://h5.ha.chinamobile.com/hnmccClient/action.dox'


class PhoneInfo(ABC):
    def __init__(self) -> None:
        self.params = {'channel': 2, 'version': '7.0.2'}
        self.rate_bucket_cnt = 0
        self.error_cnt = 0
        self.header_key = '7103_cmcc_headers'
        self.headers = {}

    def is_cookie_expired(self) -> bool:
        js = self.check_once(MobileEndpoints.balance.value)
        if js and '未登录' in js.get('msg', ''):
            cf.warning('cookie is invalid')
            return True
        cf.info('cookie is valid')
        return False

    def get_cookies(self) -> dict:
        auth_sign = urllib.parse.unquote(auth.cmcc['auth_sign'])
        cmcc_headers = auth.cmcc['header']
        resp = cf.net.post(MobileEndpoints.action.value,
                           data={'authSign': auth_sign},
                           headers=cmcc_headers)
        msg = {
            'auth_sign': auth_sign,
            'cmcc_headers': cmcc_headers,
            'resp': resp.text,
            'status_code': resp.status_code,
            'action': 'get_cookies'
        }
        cf.info(msg)
        return resp.cookies

    def get_headers(self) -> dict:
        if self.headers:
            return self.headers
        headers = auth.cmcc['header']
        cookies = self.get_cookies()
        jssesionid = cookies['JSESSIONID']
        sso = cookies['hncmjsSSOCookie']
        cookie = "JSESSIONID={}; hncmjsSSOCookie={}; WT_FPC=id=2fd3232b80e3c48ef421648804206287:lv=1658274294270:ss=1658274293912; mobile=13943-4355-6269-29599; VersionName=7.0.3".format(
            jssesionid, sso)
        headers['Cookie'] = cookie
        cf.info({'headers': headers, 'action': 'get_headers'})
        self.headers = headers
        return headers

    def check_once(self, endpoint: str) -> dict:
        try:
            headers = self.get_headers()
            resp = cf.net.get(endpoint, data=self.params, headers=headers).json()
            cf.info('using header', headers)
            cf.info('check once result', resp)
            return resp
        except Exception as e:
            cf.error('check once error:', e)
            return {'error': str(e)}

    @abstractmethod
    def get_cost_summary(self) -> str:
        pass

    @abstractmethod
    def get_flow_summary(self) -> str:
        pass


class PapaPhone(PhoneInfo):
    def __init__(self) -> None:
        super().__init__()

    def get_cost_summary(self) -> str:
        js = self.check_once(MobileEndpoints.balance.value)
        if 'data' not in js or js['data'] is None or 'expendList' not in js['data']:
            msg = ''
        else:
            expend = list(map(ExpendData.parse_obj, js['data']['expendList']))
            msg = '\n'.join(map(str, expend))
        return msg

    def get_flow_summary(self) -> str:
        js = self.check_once(MobileEndpoints.flow.value)
        if 'data' not in js:
            msg = ''
        elif js['data'] is None or js['data'].get('flowList') is None:
            msg = ''
        else:
            msg = "<p> name | all | remain </p>\n"
            for flow in js['data']['flowList']:
                if not flow or flow['details'] is None:
                    continue
                for d in flow['details']:
                    if d['expireFlag']:
                        continue  # ignore expired flow
                    msg += '<p> {} | {} | {} </p>\n'.format(
                        d['name'], d['totalFlow'], d['flowRemain'])
        return msg

    def get_summary(self) -> str:
        msg = self.get_cost_summary()
        msg += '-' * 30 + '\n'
        time.sleep(1)
        msg += self.get_flow_summary()
        return msg


def create_telegraph_page(msg: str) -> str:
    from telegraph import Telegraph
    telegraph = Telegraph()
    telegraph.create_account(short_name=cf.random_string(10))
    response = telegraph.create_page(
        cf.random_string(16),
        html_content=msg,
    )
    msg = response['url']
    return msg


if __name__ == '__main__':
    pp = PapaPhone()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=pp.post_summary,
                      trigger='cron',
                      hour='8',
                      minute='21',
                      timezone='Asia/Shanghai')
    cf.info('scheduler started')
    while True:
        time.sleep(1)
