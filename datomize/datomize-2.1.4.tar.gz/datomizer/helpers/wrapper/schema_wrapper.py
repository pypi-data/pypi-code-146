from datomizer.protos.autodiscoveryservice_pb2 import SchemaDiscoveryDTO, TableDTO, ColumnDTO
from datomizer.utils.exceptions import ColumnNotFound
from datomizer.utils.messages import COLUMN_NOT_EXISTS


class SchemaWrapper(object):
    schema: SchemaDiscoveryDTO

    def __init__(self, schema):
        self.schema = schema

    def tables(self) -> list:
        return self.schema.tables

    def table(self, table_name=None) -> TableDTO:
        tables = self.tables()
        table: TableDTO
        for table in tables:
            if table_name == table.name:
                return table

        return tables[0]

    def columns(self, table_name=None) -> list:
        return self.table(table_name).columns

    def column(self, table_name, column_name) -> ColumnDTO:
        columns = self.columns(table_name)
        column: ColumnDTO
        for column in columns:
            if column_name == column.name:
                return column

        raise ColumnNotFound(COLUMN_NOT_EXISTS)

    def __str__(self):
        return str(self.schema)
