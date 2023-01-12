import requests
import logging

from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

from enum import Enum

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from .error import EloquaException

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

logger = logging.getLogger('eloqua.client')

LOGIN_URL = 'https://login.eloqua.com'
API_VERSION = '2.0'
TOKEN_URL = LOGIN_URL + '/auth/oauth2/token'


class AuthType(Enum):
    BASIC = 1,
    OAUTH2 = 2


class EloquaBulkClient(object):

    def __init__(
        self,
        username,
        password,
        bulk_url,
        client_id=None,
        client_secret=None,
        debug=False
    ):
        """
        Initialize the instance with the given parameters.
        Available kwargs
        :param bulk_url - Bulk API url

        Basic Authentication:
        :param company - Eloqua site name
        :param username - Eloqua user name
        :param password - Eloqua user password


        OAuth 2.0 authentication:
        :param client_id - the client id generated for the user
        :param client_secret - the client secret generated for the user

        """
        self.bulk_url = bulk_url
        self.debug = debug

        basic_auth_args = (username, password)
        oauth_args = (username, password, client_id, client_secret)
        # Determine if the user wants to use OAuth 2.0 for added security
        # Eloqua supports Resource Owner Password Credentials Grant
        if all(arg is not None for arg in oauth_args):
            self.oauth = OAuth2Session(
                client=LegacyApplicationClient(client_id=client_id),
                auto_refresh_url=TOKEN_URL,
                token_updater=self.token_updater)

            self.token = self.oauth.fetch_token(
                token_url=TOKEN_URL,
                username=username,
                password=password,
                client_id=client_id,
                client_secret=client_secret)

            self.auth_type = AuthType.OAUTH2

        elif all(arg is not None for arg in basic_auth_args):
            self.auth = HTTPBasicAuth(*basic_auth_args)
            self.auth_type = AuthType.BASIC

        else:
            raise TypeError(
                'You must provide login information.'
            )

        self.valid_until = None
        self.base_url = None

    def token_updater(self, token):
        self.token = token

    def execute(self, method, *args, **kwargs):

        method_map = {
            'create_export': self.create_export,
            'create_sync': self.create_sync,
            'check_sync_status': self.check_sync_status,
            'get_synced_data': self.get_synced_data,
            'get_fields': self.get_fields,
            'create_import': self.create_import,
            'upload_data': self.upload_data,
            'get_sync_rejects': self.get_sync_rejects
        }
        result = method_map[method](*args, **kwargs)
        return result

    """
    entity: accounts, activities, campaignResponses, contacts
    """
    def create_export(
        self,
        name,
        entity,
        fields=None,
        filter=None,
        customObjectId=None,
        customObjectName=None,
        activityType=None,
        areSystemTimestampsInUTC=False
    ):
        # if fields aren't provided, then fetch all fields of the entity
        if fields is None:
            if entity == 'contacts':
                fields = self._get_fields_dict(entity=entity)
            elif entity == 'customObjects':
                fields = self._get_fields_dict(
                    entity=entity,
                    parentId=customObjectId,
                    parentName=customObjectName)
            elif entity == 'activities':
                fields = self._get_fields_dict(
                    entity=entity,
                    activityType=activityType)

        data = {
            'name': name,
            'fields': fields,
            'filter': filter,
            'areSystemTimestampsInUTC': areSystemTimestampsInUTC
        }

        if entity in ('contacts', 'activities'):
            url = '{base_url}/{entity}/exports'.format(
                base_url=self.bulk_url, entity=entity)
        elif entity == 'customObjects':
            cdo_id = customObjectId
            if cdo_id is None and customObjectName is not None:
                cdo_id = self._get_custom_object_id(
                    custom_object_name=customObjectName)
            else:
                raise TypeError(
                    '''Either customObjectId or customObjectName
                    must be provided'''
                )

            url = '{base_url}/{entity}/{parentId}/exports'.format(
                base_url=self.bulk_url, entity=entity, parentId=cdo_id)

        resp = self.post(url, data)

        return resp

    def create_import(
        self,
        name,
        entity,
        fields,
        parent_id=None,
        identifier_field_name=None,
        auto_delete_duration='P7D',
        data_retention_duration='P7D',
        is_sync_triggered_on_import=False,
        is_updating_multiple_matched_records=False,
        map_data_cards=False,
        map_data_cards_case_sensitive_match=False,
        map_data_cards_entity_field=None,
        map_data_cards_entity_type=None,
        map_data_cards_source_field=None,
        null_identifier_field_name=False,
        sync_actions=None,
        update_rule_by_field=None
    ):

        data = {
            'name': name,
            'fields': fields,
            'identifierFieldName': identifier_field_name,
            'autoDeleteDuration': auto_delete_duration,
            'dataRetentionDuration': data_retention_duration,
            'isSyncTriggeredOnImport': is_sync_triggered_on_import,
            'isUpdatingMultipleMatchedRecords':
                is_updating_multiple_matched_records,
            'nullIdentifierFieldName': null_identifier_field_name,
            'syncActions': sync_actions,
            'updateRuleByField': update_rule_by_field
        }

        if (entity == 'customObjects'):
            data['mapDataCards'] = map_data_cards
            data['mapDataCardsSensitiveMatch'] = map_data_cards_case_sensitive_match
            data['mapDataCardsEntityField'] = map_data_cards_entity_field
            data['mapDataCardsEntityType'] = map_data_cards_entity_type
            data['mapDataCardsSourceField'] = map_data_cards_source_field
            url = '{base_url}/{entity}/{parent_id}/imports'.format(
                base_url=self.bulk_url,
                parent_id=parent_id,
                entity=entity
            )
        else:
            url = '{base_url}/{entity}/imports'.format(
                base_url=self.bulk_url,
                entity=entity
            )

        resp = self.post(url, data)

        return resp

    def create_sync(self, synced_instance_uri, callback_url=None):
        data = {
            'syncedInstanceUri': synced_instance_uri,
            'callbackUrl': callback_url
        }

        url = '{base_url}/syncs'.format(base_url=self.bulk_url)

        resp = self.post(url, data)
        return resp

    def get_sync_rejects(
        self,
        sync_uri,
        offset,
        limit
    ):
        url = f"{self.bulk_url}{sync_uri}/rejects"
        return self.get(url, {'limit': limit, 'offset': offset})

    def upload_data(self, sync_instance_uri, data):
        url = '{base_url}{sync_instance_uri}'.format(
            base_url=self.bulk_url,
            sync_instance_uri=sync_instance_uri
        )

        return self.post(url, data)

    def check_sync_status(self, sync_uri):

        url = '{base_url}{sync_uri}'.format(
            base_url=self.bulk_url,
            sync_uri=sync_uri
        )

        resp = self.get(url)
        return resp

    def get_synced_data(self, sync_uri, offset, batch_size):

        url = '{base_url}{sync_uri}/data?limit={limit}&offset={offset}'.format(
            base_url=self.bulk_url,
            sync_uri=sync_uri,
            limit=batch_size,
            offset=offset)

        resp = self.get(url)

        return resp

    def get_fields(
        self,
        entity,
        parentId=None,
        parentName=None,
        activityType=None
    ):
        if entity in ('contacts', 'activities'):
            url = '{base_url}/{entity}/fields'.format(
                base_url=self.bulk_url,
                entity=entity)

            resp = self.get(url)
            fields = resp['items']

            if entity == 'contacts':
                return fields

            if activityType is not None:
                filtered = []
                for field in fields:
                    if activityType in field['activityTypes']:
                        filtered.append(field)

                return filtered

            return fields

        elif entity == 'customObjects':
            if parentId is not None:
                url = '{base_url}/{entity}/{parentId}/fields'.format(
                    base_url=self.bulk_url,
                    entity=entity,
                    parentId=parentId)

                resp = self.get(url)
                fields = resp['items']

                return fields
            elif parentName is not None:
                cdo_id = self._get_custom_object_id(
                    custom_object_name=parentName)

                url = '{base_url}/{entity}/{parentId}/fields'.format(
                    base_url=self.bulk_url,
                    entity=entity,
                    parentId=cdo_id)

                resp = self.get(url)
                fields = resp['items']

                return fields
            else:
                raise TypeError(
                    '''You must provide parentId (custom object id)
                    or parentName (custom object name)'''
                )

    def _get_custom_object_id(self, custom_object_name):
        if custom_object_name is None:
            raise TypeError(
                '''custom_object_name is required'''
            )

        url = "{base_url}/{entity}?q=name='{parentName}'".format(
            base_url=self.bulk_url,
            entity='customObjects',
            parentName=custom_object_name)

        resp = self.get(url)
        cdos = resp['items']

        if len(cdos) == 0:
            raise Exception(
                '''CDO with the name %s not found''' % custom_object_name
            )
        elif len(cdos) > 1:
            raise Exception(
                '''There are more than one CDO having
                this name: %s''' % custom_object_name
            )
        else:
            cdo = cdos[0]
            cdo_id = int(cdo['uri'].split('/')[-1])

            return cdo_id

    def _get_fields_dict(
        self,
        entity,
        parentId=None,
        parentName=None,
        activityType=None
    ):
        fields_dict = {}
        fields = self.get_fields(entity, parentId, parentName, activityType)

        for field in fields:
            fields_dict[field['internalName']] = field['statement']

        return fields_dict

    def make_request(self, **kwargs):
        if self.debug:
            logger.info(u'{method} Request: {url}'.format(**kwargs))
            if kwargs.get('json'):
                logger.info('payload: {json}'.format(**kwargs))

        if self.auth_type == AuthType.OAUTH2:
            resp = self.oauth.request(**kwargs)
        else:
            resp = requests.request(auth=self.auth, **kwargs)

        if self.debug:
            logger.info(u'{method} response: {status}'.format(
                method=kwargs['method'],
                status=resp.status_code))

        return resp

    def post(self, url, data=None, headers=None):
        if not headers:
            headers = {
                'Accept': 'application/json'
            }
        elif 'Accept' not in headers.keys():
            headers['Accept'] = 'application/json'

        try:
            r = self.make_request(**dict(
                method='POST',
                url=url,
                json=data,
                headers=headers
            ))
        except RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise EloquaException(r.reason, r.text)
            if r.status_code == 204:
                return None
            return r.json()

    def get(self, url, headers=None, **queryparams):
        if not headers:
            headers = {
                'Accept': 'application/json'
            }
        elif 'Accept' not in headers.keys():
            headers['Accept'] = 'application/json'

        if len(queryparams):
            url += '?' + urlencode(queryparams)

        try:
            r = self.make_request(**dict(
                method='GET',
                url=url,
                headers=headers
            ))
        except RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise EloquaException(r.reason, r.text)
            return r.json()
