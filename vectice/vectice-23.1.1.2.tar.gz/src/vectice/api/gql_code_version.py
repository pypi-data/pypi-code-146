from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gql import gql
from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser

if TYPE_CHECKING:
    from vectice.api.json.code_version import CodeVersionCreateBody, CodeVersionOutput


_logger = logging.getLogger(__name__)


_RETURNS = """
            createdDate
            updatedDate
            deletedDate
            version
            id
            versionNumber
            name
            description
            uri
            authorId
            codeId
            gitVersionId
            gitVersion {
                        createdDate
                        updatedDate
                        deletedDate
                        version
                        id
                        repositoryName
                        branchName
                        commitHash
                        commitComment
                        commitAuthorEmail
                        commitAuthorName
                        isDirty
                        uri
                        entrypoint
                        authorId
                        workspaceId
                        }
            isStarred
            __typename
            """


class GqlCodeVersionApi(GqlApi):
    def create_code_version(self, code_id: int, code_version: CodeVersionCreateBody):

        variable_types = "$codeId:Float!,$codeVersion:CodeVersionCreationBody!"
        kw = "codeId:$codeId,codeVersion:$codeVersion"
        variables = {"codeId": code_id, "codeVersion": code_version}
        query = GqlApi.build_query(
            gql_query="createCodeVersion",
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            dataset_output: CodeVersionOutput = Parser().parse_item(response["createCodeVersion"])
            return dataset_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "code version", "createCodeVersion")

    def get_code_version(self, code_version: str | int, code_id: int | None = None) -> CodeVersionOutput:
        """
        parent_id is the project id
        """
        if isinstance(code_version, int):
            gql_query = "getCodeVersion"
            variable_types = "$codeId:Float!"
            variables = {"codeVersionId": code_version}
            kw = "codeVersionId:$codeVersionId"
        elif isinstance(code_version, str) and code_id:
            gql_query = "getCodeVersionByName"
            variable_types = "$name:String!,$codeId:Float!"
            variables = {"name": code_version, "codeId": code_id}  # type: ignore[dict-item]
            kw = "name:$name,codeId:$codeId"
        else:
            raise ValueError("string and parent id required.")
        query = GqlApi.build_query(
            gql_query=gql_query, variable_types=variable_types, returns=_RETURNS, keyword_arguments=kw, query=True
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            phase_output: CodeVersionOutput = Parser().parse_item(response[gql_query])
            return phase_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "getCodeVersion", code_version)
