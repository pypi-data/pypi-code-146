"""
# Repository

Interface for interactions with database.

Only insert and truncate is needed in this case,
but also add, delete or get can be added to interact with database.
"""
from abc import ABC, abstractmethod
from typing import Optional

from .settings import Settings
from .utils import chunks


class AbstractRepository(ABC):

    @abstractmethod
    def insert(self, dict_list, table):
        raise NotImplementedError   # pragma: no cover

    @abstractmethod
    def truncate(self, table):
        raise NotImplementedError   # pragma: no cover

    @abstractmethod
    def add(self, *args):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get(self, *args):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def list(self, *args) -> list:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def count(self, *args) -> int:
        raise NotImplementedError  # pragma: no cover


class SqlAlchemyRepository(AbstractRepository, ABC):
    """
    Main repository for interacting with DB.
    """
    def __init__(self, session):
        self.session = session

    def insert(self, dict_list: list, table) -> None:
        """
        Insert dict list into DB with bulk insert.
        Much faster for large data set.
        """
        for item in chunks(dict_list, Settings.chunk_size):
            self.session.bulk_insert_mappings(table, item)

    def truncate(self, table) -> None:
        """
        Truncate table before inserting to avoid conflicts with primary key.
        """
        self.session.query(table).delete()

    def add(self, item) -> None:
        """
        Add any row of any table into DB.
        """
        self.session.add(item)

    def get(self, table, by=None) -> tuple:
        """
        Get row from any DB with or without conditions.
        """
        if by is None:
            return self.session.query(table).first()
        return self.session.query(table).filter(table.id == by).first()

    def list(self, table, by: Optional[bool] = None) -> list:
        """
        Get any data as list with or without conditions.
        """
        if by is None:
            return self.session.query(table).yield_per(Settings.chunk_size)

        return self.session.query(table).filter(
            table.exported == by).yield_per(Settings.chunk_size)

    def count(self, table_col, by: bool) -> int:
        """
        Count the table column by filter.
        """
        return self.session.query(table_col).filter(table_col == by).count()


class FakeRepository(AbstractRepository, ABC):
    def __init__(self, items):
        self._items = set(items)

    def insert(self, dict_list, table):
        for item in dict_list:
            self._items.add(item.values)

    def truncate(self, table):
        self._items = ()

    def add(self, item):
        self._items.add(item)

    def get(self, item, filter_=None) -> None:
        return next(b for b in self._items if b == filter_)

    def list(self, batch, by) -> list:
        return list(self._items)

    def count(self, table_col, by):
        return len(table_col)