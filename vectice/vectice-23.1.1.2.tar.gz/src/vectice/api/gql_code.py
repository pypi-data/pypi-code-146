from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gql import gql
from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser

if TYPE_CHECKING:
    from vectice.api.json.code import CodeInput, CodeOutput


_logger = logging.getLogger(__name__)


_RETURNS = """
            createdDate
            updatedDate
            deletedDate
            version
            id
            name
            description
            uri
            projectId
            authorId
            lastUpdatedById
            __typename
            """


class GqlCodeApi(GqlApi):
    def create_code(self, project_id: int, code: CodeInput) -> CodeOutput:

        variable_types = "$projectId:Float!,$code:CodeCreateInput!"
        kw = "projectId:$projectId,code:$code"
        variables = {"projectId": project_id, "code": code}

        query = GqlApi.build_query(
            gql_query="createCode",
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            dataset_output: CodeOutput = Parser().parse_item(response["createCode"])
            return dataset_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "code", "createCode")

    def get_code(self, code: str | int, project_id: int | None = None) -> CodeOutput:
        """
        parent_id is the project id
        """
        if isinstance(code, int):
            gql_query = "getCode"
            variable_types = "$codeId:Float!"
            variables = {"codeId": code}
            kw = "codeId:$codeId"
        elif isinstance(code, str) and project_id:
            gql_query = "getCodeByName"
            variable_types = "$name:String!,$projectId:Float!"
            variables = {"name": code, "projectId": project_id}  # type: ignore[dict-item]
            kw = "name:$name,projectId:$projectId"
        else:
            raise ValueError("string and parent id required.")
        query = GqlApi.build_query(
            gql_query=gql_query, variable_types=variable_types, returns=_RETURNS, keyword_arguments=kw, query=True
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            phase_output: CodeOutput = Parser().parse_item(response[gql_query])
            return phase_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "getCode", code)
