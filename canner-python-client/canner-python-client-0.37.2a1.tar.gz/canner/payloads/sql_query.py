from .operation_type import OperationType


class SqlQueryPayload(object):
    def __init__(self) -> None:
        self._name = OperationType.SQL_QUERY.value
        self._query = """
            query sqlQuery($where: SqlQueryWhereUniqueInput!) {
                sqlQuery(where: $where) {
                    id
                    status
                    error
                    location
                    statementId
                    rowCount
                    columns
                }
            }
        """

    def build(self, sql_query_id: str) -> dict:
        return {
            "operationName": self._name,
            "query": self._query,
            "variables": {"where": {"id": sql_query_id}},
        }
