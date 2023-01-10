from typing import Iterable

from fastapi import APIRouter, Query, Response
from ftm_geocode.geocode import Geocoders, geocode_proxy
from pydantic import BaseModel, Field
from yente import settings
from yente.data.common import EntityResponse, ErrorResponse
from yente.data.entity import Entity
from yente.logs import get_logger

from ..search.search import result_entities

log = get_logger(__name__)
router = APIRouter()


class EntitiesResponse(BaseModel):
    result: list[EntityResponse]

    @classmethod
    def from_entities(cls, entities: Iterable[Entity]) -> "EntitiesResponse":
        return cls(result=[EntityResponse.from_entity(e) for e in entities])


class EntityData(BaseModel):
    id: str
    schema_: str = Field(..., example=settings.BASE_SCHEMA, alias="schema")
    properties: dict[str, str | list[str]] = Field(
        ..., example={"address": ["Cowley Road, Cambridge, CB4 0WS, United Kingdom "]}
    )


class EntityQuery(BaseModel):
    entity: EntityData


@router.post(
    "/geocode",
    summary="Geocode an entity",
    tags=["Geocoding"],
    response_model=EntitiesResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def geocode(
    response: Response,
    entity: EntityQuery,
    geocoder: Geocoders = Query(Geocoders.nominatim),
    rewrite_ids: bool = Query(True, description="Rewrite address entity ids"),
    cache: bool = Query(True, description="Use geocoding cache"),
) -> EntitiesResponse:
    """
    Send an entity proxy dict and get geocoded `Address` entities back, if
    geocoding was successfull.

    Uses nominatim per default

    This looks for the [address prop](https://followthemoney.readthedocs.io/en/latest/types.html#type-address)
    on input entities and creates address entities with reference to the input
    entities. The output contains all entities from the input stream plus newly
    created addresses.

    If an input entity is itself an [Address entity](https://followthemoney.readthedocs.io/en/latest/model.html#address),
    it will be geocoded as well and their props (country, city, ...) will be merged
    with the geocoder result.

    During the process, addresses are parsed and normalized as well.
    """
    data = entity.entity.dict()
    data["schema"] = entity.entity.schema_
    results = list(
        result_entities(
            geocode_proxy([geocoder], data, rewrite_ids=rewrite_ids, use_cache=cache)
        )
    )
    success = len(results) > 1
    log.info("/geocode/", action="geocode", success=success)
    response.headers.update(settings.CACHE_HEADERS)
    return EntitiesResponse.from_entities(results)
