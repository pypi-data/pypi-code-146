from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gql import gql
from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser

if TYPE_CHECKING:
    from vectice.api.json import PagedResponse

_logger = logging.getLogger(__name__)

# TODO JobRun for lineages
_RETURNS = """
            items {
                    id
                    date
                    targetType
                    targetId
                    targetName
                    __typename
                    }
            total
            page {
                afterCursor
                hasNextPage
                }
            __typename
            """


class LastAssetApi(GqlApi):
    def get_last_assets(self, target_types: list[str], page):
        variable_types = "$targetTypes:[ActivityTargetType!],$page:PageIndexInput"
        kw = "targetTypes:$targetTypes,page:$page"
        variables = {"targetTypes": target_types, "page": page}

        query = GqlApi.build_query(
            gql_query="getLastAssets",
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=True,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            assets_output: PagedResponse = Parser().parse_paged_response(response["getLastAssets"])
            return assets_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "asset", "getLastAssets")
