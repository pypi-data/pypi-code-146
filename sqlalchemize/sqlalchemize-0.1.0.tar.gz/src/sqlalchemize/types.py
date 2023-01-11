from typing import Any

import sqlalchemy.engine as sa_engine
import sqlalchemy.orm.session as sa_session


Record = dict[str, Any]
SqlConnection = sa_engine.Engine | sa_session.Session | sa_engine.Connection


class MissingPrimaryKey(Exception):
    def __init__(self, message='Table must have primary key. Use alterize.create_primary_key to add a primary key to your table.', errors=None):
        super().__init__(message, errors)

