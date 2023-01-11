from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import json
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import IO
from typing import List
from typing import Optional
from typing import Union

from .build_constants import BUILD_GCLOUD_REST
from .session import SyncSession
from .token import Token
from .token import Type
from .utils import encode

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[assignment]

API_ROOT_IAM = 'https://iam.googleapis.com/v1'
API_ROOT_IAM_CREDENTIALS = 'https://iamcredentials.googleapis.com/v1'
SCOPES = ['https://www.googleapis.com/auth/iam']


class IamClient(object):
    def __init__(
        self, service_file                                   = None,
        session                    = None,
        token                  = None,
    )        :
        self.session = SyncSession(session)
        self.token = token or Token(
            service_file=service_file, scopes=SCOPES,
            session=self.session.session,  # type: ignore[arg-type]
        )

        if self.token.token_type not in {
            Type.GCE_METADATA,
            Type.SERVICE_ACCOUNT,
        }:
            raise TypeError(
                'IAM Credentials Client is only valid for use '
                'with Service Accounts or GCE Metadata',
            )

    def headers(self)                  :
        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
        }

    @property
    def service_account_email(self)                 :
        return self.token.service_data.get('client_email')

    # https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.keys/get
    def get_public_key(
        self, key_id                = None,
        key                = None,
        service_account_email                = None,
        project                = None,
        session                    = None,
        timeout      = 10,
    )                  :
        service_account_email = (
            service_account_email
            or self.service_account_email
        )
        project = project or self.token.get_project()

        if not key_id and not key:
            raise ValueError('get_public_key must have either key_id or key')

        if not key:
            key = (
                'projects/{}/serviceAccounts/'
                '{}/keys/{}'.format((project), (service_account_email), (key_id))
            )

        url = '{}/{}?publicKeyType=TYPE_X509_PEM_FILE'.format((API_ROOT_IAM), (key))
        headers = self.headers()

        s = SyncSession(session) if session else self.session

        resp = s.get(url=url, headers=headers, timeout=timeout)

        data                 = resp.json()
        return data

    # https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.keys/list
    def list_public_keys(
            self, service_account_email                = None,
            project                = None,
            session                    = None,
            timeout      = 10,
    )                        :
        service_account_email = (
            service_account_email
            or self.service_account_email
        )
        project = project or self.token.get_project()

        url = (
            '{}/projects/{}/'
            'serviceAccounts/{}/keys'.format((API_ROOT_IAM), (project), (service_account_email))
        )

        headers = self.headers()

        s = SyncSession(session) if session else self.session

        resp = s.get(url=url, headers=headers, timeout=timeout)

        data                       = (resp.json()).get('keys', [])
        return data

    # https://cloud.google.com/iam/credentials/reference/rest/v1/projects.serviceAccounts/signBlob
    def sign_blob(
        self, payload                             ,
        service_account_email                = None,
        delegates                      = None,
        session                    = None,
        timeout      = 10,
    )                  :
        service_account_email = (
            service_account_email
            or self.service_account_email
        )
        if not service_account_email:
            raise TypeError(
                'sign_blob must have a valid '
                'service_account_email',
            )

        resource_name = 'projects/-/serviceAccounts/{}'.format((service_account_email))
        url = '{}/{}:signBlob'.format((API_ROOT_IAM_CREDENTIALS), (resource_name))

        json_str = json.dumps({
            'delegates': delegates or [resource_name],
            'payload': encode(payload or '').decode('utf-8'),
        })

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(json_str)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session

        resp = s.post(
            url=url, data=json_str, headers=headers,
            timeout=timeout,
        )
        data                 = resp.json()
        return data

    def close(self)        :
        self.session.close()

    def __enter__(self)               :
        return self

    def __exit__(self, *args     )        :
        self.close()
