from __future__ import annotations

from typing import Any, TYPE_CHECKING, Type, TypeVar, List

from vectice.api.http_error_handlers import ClientErrorHandler
from vectice.api.json import (
    CodeOutput,
    CodeVersionOutput,
    DatasetRegisterOutput,
    IterationOutput,
    ModelRegisterOutput,
    PagedResponse,
    PhaseOutput,
    ProjectOutput,
    StepOutput,
    UserActivity,
    WorkspaceOutput,
    PublicConfigOutput,
)

if TYPE_CHECKING:
    from gql import Client

    from vectice.api._auth import Auth

ResultType = TypeVar("ResultType")


class Parser:
    def map_type(self, type_name: str) -> Type[ResultType]:
        types_map = {
            "Workspace": WorkspaceOutput,
            "Project": ProjectOutput,
            "Phase": PhaseOutput,
            "IterationStep": StepOutput,
            "Iteration": IterationOutput,
            "DatasetRegisterResultOutput": DatasetRegisterOutput,
            "ModelRegisterResultOutput": ModelRegisterOutput,
            "UserActivity": UserActivity,
            "Code": CodeOutput,
            "CodeVersion": CodeVersionOutput,
            "PublicConfigOutput": PublicConfigOutput,
        }
        if type_name in types_map.keys():
            return types_map[type_name]  # type: ignore[return-value]
        else:
            raise RuntimeError("Unknown type: " + type_name)

    def parse_item(self, item: dict[str, Any]) -> ResultType:  # type: ignore[type-var]
        clazz: Type[ResultType] = self.map_type(item["__typename"])
        result = clazz(**item)
        return result

    def parse_list(self, list: list[dict[str, Any]]) -> list[ResultType]:
        # TODO: rename 'list' parameter to avoid shadowing builtin
        result: List[ResultType] = []
        for item in list:
            result.append(self.parse_item(item))
        return result

    def parse_paged_response(self, data: dict[str, Any]) -> PagedResponse[ResultType]:
        return PagedResponse(data["total"], data["page"], self.map_type(data["items"][0]["__typename"]), data["items"])

    def parse(self, data) -> ResultType | list[ResultType] | PagedResponse[ResultType]:
        if type(data) == list:
            return self.parse_list(data)
        else:
            if "items" in data and "page" in data and "total" in data:
                return self.parse_paged_response(data)
            else:
                return self.parse_item(data)


class GqlApi:
    def __init__(self, client: Client, auth: Auth):
        self.client = client
        self.auth = auth
        self._error_handler = ClientErrorHandler()

    def execute(self, query, variables=None):
        # retrieve auth & api http headers
        self.client.transport.headers = self.auth.http_headers
        return self.client.execute(query, variables)

    @staticmethod
    def build_query(gql_query, variable_types, returns, keyword_arguments, query=True):
        query_type = "query" if query else "mutation"
        variable_types_formatted = f"({variable_types})" if variable_types else ""
        keyword_arguments_formatted = f"({keyword_arguments})" if keyword_arguments else ""
        query_built = f"""
        {query_type} {gql_query} {variable_types_formatted} {{
            {gql_query} {keyword_arguments_formatted} {{
                {returns}
            }}
        }}
        """
        return query_built
