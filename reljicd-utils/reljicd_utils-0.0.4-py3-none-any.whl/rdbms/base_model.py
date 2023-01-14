from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, Generator, List, Optional, Tuple, TypeVar

import numpy
import pandas
from pandas import notnull
from sqlalchemy import BigInteger, Column, TIMESTAMP, func
from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import NoResultFound

from reljicd_utils.logger.logger import get_logger
from reljicd_utils.rdbms.scoped_session import Session
from reljicd_utils.rdbms.transaction import transaction

LOGGER = get_logger(__name__)

T = TypeVar('T', bound='BaseModel')


class Identifiers(object):
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)


class BaseModel(object):
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=func.now(),
                        default=func.now())
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now(),
                        default=func.now())

    def __str__(self):
        attrs_dict = dict(self.__dict__)
        del attrs_dict['_sa_instance_state']
        return str(attrs_dict)

    @classmethod
    def query(cls, *criterion: Any, **kwargs) -> Query:
        return Session.query(cls).filter(*criterion).filter_by(**kwargs)

    @classmethod
    def one(cls, *criterion: Any, **kwargs) -> T:
        return cls.query(*criterion, **kwargs).one()

    @classmethod
    def first(cls, *criterion: Any, **kwargs) -> T:
        return cls.query(*criterion, **kwargs).first()

    @classmethod
    @lru_cache(maxsize=100)
    def cached_id(cls, *criterion: Any, **kwargs) -> int:
        return cls.query(*criterion, **kwargs).one().id

    @classmethod
    def one_or_none(cls, *criterion: Any, **kwargs) -> Optional[T]:
        return cls.query(*criterion, **kwargs).one_or_none()

    @classmethod
    def exists_one(cls, *criterion: Any, **kwargs) -> bool:
        try:
            cls.one(*criterion, **kwargs)
            return True
        except NoResultFound:
            return False

    @classmethod
    def all(cls,
            *criterion: Any,
            batch_size: int = 1000,
            id_offset: int = 0,
            limit: int = None,
            print_progress: bool = False,
            order_by_updated_at: bool = False,
            **kwargs) -> Generator[T, None, None]:
        if limit and batch_size > limit:
            batch_size = limit
        if print_progress:
            total = cls.count(*criterion, **kwargs)

        counter = 0
        order_by = ((cls.id, cls.updated_at)
                    if order_by_updated_at else (cls.id,))
        while True:
            if limit and counter >= limit:
                break

            objs = (cls.query(*criterion, **kwargs)
                    .filter(cls.id > id_offset)
                    .order_by(*order_by)
                    .limit(batch_size))

            if objs.count() == 0:
                break
            for obj in objs:
                yield obj
                id_offset = obj.id
                counter += 1
                if limit and counter >= limit:
                    break

            if print_progress:
                LOGGER.info(f'Working on {cls.__name__} {counter}/{total}')

    @classmethod
    def all_between_ids(cls,
                        id_lower: int,
                        id_upper: int) -> Generator[T, None, None]:
        count = cls.count(cls.id > id_lower, cls.id < id_upper + 1)
        if not count:
            return
        for obj in cls.all(id_offset=id_lower,
                           limit=count):
            yield obj

    @classmethod
    def delete(cls, *criterion: Any, **kwargs) -> None:
        cls.query(*criterion, **kwargs).delete()

    @classmethod
    @transaction
    def insert_from_csv(cls, csv: str,
                        na_values: List[str] = None,
                        keep_default_na=True) -> None:
        df = pandas.read_csv(csv,
                             na_values=na_values,
                             keep_default_na=keep_default_na)
        df = df.where((notnull(df)),
                      None)  # Fix for converting NaN in dataframe to None

        for original_record in df.to_dict('records'):
            record = {}
            for key, value in original_record.items():
                # Fix for psycopg
                if isinstance(value, numpy.int64):
                    value = int(value)

                # Fix for psycopg (ms-academic)
                if "date" in key and value:
                    try:
                        value = datetime.strptime(value, '%d/%m/%Y')
                    except ValueError:
                        pass

                record[key] = value

            # noinspection PyArgumentList
            obj = cls(**record)
            Session.add(obj)

    @classmethod
    def get_or_create(cls, identifiers: Identifiers, **kwargs) -> T:
        try:
            return cls.one(**identifiers.__dict__)
        except NoResultFound:
            return cls.create(**identifiers.__dict__, **kwargs)

    @classmethod
    def create(cls, **kwargs) -> T:
        # noinspection PyArgumentList
        obj = cls(**kwargs)
        Session.add(obj)
        return obj

    @classmethod
    def count(cls, *criterion, **kwargs) -> int:
        if hasattr(cls, 'id') and cls.id is not None:
            return (Session.query(func.count(cls.id))
                    .filter(*criterion)
                    .filter_by(**kwargs)
                    .scalar())
        else:
            return cls.query(*criterion, **kwargs).count()

    @classmethod
    def max(cls, *criterion, column: str, **kwargs) -> int:
        return (Session.query(func.max(getattr(cls, column)))
                .filter(*criterion)
                .filter_by(**kwargs)
                .scalar())

    @classmethod
    def min(cls, *criterion, column: str, **kwargs) -> int:
        return (Session.query(func.min(getattr(cls, column)))
                .filter(*criterion)
                .filter_by(**kwargs)
                .scalar())

    @classmethod
    def id_ranges(cls, batch_size: int) -> List[Tuple[int, int]]:
        id_max = cls.max(column='id')
        id_offset = cls.min(column='id') - 1
        _id_tuples = []
        while id_offset < id_max:
            _id_tuples.append((id_offset, id_offset + batch_size))
            id_offset += batch_size
        return _id_tuples

    @classmethod
    def bulk_insert(cls, mappings: List[Dict],
                    return_defaults: bool = False) -> Optional[T]:
        return Session.bulk_insert_mappings(cls, mappings,
                                            return_defaults=return_defaults)
