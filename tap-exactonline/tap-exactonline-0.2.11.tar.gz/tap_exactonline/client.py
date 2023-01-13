"""REST client handling, including ExactOnlineStream base class."""


from pathlib import Path
from typing import Optional, Iterable
import urllib.parse

from exactonline.storage import ExactOnlineConfig, MissingSetting
from singer_sdk.authenticators import SingletonMeta
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from memoization import cached

from tap_exactonline.helpers.ExactApiWrapper import ExactWrapperApi
from tap_exactonline.helpers.parser import ODataParser
from exactonline.resource import GET

import logging

from tap_exactonline.helpers.secretsManager import get_secret

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ExactOnlineStorage(ExactOnlineConfig):
    def __init__(
            self,
            base_url: str = None,
            rest_url: str = None,
            auth_url: str = None,
            token_url: str = None,
            client_id: str = None,
            client_secret: str = None,
            access_token: str = None,
            refresh_token: str = None,
            access_expiry: int = None,
            division: int = None,
            secret_id: str = None
    ):
        self._store = {
            'server': {
                'auth_url': auth_url,
                'rest_url': rest_url,
                'token_url': token_url,
            },
            'application': {
                'base_url': base_url,
                'client_id': client_id,
                'client_secret': client_secret,
                'iteration_limit': 5000,
                'secret_id': secret_id,
            },
            'transient': {
                'access_expiry': access_expiry,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'division': division,
            }
        }

    def get(self, section, option):
        try:
            return self._store[section][option]
        except:
            raise MissingSetting(option)

    def set(self, section, option, value):
        if section not in self._store:
            self._store[section] = {}
        self._store[section][option] = value


class ExactClientSingleton(ExactWrapperApi, metaclass=SingletonMeta):
    """Exact singleton"""


class ExactOnlineStream(Stream):
    """ExactOnline stream class."""

    @property
    @cached
    def conn(self):
        secret = get_secret(self.config.get('secret_id'))
        storage = ExactOnlineStorage(
            base_url=self.config.get('base_url'),
            rest_url=self.config.get('rest_url'),
            auth_url=self.config.get('auth_url'),
            token_url=self.config.get('token_url'),
            client_id=self.config.get('client_id'),
            client_secret=self.config.get('client_secret'),
            access_token=secret['access_token'],
            refresh_token=secret['refresh_token'],
            access_expiry=int(secret['access_expiry']),
            division=self.config.get('division'),
            secret_id=self.config.get('secret_id'),
        )

        return ExactClientSingleton(storage=storage)

    def __init__(self, tap: Tap):
        super().__init__(tap)

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        for key in row.keys():
            row[key] = ODataParser.parse(row[key])
        return row

    def skiptoken(self, context: Optional[dict]):
        token = self.get_starting_replication_key_value(context)
        if len(token) > 0:
            if token.find("-") < 0:
                return "%sL" % token
            else:
                return "guid'%s'" % token
        return ''

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        select = urllib.parse.quote_plus(",".join(self.schema.get('properties').keys()))

        full_path = self.path

        if self.replication_key:
            skiptoken = self.skiptoken(context)

            full_path = full_path + "?$select=" + select + "&$skiptoken=" + skiptoken
        else:
            full_path = full_path + "?$select=" + select

        response = self.conn.restv1(GET(full_path))

        logging.info("api request done. setting %s to inactive" % self.name)
        self.tap_state.update({'stream_running': False})

        for row in response:
            transformed_record = self.post_process(row, context)
            if transformed_record is None:
                continue
            yield transformed_record
