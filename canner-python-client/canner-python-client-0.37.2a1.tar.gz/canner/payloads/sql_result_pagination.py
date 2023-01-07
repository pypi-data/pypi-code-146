from .operation_type import OperationType


class SqlResultPaginationPayload(object):
    def __init__(self) -> None:
        self._name = OperationType.SQL_RESULT_PAGINATION.value
        self._query = """
            query sqlResultPagination($where: SqlResultPaginationWhereInput!) {
                sqlResultPagination(where: $where) {
                    result
                }
            }
        """

    def build(self, sql_query_id: str, limit: int, offset: int) -> dict:
        return {
            "operationName": self._name,
            "query": self._query,
            "variables": {
                "where": {
                    "id": sql_query_id,
                    "limit": limit,
                    "offset": offset,
                    "source": "NOTEBOOK",
                }
            },
        }