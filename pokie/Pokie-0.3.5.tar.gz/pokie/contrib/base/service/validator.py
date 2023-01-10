from typing import Any, Optional

from rick.base import Di
from rick.mixin import Injectable

from pokie.contrib.base.repository import ValidatorRepository
from pokie.constants import DI_CONFIG, DI_DB


class ValidatorService(Injectable):
    def __init__(self, di: Di):
        super().__init__(di)
        cfg = di.get(DI_CONFIG)
        self.db = di.get(DI_DB)

        self._cache = None
        if cfg.get("db_cache_metadata", False):
            self._cache = {}

    def id_exists(
        self, pk_name: str, pk_value, table_name: str, schema: str = None
    ) -> bool:
        """
        Check if pk_value exists on the specified table as primary key value

        :param pk_name: primary key name (optional)
        :param pk_value: primary key value
        :param table_name: table name
        :param schema: optional schema name
        :return: True if id is a valid primary key, False if it doesn't
        """
        if not pk_name:
            pk_name = self.get_pk_field(table_name, schema)
        return self.repo_validator.pk_exists(pk_value, pk_name, table_name, schema)

    def get_pk_field(self, table_name: str, schema: str = None) -> Optional[str]:
        """
        Get primary key field name

        :param table_name:
        :param schema:
        :return: str or None
        """
        key = "{}.{}".format(table_name, schema)
        name = self._cache_get(table_name)
        if name is not None:
            return name

        record = self.db.metadata().table_pk(table_name, schema)
        if record is not None:
            self._cache_add(key, record.field)
            return record.field

        return None

    @property
    def repo_validator(self) -> ValidatorRepository:
        return ValidatorRepository(self.db)

    def _cache_add(self, key, value):
        if self._cache is not None:
            self._cache[key] = value

    def _cache_get(self, key, default=None) -> Any:
        if self._cache is not None:
            if key in self._cache.keys():
                return self._cache[key]
        return default
