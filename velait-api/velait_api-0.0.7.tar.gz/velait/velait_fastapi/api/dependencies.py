from typing import Optional, Any

from fastapi import Query

import settings


def search_params(
    search: Optional[str] = None,
    query: str = None,
    page: Optional[Any] = Query(default={"page": 0, "size": settings.API_PAGE_SIZE}),
    ordering: Optional[str] = None,
):
    return {
        "search": search,
        "query": query,
        "page": page,
        "ordering": ordering,
    }


__all__ = ['search_params']
