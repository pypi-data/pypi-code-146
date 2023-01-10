from typing import Any, Optional, List

from rick.base import Di
from rick.mixin import Injectable

from pokie.constants import DI_DB
from pokie.contrib.base.dto import SettingsRecord
from pokie.contrib.base.repository.settings import SettingsRepository


class SettingsService(Injectable):
    def __init__(self, di: Di):
        super().__init__(di)
        self.db = di.get(DI_DB)

    def list(self) -> List[SettingsRecord]:
        return self.repo_config.fetch_all()

    def by_module(self, module: str) -> List[SettingsRecord]:
        return self.repo_config.fetch_by_module(module)

    def by_key(self, module: str, key: str) -> Optional[SettingsRecord]:
        return self.repo_config.fetch_by_key(module, key)

    def upsert(self, module: str, key: str, value: str):
        return self.repo_config.upsert(module, key, value)

    def delete(self, module, key):
        record = self.repo_config.fetch_by_key(module, key)
        if record is not None:
            self.repo_config.delete_pk(record.id)

    @property
    def repo_config(self) -> SettingsRepository:
        return SettingsRepository(self.db)
