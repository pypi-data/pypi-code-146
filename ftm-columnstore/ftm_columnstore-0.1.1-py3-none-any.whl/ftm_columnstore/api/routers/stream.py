from typing import Generator

import orjson
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from followthemoney import model
from nomenklatura.entity import CE
from yente import settings
from yente.data.common import ErrorResponse
from yente.logs import get_logger

from ftm_columnstore.query import EntityQuery

from ..search.queries import entities_query
from .util import PATH_DATASET, get_dataset, get_ftm_filters

log = get_logger(__name__)
router = APIRouter()


def stream_entities(query: EntityQuery) -> Generator[CE, None, None]:
    for entity in query:
        yield orjson.dumps(entity.to_dict()) + b"\n"


@router.get(
    "/stream/{dataset}",
    summary="Stream entities",
    tags=["Data access"],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def stream(
    request: Request,
    # response: StreamingResponse,
    dataset: str = PATH_DATASET,
    schema: str = Query(settings.BASE_SCHEMA, title="Types of entities"),
) -> StreamingResponse:
    """
    Stream entities based on filter criteria
    """
    ds = get_dataset(dataset)
    schema_obj = model.get(schema)
    if schema_obj is None:
        raise HTTPException(400, detail="Invalid schema")
    filters = get_ftm_filters(request)
    query = entities_query(ds, schema_obj, filters)
    log.info(
        f"/stream/{ds.name}",
        action="stream",
        filters=filters,
        dataset=ds.name,
    )
    return StreamingResponse(stream_entities(query))
