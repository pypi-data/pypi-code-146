from rick_db.conn import Connection
from rick_db.repository import BaseRepository
from rick_db.sql import Select


class ValidatorRepository(BaseRepository):
    def __init__(self, db: Connection):
        """
        Constructor
        This class is a stub repository; it doesn't have Record class, table name or schema
        :param db:
        """
        super(ValidatorRepository, self).__init__(db, "")

    def pk_exists(self, pk_value, pk_name, table_name, schema=None) -> bool:
        sql, values = (
            Select(self._dialect)
            .from_(table_name, cols=[pk_name], schema=schema)
            .where(pk_name, "=", pk_value)
            .assemble()
        )

        with self._db.cursor() as c:
            record = c.fetchone(sql, values)
            return record is not None
