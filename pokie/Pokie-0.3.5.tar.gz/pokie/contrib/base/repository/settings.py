from typing import List, Optional

from rick_db import Repository
from pokie.contrib.base.dto import SettingsRecord


class SettingsRepository(Repository):
    def __init__(self, db):
        super().__init__(db, SettingsRecord)

    def fetch_by_module(self, module: str) -> List[SettingsRecord]:
        """
        Fetch config entries by module
        :param module: module name
        :return:
        """
        qry = self._cache_get("fetch_by_module")
        if qry is None:
            qry, values = (
                self.select().where(SettingsRecord.module, "=", module).assemble()
            )
            self._cache_set("fetch_by_module", qry)
        else:
            values = [module]
        with self._db.cursor() as c:
            return c.fetchall(qry, values, self._record)

    def fetch_by_key(self, module: str, key: str) -> Optional[SettingsRecord]:
        """
        Fetch settings by key
        :param module: module name
        :param key: key name
        :return:
        """
        qry = self._cache_get("fetch_by_key")
        if qry is None:
            qry, values = (
                self.select()
                .where(SettingsRecord.module, "=", module)
                .where(SettingsRecord.key, "=", key)
                .assemble()
            )
            self._cache_set("fetch_by_key", qry)
        else:
            values = [module, key]
        with self._db.cursor() as c:
            return c.fetchone(qry, values, self._record)

    def upsert(self, module: str, key: str, value: str):
        """
        Insert or update settings entries
        :param module: module name
        :param key: key name
        :param value: value
        :return: id if new record is created
        """
        record = self.fetch_by_key(module, key)
        if record is not None:
            record.value = value
            return self.update(record)
        return self.insert_pk(SettingsRecord(module=module, key=key, value=value))
