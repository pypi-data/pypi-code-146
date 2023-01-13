"""Ingest utility module"""
import logging
import random
import string
from typing import Tuple

import sqlalchemy as sqla

from .. import util

log = logging.getLogger(__name__)


def generate_ingest_label():
    """Generate random ingest operation label"""
    rand = random.SystemRandom()
    chars = string.ascii_uppercase + string.digits
    return "".join(rand.choice(chars) for _ in range(8))


def init_sqla(
    db_url: str = "sqlite:///:memory:",
) -> Tuple[sqla.engine.Engine, sqla.orm.sessionmaker]:
    """Return configured sqla engine and session factory for DB url"""
    engine_kwargs = {"json_serializer": util.json_serializer}
    if db_url.startswith("sqlite://"):
        pool_cls = sqla.pool.StaticPool if ":memory:" in db_url else sqla.pool.NullPool
        engine_kwargs.update(
            {
                "connect_args": {"check_same_thread": False},
                "poolclass": pool_cls,
            }
        )
    else:
        # TODO migrate from deprecated postgres:// scheme to postgresql://
        # TODO enable connection pooling in workers / api
        engine_kwargs.update(
            {
                "connect_args": {"connect_timeout": 10},
                "poolclass": sqla.pool.NullPool,
            }
        )

    engine = sqla.create_engine(db_url, **engine_kwargs)
    sessionmaker = sqla.orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return engine, sessionmaker
