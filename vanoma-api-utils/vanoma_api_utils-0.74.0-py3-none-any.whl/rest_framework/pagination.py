from typing import Any, Dict, List
from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response


def create_page(
    count: int, results: List[Any], page: int = 1, size: int = 10
) -> Dict[str, Any]:
    return {
        "count": count,
        "page": page,
        "size": size,
        "results": results,
    }


class PageNumberPagination(pagination.PageNumberPagination):
    """
    Overriden to allow client to control the page size. Also, instead of returning
    the "next" and "previous" attributes in the paginated response, we replace them
    with "page" and "size". This is part of the effort to avoid leaking our API
    endpoints to users in the browsers.
    """

    page_size = 10
    page_size_query_param = "size"

    def get_paginated_response(self, data: List[Any]) -> Response:
        page_number = self.request.query_params.get(self.page_query_param, 1)  # type: ignore
        page_size = self.request.query_params.get(  # type: ignore
            self.page_size_query_param, self.page_size  # type: ignore
        )

        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),  # type: ignore
                    ("page", page_number),
                    ("size", page_size),
                    ("results", data),
                ]
            )
        )
