# pylint: disable=attribute-defined-outside-init
"""
# Unit of Work

Interface to repository.

With help of this module the tool is independent of the database.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from sqlalchemy.orm.session import Session

from src.sqlalchemy_uow.repository import AbstractRepository, SqlAlchemyRepository, FakeRepository


class AbstractUnitOfWork(ABC):
    items: AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self                             # pragma: no cover

    def __exit__(self, *args):
        self.rollback()                         # pragma: no cover

    @abstractmethod
    def commit(self):
        raise NotImplementedError               # pragma: no cover

    @abstractmethod
    def rollback(self):
        raise NotImplementedError               # pragma: no cover


class SqlAlchemyUnitOfWork(AbstractUnitOfWork, ABC):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.items = SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.items = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
