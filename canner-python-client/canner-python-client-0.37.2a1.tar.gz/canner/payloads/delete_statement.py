from .operation_type import OperationType


class DeleteStatementPayload(object):
    def __init__(self) -> None:
        self._name = OperationType.DELETE_STATEMENT.value
        self._query = """
            mutation deleteStatement($where: StatementWhereUniqueInput!) {
                deleteStatement(where: $where) {
                    id
                }
            }
        """

    def build(self, statement_id: str) -> dict:
        return {
            "operationName": self._name,
            "query": self._query,
            "variables": {"where": {"id": statement_id}},
        }
