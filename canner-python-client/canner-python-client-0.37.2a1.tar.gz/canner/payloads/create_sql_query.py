from .operation_type import OperationType


class CreateSqlQueryPayload(object):
    def __init__(self) -> None:
        self._name = OperationType.CREATE_SQL_QUERY.value
        self._query = """
            mutation createSqlQuery($data: SqlQueryCreateInput!, $where: SqlQueryWhereInput!) {
                createSqlQuery(data: $data, where: $where) {
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

    def build(
        self, sql: str, workspace_id: str, cache_refresh: bool, cache_ttl: int
    ) -> dict:
        return {
            "operationName": self._name,
            "query": self._query,
            "variables": {
                "data": {
                    "sql": sql,
                    "cacheRefresh": cache_refresh,
                    "cacheTTL": cache_ttl,
                    "source": "NOTEBOOK",
                },
                "where": {"workspaceId": workspace_id},
            },
        }
