#!/usr/bin/env python3
'''
This module contains the methods to connect to NetOrca platform
and carry out basic functions usual for ansible integrations.
'''

import logging
from urllib.parse import urljoin
import requests

import netorca_sdk.constants as const


class Connection:
    '''
    Base class to handle connectivity and basic functions to NetOrca
    '''
    def __init__(self, base_url, username=None,  password=None, api_key=None):
        '''
        Initialises the class and connection to the NetOrca platform
        :param base_url: url of NetOrca deployment
        :param username: Username for NetOrca login
        :param password: Password for NetOrca login
        :param api_key: API_key for NetOrca login (will be used as first preference)
        '''
        self.base_url = base_url
        self.api_key = api_key
        self.username = username
        self.password = password
        self._login()

    def _login(self):
        '''
        Logs into the NetOrca platform via api key or via username and password generating a token
        :return: None
        '''
        url = urljoin(self.base_url, const._PATH_LOGIN)
        if self.api_key:
            self.header = {
                'Authorization': f'Api-Key { self.api_key }',
                'content_type': 'application/json'
            }
            response = requests.get(urljoin(self.base_url, const._PATH_TEAMS), headers=self.header)
            if response.status_code != 200:
                raise ConnectionRefusedError('api_key not valid on the NetOrca deployment')
        else:
            data = {
                "username": self.username,
                "password": self.password
            }
            response = requests.post(url, json=data)
            if response.status_code == 200 and 'token' in response.json():
                token = response.json()['token']
                self.header = {
                    'Authorization': f'Token { response.json()["token"] }',
                    'content-type': 'application/json'
                }
            else:
                raise ConnectionRefusedError('Supplied username and password not accepted by NetOrca platform')

    def post(self, path, data):
        '''
        Post to the NetOrca api
        :param path: NetOrca path
        :param data: Data to post in JSON
        :return: Requests response
        '''
        url = urljoin(self.base_url, path)
        return requests.post(url, json=data, headers=self.header)

    def put(self, path, data):
        '''
        Put to the NetOrca API
        :param path: NetOrca path
        :param data: Data to put in JSON
        :return: Request reponse
        '''
        url = urljoin(self.base_url, path)
        return requests.put(url, json=data, headers=self.header)

    def get(self, path, filters=None):
        '''
        Gets from the netorca api
        :param path: NetOrca path
        :param filters: dict of filters to apply
        :return: Requests reponse
        '''
        url = urljoin(self.base_url, path)
        return requests.get(url, params=filters, headers=self.header)


class BaseObj:
    '''
    Base NetOrca Object
    '''
    def __init__(self, conn, context, input):
        '''
        Initialise the object
        '''
        self.conn = conn
        self.input = input
        self.context=context
        self._map_fields()

    def _map_fields(self):
        '''
        Map fields from the input to methods
        :return: None
        '''
        try:
            class_map = getattr(self, 'class_map')
            for key, value in self.input.items():
                if key in class_map.keys():
                    class_ = getattr(class_map[key]['module'], class_map[key]['name'])
                    setattr(self, key, class_(self.conn, self.context, value))
                else:
                    setattr(self, key, value)
        except AttributeError:
            for key, value in self.input.items():
                setattr(self, key, value)


class Endpoint:
    '''
    Base class to handle endpoint connection to the NetOrca api
    '''
    def __init__(self, conn, context):
        '''
        Endpoint base class, requires an initialised NetOrca connection class
        :param connection: Connection cls
        '''
        self.conn = conn
        self.context = context
        try:
            getattr(self, 'settings')
            getattr(self, 'class_')
        except AttributeError:
            raise RuntimeError('Endpoint class should not be used directly')
        self._set_path()
        self.objs = []

    def _set_path(self):
        '''
        Sets the path based on the context input and settings
        :return: None
        '''
        try:
            if self.context == 'owner':
                self.path = self.settings['owner_path']
            elif self.context == 'consumer':
                self.path = self.settings['consumer_path']
            else:
                raise RuntimeError('Context not supported')
        except KeyError:
            raise RuntimeError('Incorrectly configured class')

    def supported_filters(self):
        '''
        Returns a list of supported filters on this cllass
        :return: list
        '''
        try:
            return self.settings['filters']
        except KeyError:
            logging.warning('No filters specified for this class')
            return None

    def get_all(self, **kwargs):
        '''
        Gets all items for this endpoint type
        :param kwargs: named filter arguments
        :return: None
        '''
        filters = kwargs
        response = self.conn.get(path=self.path, filters=filters)
        if response.status_code == 200:
            for item in response.json()['results']:
                self.objs.append(self.class_(self.conn, self.context, item))
        else:
            raise ConnectionError(f' { response.status_code } return from API, '
                                  f'something went wrong. Log details: \n\n{ response.text }')

    def get_single(self, uuid):
        '''
        Gets a single instance of the endpoint object
        :param uuid: str -> uuid of object
        :return: Obj class instance
        '''
        url = urljoin(self.path, uuid)
        response = self.conn.get(path=url)
        if response.status_code==200:
            return self.class_(self.conn, self.context, response.json())
        else:
            logger.warning('Obj not found')
            return None
