from .operation_type import OperationType


class DeleteFilesPayload(object):
    # Prevent pytest from trying to collect TestConfig as tests:
    __test__ = False

    def __init__(self) -> None:

        self._name = OperationType.DELETE_FILES.value
        self._query = """
            mutation deleteFiles($where: FileWhereInput!) {
                deleteFiles(where: $where) {
                    name
                }
            }
        """

    @property
    def name(self) -> str:
        return self._name

    def build(self, workspace_id: str, filename: str) -> dict:

        return {
            "operationName": self._name,
            "query": self._query,
            "variables": {
                "where": {
                    "workspaceId": workspace_id,
                    "absolutePaths": [filename],
                }
            },
        }
