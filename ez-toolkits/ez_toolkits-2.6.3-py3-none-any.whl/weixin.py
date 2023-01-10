import json
import time

import requests


class work(object):

    '''
    企业微信开发者中心

        https://developer.work.weixin.qq.com/
        https://developer.work.weixin.qq.com/document/path/90313 (全局错误码)

    参考文档:

        https://www.gaoyuanqi.cn/python-yingyong-qiyewx/
        https://www.jianshu.com/p/020709b130d3
    '''

    _work_id, _agent_id, _agent_secret, _access_token = None, None, None, None

    def __init__(self, work_id, agent_id, agent_secret):
        ''' Initiation '''
        self._work_id = work_id
        self._agent_id = agent_id
        self._agent_secret = agent_secret

        ''' 获取 Token '''
        self.get_access_token()

    def get_access_token(self):
        _response = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self._work_id}&corpsecret={self._agent_secret}')
        if _response.status_code == 200:
            _result = _response.json()
            self._access_token = _result.get('access_token')
        else:
            self._access_token = None

    def get_agent_list(self):

        self.get_access_token() if self._access_token == None else next

        _response = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/agent/list?access_token={self._access_token}')

        if _response.status_code == 200:
            _response_data = _response.json()
            if _response_data.get('errcode') == 42001:
                self.get_access_token()
                time.sleep(1)
                self.get_agent_list()
            return _response_data
        return {'response': _response.text}

    def get_department_list(self, id):

        self.get_access_token() if self._access_token == None else next

        _response = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={self._access_token}&id={id}')

        if _response.status_code == 200:
            _response_data = _response.json()
            if _response_data.get('errcode') == 42001:
                self.get_access_token()
                time.sleep(1)
                self.get_department_list(id)
            return _response_data
        return {'response': _response.text}

    def get_user_list(self, id):

        self.get_access_token() if self._access_token == None else next

        _response = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={self._access_token}&department_id={id}')

        if _response.status_code == 200:
            _response_data = _response.json()
            if _response_data.get('errcode') == 42001:
                self.get_access_token()
                time.sleep(1)
                self.get_user_list(id)
            return _response_data
        return {'response': _response.text}

    def get_user_id_by_mobile(self, mobile):

        self.get_access_token() if self._access_token == None else next

        _json_dict = {'mobile': mobile}

        _json_string = json.dumps(_json_dict)

        _response = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?access_token={self._access_token}', data=_json_string)

        if _response.status_code == 200:
            _response_data = _response.json()
            if _response_data.get('errcode') == 42001:
                self.get_access_token()
                time.sleep(1)
                self.get_user_id_by_mobile(id)
            return _response_data
        return {'response': _response.text}

    def get_user_info(self, id):

        self.get_access_token() if self._access_token == None else next

        _response = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={self._access_token}&userid={id}')

        if _response.status_code == 200:
            _response_data = _response.json()
            if _response_data.get('errcode') == 42001:
                self.get_access_token()
                time.sleep(1)
                self.get_user_info(id)
            return _response_data
        return {'response': _response.text}

    def send_text(self, users, message):
        '''
        https://developer.work.weixin.qq.com/document/path/90235
        '''

        self.get_access_token() if self._access_token == None else next

        _json_dict = {
            'touser': users,
            'msgtype': 'text',
            'agentid': self._agent_id,
            'text': {'content': message},
            'safe': 0,
            'enable_id_trans': 0,
            'enable_duplicate_check': 0,
            'duplicate_check_interval': 1800
        }

        _json_string = json.dumps(_json_dict)

        _response = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self._access_token}', data=_json_string)

        if _response.status_code == 200:
            _response_data = _response.json()
            if _response_data.get('errcode') == 42001:
                self.get_access_token()
                time.sleep(1)
                self.send_text(users, message)
            return _response_data
        return {'response': _response.text}
