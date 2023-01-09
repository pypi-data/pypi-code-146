import logging
import os
import time
from datetime import datetime
from json import dump, load
from logging.handlers import RotatingFileHandler
from os import environ
from os.path import join
from xmlrpc.client import ServerProxy, Error
from dateutil import parser
from keapcache import KeapCache
from authlib.integrations.requests_client import OAuth2Session
from flask import Blueprint, request, redirect, url_for


class KeapSession(OAuth2Session, KeapCache):

    def __init__(self, app, auth_class=None, logger=None, cache=None):
        APP_BASE_DIR = app.root_path
        if auth_class is None:
            # self.auth_handler = JsonAuthHandler((join(str(Path(__file__).parent.parent.parent.resolve()), "keys/keap_token.json")))
            if 'KEYS_DIR' not in app.config.keys():
                keys_dir = app.root_path
            else:
                keys_dir = app.config.get('KEYS_DIR')
            self.auth_handler = JsonAuthHandler(join(keys_dir, 'keap_token.json'))
        else:
            self.auth_handler = auth_class()

        if logger is None:
            self.logger = self.setup_logger(APP_BASE_DIR)
        else:
            self.logger = logger

        self.token_endpoint = "https://api.infusionsoft.com/token"
        self.auth_endpoint = 'https://signin.infusionsoft.com/app/oauth/authorize'
        self.api_base_url = 'https://api.infusionsoft.com/crm/rest/v1/'
        OAuth2Session.__init__(self, token=self.auth_handler.get_token(), client_id=app.config.get('KEAP_CLIENT_ID'),
                               client_secret=app.config.get('KEAP_CLIENT_SECRET'),
                               update_token=self.auth_handler.store_token,
                               redirect_uri=f"{app.config.get('AUTH_APP_BASE_URL')}authorize-keap",
                               token_endpoint=self.token_endpoint)
        cache_dir = (os.path.join(APP_BASE_DIR, "cache"))
        cache_file = (os.path.join(cache_dir, "cache"))
        KeapCache.__init__(self, cache_file=cache_file)
        self.contact_custom_fields = None
        self.tags = None
        self.name = "Keap-"
        app.register_blueprint(self.get_blueprint())

    def refresh_session_auth(self):
        try:
            self.refresh_token(url=self.token_endpoint)
            self.logger.info("Token Refreshed.")
            return True
        except Exception as e:
            self.logger.warning("Token Refresh Failed.")
            self.logger.exception(e)
            return False

    def update_authorization(self, authorization_data, **kwargs):
        self.auth_handler.update_authorization(authorization_data)

    def is_auth_expired(self):
        return self.token.is_expired()

    def has_token(self):
        if self.token is None:
            return False
        else:
            return True

    def is_authorized(self):
        if not self.has_token():
            return False
        if self.is_auth_expired():
            return self.refresh_session_auth()
        else:
            return True

    def validate_auth(self):
        return self.is_authorized()

    def get_xmlrpc_client(self):
        if not self.is_authorized():
            return None
        else:
            return InfusionsoftOAuth(self.token.get("access_token"))

    def get_authorization_url(self):
        return self.create_authorization_url(self.auth_endpoint)

    def handle_callback(self, callback_request, code):
        token = self.fetch_token(url=self.token_endpoint, authorization_response=callback_request.url, scope='full',
                                 client_id=self.client_id,
                                 redirect_uri=self.redirect_uri,
                                 client_secret=self.client_secret, code=code,
                                 grant_type='authorization_code')
        self.auth_handler.store_token(token)

    def get_blueprint(self):
        keap_blueprint = Blueprint('keap_blueprint', __name__, cli_group="keap")

        @keap_blueprint.route('/authorize-keap')
        def authorize_keap():
            code = request.args.get('code', None)
            if not code:
                uri, state = self.get_authorization_url()
                return redirect(uri, code=302)
            else:
                self.handle_callback(request, code=code)
                self.set_tags()
                self.get_contact_custom_fields()
                return redirect(url_for('index'))

        @keap_blueprint.cli.command()
        def refresh_auth():
            self.refresh_session_auth()

        return keap_blueprint

    @staticmethod
    def get_field_map():
        return CustomFieldMap.keap

    def set_tags(self):
        tags = {}
        tag_names = environ.get('KEAP_TAGS').split(',')
        for tag_name in tag_names:
            tag_id = self.get_tag_id(tag_name)
            if tag_id is not None:
                tags[tag_name] = tag_id
            else:
                continue
        self.update_cache('tags', tags)

    def get_tag_id(self, tag_name):
        params = {"name": tag_name}
        response = self.session.get(f'{self.api_base_url}tags', params=params)
        if response.json().get('count') > 0:
            return response.json().get('tags')[0].get('id')
        else:
            return None

    def get_contact_custom_fields(self):
        if self.contact_custom_fields is None:
            response = self.session.get(f'{self.api_base_url}contactCustomFields')
            if response.status_code == 200:
                custom_fields = response.json()
                keap_custom_fields = KeapCustomFields()
                for field in custom_fields:
                    keap_custom_fields[f"_{field.get('field_name')}"] = field.get("id")
                self.contact_custom_fields = keap_custom_fields
                return keap_custom_fields
            else:
                return None
        else:
            return self.contact_custom_fields

    def get_contact_custom_field_id(self, field_key):
        fields = self.get_contact_custom_fields()
        keap_field_name = CustomFieldMap.keap.get(f"{field_key}")
        return fields.get(f"{keap_field_name}")

    @staticmethod
    def setup_logger(base_dir):
        LOG_DIR = (os.path.join(base_dir, "logs"))
        LOG_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file_handler = RotatingFileHandler(LOG_DIR + f'/keap_client.log', maxBytes=100000, backupCount=5)
        log_file_handler.setFormatter(LOG_FORMATTER)
        if not os.path.exists(LOG_DIR):
            try:
                os.makedirs(LOG_DIR)
            except Exception as e:
                print(e)
        logger = logging.getLogger("keap_client")
        logger.addHandler(log_file_handler)
        logger.setLevel(logging.DEBUG)
        return logger




