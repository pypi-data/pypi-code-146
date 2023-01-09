"""Base Class with helper methods common to all modules"""

import json
import logging
from http import HTTPStatus

import requests
from oauth2_xfel_client.oauth2_client_backend import Oauth2ClientBackend

from ..common.config import CREATE, DELETE, UPDATE, GET, SET, \
    DEF_MAX_RETRIES, DEF_TIMEOUT, DEF_SSL_VERIFY


def default_headers(user_email):
    return {
        'content-type': 'application/json',
        'Accept': 'application/json; version=2',
        'X-User-Email': user_email,
    }


class Base:
    def __init__(self, *,
                 base_api_url, use_oauth2=True,
                 client_id='', client_secret='',
                 token_url='', refresh_url='', auth_url='', scope='',
                 user_email='',
                 session_token=None,
                 max_retries=DEF_MAX_RETRIES,
                 timeout=DEF_TIMEOUT,
                 ssl_verify=DEF_SSL_VERIFY):

        if use_oauth2:
            self.oauth_client = Oauth2ClientBackend(
                client_id=client_id,
                client_secret=client_secret,
                scope=scope,
                token_url=token_url,
                refresh_url=refresh_url,
                auth_url=auth_url,
                session_token=session_token,
                max_retries=max_retries,
                timeout=timeout,
                ssl_verify=ssl_verify
            )
            self.session = self.oauth_client.session

        else:
            # Oauth disabled - used with base_api_url pointing to an
            # xfel-oauth-proxy instance
            self.oauth_client = None
            self.session = requests.Session()

        self.headers = default_headers(user_email)
        # Ensure the base URL has a trailing slash
        self.base_api_url = base_api_url.rstrip('/') + '/'

    @staticmethod
    def load_json_from_str(hash_str):
        if hash_str == '' or hash_str == '[]':
            return {}
        else:
            return json.loads(hash_str)

    @staticmethod
    def load_json_from_content(response):
        return Base.load_json_from_str(response.content.decode('utf8'))

    @staticmethod
    def load_json_from_headers(response):
        headers = {}

        try:
            if response.headers is None:
                return headers
        except Exception as exp:
            return headers

        headers['Date'] = response.headers.get('Date')
        headers['X-Total-Pages'] = response.headers.get('X-Total-Pages')
        headers['X-Count-Per-Page'] = response.headers.get('X-Count-Per-Page')
        headers['X-Current-Page'] = response.headers.get('X-Current-Page')
        headers['X-Total-Count'] = response.headers.get('X-Total-Count')

        return headers

    @staticmethod
    def format_response(response, action, success_code, module_name):
        r_content = Base.load_json_from_content(response)
        r_pagination = Base.load_json_from_headers(response)

        # print('-' * 100)
        # print('r_content: ' + str(r_content))
        # print('action: ' + str(action))
        # print('success_code: ' + str(success_code))
        # print('module_name: ' + str(module_name))

        # Standard situation in case of success
        if response.status_code == success_code and r_content:
            res = Base.response_success(module_name, action,
                                        r_pagination, r_content)

        # Successful set operation on Reports may return 200 or 201
        elif action == SET and response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED] and r_content:
            res = Base.response_success(module_name, action,
                                        r_pagination, r_content)

        # In case there is nothing to report (e.g. delete operation success)
        elif response.status_code == HTTPStatus.NO_CONTENT and not r_content:
            res = Base.response_success(module_name, action,
                                        r_pagination, r_content)

        # This else if covers search return data (e.g. find_by_name)
        elif response.status_code == success_code and r_content == []:
            res = Base.response_success(module_name, action,
                                        r_pagination, r_content)

        # Protects from having a success response, but an empty hash was sent
        elif response.status_code == success_code and r_content == {}:
            res = Base.response_error(module_name, action, r_content)

        # In any other case an Error is reported
        else:
            if 'info' in r_content:
                app_info = r_content['info']
            else:
                app_info = '{}: expected {}, got {}'.format(
                    "HTTP response unexpected status code",
                    success_code, response.status_code)
            res = Base.response_error(module_name, action, app_info)

        return res

    @staticmethod
    # TODO, Make it validate and return key, value criteria
    def unique_key_format_result(res, module_name, unique_id=None):
        if len(res['data']) > 0:
            data = res['data'][0]
            info = res['info']
        else:
            data = {}

            if unique_id:
                info = '{0} "{1}" could not be found!'.format(module_name,
                                                              unique_id)
            else:
                info_msg = 'No {0} could be found respecting the specified ' \
                           'search criteria'
                info = info_msg.format(module_name)

        res = {'success': res['success'],
               'info': info,
               'app_info': res['app_info'],
               'pagination': Base.load_json_from_headers(res),
               'data': data}
        return res

    @staticmethod
    def response_success(module_name, action, r_pagination, r_content):
        if action == CREATE:
            msg = '{0} created successfully'.format(module_name)
        elif action == UPDATE:
            msg = '{0} updated successfully'.format(module_name)
        elif action == GET:
            msg = 'Got {0} successfully'.format(module_name)
        elif action == DELETE:
            msg = '{0} deleted successfully'.format(module_name)
        elif action == SET:
            msg = '{0} set successfully'.format(module_name)
        else:
            return Base.response_error(module_name, action, r_content)

        res = {'success': True,
               'info': msg,
               'app_info': {},
               'pagination': r_pagination,
               'data': r_content}
        logging.debug('response_success => {0}'.format(res))
        return res

    @staticmethod
    def response_error(module_name, action, app_info):
        if action == CREATE:
            msg = 'Error creating {0}'.format(module_name)
        elif action == UPDATE:
            msg = 'Error updating {0}'.format(module_name)
        elif action == GET:
            msg = '{0} not found!'.format(module_name)
        elif action == DELETE:
            msg = 'Error deleting {0}'.format(module_name)
        elif action == SET:
            msg = 'Error setting {0}'.format(module_name)
        else:
            msg = 'ACTION is not correct!'

        res = {'success': False,
               'info': msg,
               'app_info': app_info,
               'pagination': {},
               'data': {}}
        logging.debug('response_error => {0}'.format(res))
        return res

    @staticmethod
    def cal_debug(c_name, m_name, r_content):
        msg = '*** {0}.{1} (content) => {2}'.format(c_name, m_name, r_content)
        logging.debug(msg)

    # Method that generates the RESTful API URL
    def get_api_url(self, model_name, api_specifics=''):
        complete_api_specifics = '{0}{1}'.format(model_name, api_specifics)
        return '{0}{1}'.format(self.base_api_url, complete_api_specifics)

    def api_get(self, api_url, **kwargs):
        """Sends a GET request. Returns :class:`Response` object.
        :param api_url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault('allow_redirects', True)

        return self.session.get(api_url, headers=self.headers, **kwargs)

    def api_post(self, api_url, **kwargs):
        """Sends a POST request. Returns :class:`Response` object.
        :param api_url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault('allow_redirects', True)

        return self.session.post(api_url, headers=self.headers, **kwargs)

    def api_put(self, api_url, **kwargs):
        """Sends a PUT request. Returns :class:`Response` object.
        :param api_url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault('allow_redirects', True)

        return self.session.put(api_url, headers=self.headers, **kwargs)

    def api_delete(self, api_url, **kwargs):
        """Sends a DELETE request. Returns :class:`Response` object.
        :param api_url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault('allow_redirects', True)

        return self.session.delete(api_url, headers=self.headers, **kwargs)
