from contextlib import contextmanager
from datetime import date
from enum import Enum
from functools import wraps
from typing import Union
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from rispack.database import Database
from rispack.logger import logger


def scoped_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = BaseStore().database.session

        try:
            result = func(*args, **kwargs)
            session.commit()

            logger.info("Session committed successfully.")
        except SQLAlchemyError as err:
            logger.error(str(err))

            session.rollback()

            raise err
        finally:
            BaseStore.database.dispose_session()

        return result

    return wrapper


class BaseStore:
    database = None

    def __init__(self):
        if not BaseStore.database:
            BaseStore.database = Database()

    @property
    def session(self):
        return BaseStore.database.session

    def add(self, entity):
        self.session.add(entity)

        self.session.flush()

        return entity

    def add_all(self, entities):
        self.session.add_all(entities)

        self.session.flush()

        return entities

    def get_mapper(self):
        raise NotImplementedError

    def filter_by(self, **kwargs):
        sanitized_args = {}

        for key, val in kwargs.items():
            if type(val) in [UUID, date]:
                val = str(val)

            if isinstance(val, Enum):
                val = val.value

            sanitized_args[key] = val

        return self.session.query(self.get_mapper()).filter_by(**sanitized_args)

    def find(self, id: Union[UUID, int, str]):
        return self.filter_by(id=id).first()

    def find_by(self, **kwargs):
        return self.filter_by(**kwargs).first()

    def where(self, **kwargs):
        return self.filter_by(**kwargs).all()
