from rick.base import Di
from rick.mixin import Injectable
from rick_db import Repository

from pokie.constants import DI_DB


class AutoRestService(Injectable):
    def __init__(self, di: Di):
        super().__init__(di)
        self.repositories = {}

    def get_record(self, class_record, id_record):
        return self.get_repository(class_record).fetch_pk(id_record)

    def delete_record(self, class_record, id_record):
        return self.get_repository(class_record).delete_pk(id_record)

    def insert_record(self, class_record, record):
        return self.get_repository(class_record).insert_pk(record)

    def update_record(self, class_record, record):
        return self.get_repository(class_record).update(record)

    def get_repository(self, class_record) -> Repository:
        if class_record not in self.repositories.keys():
            self.repositories[class_record] = Repository(
                self.get_di().get(DI_DB), class_record
            )
        return self.repositories[class_record]