class Infusionsoft(object):
    base_uri = 'https://%s.infusionsoft.com/api/xmlrpc'

    def __init__(self, name, api_key, use_datetime=False):
        uri = self.base_uri % name
        self.client = ServerProxy(uri, use_datetime=use_datetime)
        self.client.error = Error
        self.key = api_key

    def __getattr__(self, service):
        def function(method, *args):
            call = getattr(self.client, service + '.' + method)

            try:
                return call(self.key, *args)
            except self.client.error as v:
                return "ERROR", v

        return function

    def server(self):
        return self.client


class InfusionsoftOAuth(Infusionsoft):
    base_uri = 'https://api.infusionsoft.com/crm/xmlrpc/v1?'

    def __init__(self, access_token, use_datetime=False):
        uri = '%saccess_token=%s' % (self.base_uri, access_token)

        self.client = ServerProxy(uri, use_datetime=use_datetime, allow_none=True)
        self.client.error = Error
        self.key = access_token


class JsonAuthHandler:

    def __init__(self, auth_file_path):
        self.auth_file_path = auth_file_path

    def store_token(self, data, **kwargs):
        data["updated_at"] = time.time()
        if "expires_at" in data:
            date = datetime.fromtimestamp(data.get("expires_at"))
            data["expiration_datetime"] = date.strftime("%m-%d-%Y  %H:%M")
        else:
            data["expiration_datetime"] = 0
        with open(self.auth_file_path, "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False, indent=4)

    def get_token(self):
        try:
            with open(self.auth_file_path, "r", encoding="utf-8") as f:
                data = load(f)
                if data == {}:
                    return None
                return data
        except FileNotFoundError:
            data = {}
            with open(self.auth_file_path, "w", encoding="utf-8") as f:
                dump(data, f, ensure_ascii=False, indent=4)
            return None

    def get_authorization(self):
        return self.get_token()

    def update_authorization(self, authorization_data, **kwargs):
        updated_auth = self.get_token()
        updated_auth["access_token"] = authorization_data["access_token"]
        updated_auth["refresh_token"] = authorization_data["refresh_token"]
        updated_auth["expires_at"] = datetime.timestamp(parser.parse(authorization_data["expires_at"]))
        self.store_token(updated_auth)




class KeapCustomFields(dict):
    pass


class CustomFieldMap:
    keap = {}
    keap_goals = {}
    for key, value in environ.items():
        if "IFS" in key and "FIELD" in key:
            keap[key] = value
        if "KEAP" in key and "FIELD" in key:
            keap[key] = value
        if "KEAP" in key and "GOAL" in key:
            keap_goals[key] = value
    pass
