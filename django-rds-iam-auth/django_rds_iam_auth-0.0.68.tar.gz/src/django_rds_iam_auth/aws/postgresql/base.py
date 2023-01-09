import getpass

import boto3
from django.db.backends.postgresql import base
from django.db.backends.utils import CursorWrapper

from django_rds_iam_auth.utils import resolve_cname


class DatabaseWrapper(base.DatabaseWrapper):

    def get_connection_params(self):
        params = super().get_connection_params()
        enabled = params.pop('use_iam_auth', None)
        if enabled:
            rds_client = boto3.client("rds")

            hostname = params.get('host')
            hostname = resolve_cname(hostname) if hostname else "localhost"

            params["password"] = rds_client.generate_db_auth_token(
                DBHostname=hostname,
                Port=params.get("port", 5432),
                DBUsername=params.get("user") or getpass.getuser(),
            )

        return params

    def make_cursor(self, cursor):
        """Create a cursor without debug logging."""
        return CursorWrapper(cursor, self)

