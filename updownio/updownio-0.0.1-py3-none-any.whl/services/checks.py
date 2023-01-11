# -*- coding: utf-8 -*-
# Copyright (C) 2023 Adrien Delle Cave
# SPDX-License-Identifier: GPL-3.0-or-later
"""updownio.services.checks"""


import logging

from six import ensure_text
from updownio.service import UpDownIoServiceBase, SERVICES


_DEFAULT_API_PATH = "api/checks"

LOG               = logging.getLogger('updownio.checks')


class UpDownIoChecks(UpDownIoServiceBase):
    SERVICE_NAME = 'checks'

    @staticmethod
    def get_default_api_path():
        return _DEFAULT_API_PATH

    @staticmethod
    def _build_recipients(recipients):
        r = []

        if not isinstance(recipients, (tuple, list)):
            return r

        for i, x in enumerate(recipients):
            if isinstance(x, str):
                r.append(('recipients[]', x))

        return r

    def list(self):
        return self.mk_api_call()

    def show(self, token, params = None):
        return self.mk_api_call(token, params)

    def downtimes(self, token, page = 1, results = False):
        return self.mk_api_call("%s/downtimes" % token,
                                {'page': int(page),
                                 'results': bool(results)})

    def metrics(self, token, xfrom = None, to = None, group = None):
        return self.mk_api_call("%s/metrics" % token,
                                {'from': xfrom,
                                 'to': to,
                                 'group': group})

    def add(self, url, data = None):
        if not isinstance(data, dict):
            data = {}

        data['url'] = url
        recipients  = data.pop('recipients', None)
        data        = list(data.items())

        if recipients:
            data.extend(self._build_recipients(recipients))

        return self.mk_api_call(method = 'POST', data = data)

    def update(self, token, data = None):
        if not isinstance(data, dict):
            data = {}

        recipients = data.pop('recipients', None)
        data       = list(data.items())

        if recipients:
            data.extend(self._build_recipients(recipients))

        return self.mk_api_call("%s" % token,
                                method = 'PUT',
                                data = data)

    def delete(self, token):
        return self.mk_api_call("%s" % token,
                                method = 'DELETE')

if __name__ != "__main__":
    def _start():
        SERVICES.register(UpDownIoChecks())
    _start()
