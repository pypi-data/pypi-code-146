from typing import Union

from rick_db import Repository
from rick_db.sql import Sql

from pokie.contrib.auth.dto import UserRecord


class UserRepository(Repository):
    def __init__(self, db):
        super().__init__(db, UserRecord)

    def find_by_username(self, username: str) -> Union[UserRecord, None]:
        key = "__user__:find_by_username"
        sql = self._cache_get(key)
        if not sql:
            sql, _ = self.select().where(UserRecord.username, "=", username).assemble()
            self._cache_set(key, sql)
        with self._db.cursor() as c:
            return c.fetchone(sql, [username], cls=UserRecord)

    def list_users(
        self, offset: int, limit: int, sort_field=None, sort_order=None
    ) -> tuple:
        if not sort_field:
            sort_field = UserRecord.id
        if not sort_order:
            sort_order = Sql.SQL_ASC
        qry = self.select().order(sort_field, sort_order)
        return self.list(qry, limit, offset, UserRecord)
