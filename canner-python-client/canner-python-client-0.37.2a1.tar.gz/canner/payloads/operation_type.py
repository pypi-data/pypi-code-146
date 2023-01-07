from enum import Enum


class OperationType(Enum):
    CREATE_SQL_QUERY = "createSqlQuery"
    SQL_QUERY = "sqlQuery"
    SQL_RESULT_PAGINATION = "sqlResultPagination"
    DELETE_STATEMENT = "deleteStatement"
    DELETE_FILES = "deleteFiles"
