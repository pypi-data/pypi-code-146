import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from servicefusion.ServicefusionToken import ServicefusionToken
from storages.JSONStorage import JSONStorage

from authlib.integrations.requests_client import OAuth2Session


class Servicefusion(OAuth2Session):
    def __init__(self, app):
        app_base_dir = app.root_path
        self.token_endpoint = "https://api.servicefusion.com/oauth/access_token"
        self.auth_endpoint = "https://api.servicefusion.com/oauth/authorize"

        self.logger = self.setup_logger(app_base_dir)
        self.token_updater = self.save_token
        self.token_handler = JSONStorage(Path(os.path.join(app_base_dir, "tokens/tokens.json")))

        OAuth2Session.__init__(self, client_id=app.config.get('SERVICEFUSION_CLIENT_ID'),
                               client_secret=app.config.get('SERVICEFUSION_CLIENT_SECRET'),
                               token_endpoint_auth_method="client_secret_basic", update_token=self.save_token)
        self.token = self.get_token()

    def save_token(self, token, **kwargs):
        sf_token = ServicefusionToken(**token)
        self.token = token
        self.token_handler.save_token('Servicefusion', sf_token)

    def get_token(self):
        token = self.token_handler.get_token('Servicefusion')
        if not token.exists:
            token = self.fetch_token(self.token_endpoint, grant_type='client_credentials')
            self.save_token(token)
            return token
        elif token.is_expired:
            self.refresh_token(url=self.token_endpoint, refresh_token=token.refresh_token)
        return token

    def get_blueprint(self):
        servicefusion_blueprint = Blueprint('servicefusion_blueprint', __name__, cli_group="servicefusion")

        @servicefusion_blueprint.cli.command()
        def refresh_auth():
            token = self.token_handler.get_token('Servicefusion')
            self.refresh_token(url=self.token_endpoint, refresh_token=token.refresh_token)

        return servicefusion_blueprint

    @staticmethod
    def setup_logger(base_dir):
        log_dir = (os.path.join(base_dir, "logs"))
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file_handler = RotatingFileHandler(log_dir + f'/servicefusion.log', maxBytes=100000, backupCount=5)
        log_file_handler.setFormatter(log_formatter)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception as e:
                print(e)
        logger = logging.getLogger("servicefusion")
        logger.addHandler(log_file_handler)
        logger.setLevel(logging.DEBUG)
        return logger

