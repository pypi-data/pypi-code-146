from typing import Iterable, Union

from assimilator.core.database import LazyCommand, BaseRepository
from fastapi import Request
from dependency_injector.wiring import inject
from starlette.datastructures import URL

from velait.velait_fastapi.api.pagination import Page, PageInfo
from velait.common.pagination import get_page_limits


def get_next_page(url: URL, current_page: int, last_page: int):
    if current_page == last_page:
        return None

    return str(url.include_query_params(page=current_page + 1))


def get_prev_page(url: URL, current_page: int):
    if current_page == 0:
        url.remove_query_params('page')
        return str(url)

    return str(url.include_query_params(page=current_page - 1))


@inject
def paginate(
    request: Request,
    page_size: int,
    data: Union[LazyCommand, Iterable],
    repository: BaseRepository,
) -> Page:
    items = data() if isinstance(data, LazyCommand) else data
    total_count = repository.count()
    last_page = total_count // page_size

    return Page(
        results=items,
        pagination=PageInfo(
            total_records=total_count,
            total_pages=last_page,
            first=str(request.url.remove_query_params('page')),
            last=str(request.url.include_query_params(page=last_page)),
            next=get_next_page(
                request.url,
                last_page=last_page,
                current_page=request.path_params.get('page', 0)
            ),
            previous=get_prev_page(request.url, current_page=request.path_params.get('page', 0)),
        ),
    )


__all__ = [
    'get_next_page',
    'get_prev_page',
    'paginate',
    'get_page_limits',
]
