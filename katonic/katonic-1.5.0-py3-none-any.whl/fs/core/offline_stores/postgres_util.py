#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Optional
import psycopg2
from pydantic.types import StrictStr

from katonic.fs.repo_config import KfsConfigBaseModel


class PostgreSQLConfig(KfsConfigBaseModel):
    host: StrictStr
    port: int = 5432
    db_name: StrictStr
    db_schema: Optional[StrictStr] = None
    user: StrictStr
    password: StrictStr


def get_postgres_conn(config: PostgreSQLConfig):
    return psycopg2.connect(
        dbname=config.db_name,
        host=config.host,
        port=int(config.port),
        user=config.user,
        password=config.password,
        options="-c search_path={}".format(config.db_schema or config.user),
    )


