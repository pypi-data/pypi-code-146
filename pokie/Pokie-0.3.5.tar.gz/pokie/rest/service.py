from rick.base import Di

from pokie.constants import DI_DB
from rick.mixin import Injectable
from rick_db import DbGrid, Repository
from .mixin import RestServiceMixin


class RestService(Injectable, RestServiceMixin):
    record_class = None  # record class
    repository_class = None  # optional custom repository class

    def __init__(self, di: Di):
        super().__init__(di)
        # copy class-attributes to instance-attributes
        # this allows usage of multiple instances of RestService with different record and repository classes
        self._record_cls = self.record_class
        self._repository_cls = self.repository_class

    def set_record_class(self, cls):
        self._record_cls = cls

    def set_repository_class(self, cls):
        self._repository_cls = cls

    def get(self, id_record):
        return self.repository.fetch_pk(id_record)

    def delete(self, id_record):
        return self.repository.delete_pk(id_record)

    def insert(self, record):
        return self.repository.insert_pk(record)

    def update(self, id_record, record):
        return self.repository.update(record, id_record)

    def exists(self, id_record):
        return self.repository.valid_pk(id_record)

    def list(
            self,
            search_fields: list,
            search_text: str = None,
            match_fields: dict = None,
            limit: int = None,
            offset: int = None,
            sort_fields: dict = None,
            search_filter: list = None
    ):
        grid = DbGrid(self.repository, search_fields, DbGrid.SEARCH_ANY)
        return grid.run(
            None,
            search_text=search_text,
            match_fields=match_fields,
            limit=limit,
            offset=offset,
            sort_fields=sort_fields,
            search_fields=search_filter
        )

    @property
    def repository(self) -> Repository:
        if self._record_cls is None:
            raise RuntimeError("Missing record class for repository")
        if self._repository_cls is None:
            return Repository(self.get_di().get(DI_DB), self._record_cls)
        else:
            return self._repository_cls(self.get_di().get(DI_DB))
