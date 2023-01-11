#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

_BASE_URL = "https://api.comapsmarthome.com/"


class ComapSmartHome(object):
    service_url_suffix = ''

    def __init__(self, auth):
        self.auth = auth
        self._request_header = None
        self.base_url = _BASE_URL + self.service_suffix

    @property
    def request_header(self):
        requests_header = {
            "Authorization": "Bearer {}".format(self.auth.token),
            "Content-Type": "application/json"
        }
        return requests_header

    @staticmethod
    def get_request(url, headers, params={}):
        r = requests.get(url=url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def post_request(url, headers, data={}):
        r = requests.post(url=url, headers=headers, json=data)
        r.raise_for_status()
        return None if r.text == '' else r.json()

    @staticmethod
    def put_request(url, headers, data={}):
        r = requests.put(url=url, headers=headers, json=data)
        r.raise_for_status()
        return None if r.text == '' else r.json()

    @staticmethod
    def patch_request(url, headers, data={}):
        r = requests.patch(url=url, headers=headers, json=data)
        r.raise_for_status()
        return None if r.text == '' else r.json()

    @staticmethod
    def delete_request(url, headers, data={}):
        r = requests.delete(url=url, headers=headers, data=data)
        r.raise_for_status()
        return None if r.text == '' else r.json()
