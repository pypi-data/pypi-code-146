import os
from airflow.hooks.base import BaseHook
import json
from distutils import util


class Credentials:
    def __init__(self, conn_id):
        connection = BaseHook.get_connection(conn_id)

        self.url = connection.host
        self.access_key = connection.login
        self.secret_key = connection.password
        if connection.extra is not None and len(connection.extra) > 0:
            version_check = json.loads(connection.extra)['ENABLE_VERSION_CHECK']
        else:
            version_check = True
        if isinstance(version_check, str):
            self.do_version_check = bool(util.strtobool(version_check))
        else:
            self.do_version_check = version_check


# setup these 4 env vars in your airflow environment. You can create api keys from torch ui's setting page.
def torch_credentials(conn_id=None):
    if conn_id is None:
        creds = {
            'url': os.getenv('TORCH_CATALOG_URL', 'https://torch.acceldata.local:5443'),
            'access_key': os.getenv('TORCH_ACCESS_KEY', 'OY2VVIN2N6LJ'),
            'secret_key': os.getenv('TORCH_SECRET_KEY', 'da6bDBimQfXSMsyyhlPVJJfk7Zc2gs'),
            'do_version_check': os.getenv('ENABLE_VERSION_CHECK', True)
        }
    else:
        creds = Credentials(conn_id).__dict__
    return creds
