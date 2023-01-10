from typing import Any, Generator, Iterable

from fastapi import HTTPException
from followthemoney import model
from followthemoney.schema import Schema
from followthemoney.types import registry
from nomenklatura.entity import CE
from yente.data.common import SearchFacet, SearchFacetItem, TotalSpec
from yente.data.entity import Entity
from yente.logs import get_logger
from yente.util import EntityRedirect

from ftm_columnstore.dataset import Datasets
from ftm_columnstore.exceptions import ClickhouseError, EntityNotFound
from ftm_columnstore.query import EntityQuery
from ftm_columnstore.search import search_entities as _search_entities

from ..routers.util import get_datasets

log = get_logger(__name__)


def result_entity(entity: CE) -> Entity:
    # FIXME
    return Entity.from_dict(model, entity.to_dict())


def result_total(query: EntityQuery) -> TotalSpec:
    # FIXME
    spec: dict[str, int | str] = {"value": len(query), "relation": "eq"}
    return TotalSpec(value=spec["value"], relation=spec["relation"])


def result_entities(response: Iterable[CE]) -> Generator[Entity, None, None]:
    for entity in response:
        entity = result_entity(entity)
        if entity is not None:
            yield entity


def result_facets(response: Any, datasets: Datasets) -> dict[str, SearchFacet]:
    facets: dict[str, SearchFacet] = {}
    return facets
    aggs: dict[str, dict[str, Any]] = response.get("aggregations", {})
    for field, agg in aggs.items():
        facet = SearchFacet(label=field, values=[])
        buckets: list[dict[str, Any]] = agg.get("buckets", [])
        for bucket in buckets:
            key: str | None = bucket.get("key")
            if key is None:
                continue
            value = SearchFacetItem(name=key, label=key, count=bucket.get("doc_count"))
            if field == "datasets":
                facet.label = "Data sources"
                try:
                    value.label = datasets[key].title
                except KeyError:
                    value.label = key
            if field in registry.groups:
                type_ = registry.groups[field]
                facet.label = type_.plural
                value.label = type_.caption(key) or value.label
            facet.values.append(value)
        facets[field] = facet
    return facets


async def search_entities(
    ds: Datasets,
    query: EntityQuery,
    q: str,
    limit: int = 10,
    offset: int = 0,
    aggregations: dict[str, Any] | None = None,
    sort: list[tuple[str, bool]] = [],
    fuzzy: bool | None = False,
) -> Iterable[CE]:
    for field, ascending in sort:
        query = query.order_by(field, ascending=ascending)
    try:
        return [e for e, _ in _search_entities(q, ds, query, limit, fuzzy)]
    except ClickhouseError as e:
        log.warning(
            f"ClickhouseError: {e.code}: {e.message}",
            driver=query.driver,
            datasets=query.datasets,
            query=str(query),
        )
        raise HTTPException(status_code=500, detail=e.message)


async def get_entity(entity_id: str) -> Entity | None:
    ds = get_datasets()
    try:
        entity = ds.get(entity_id)
        if entity.id != entity_id:
            raise EntityRedirect(entity.id)
        return result_entity(entity)
    except EntityNotFound:
        pass
    except ClickhouseError as e:
        log.warning(
            f"ClickhouseError: {e.code}: {e.message}",
            driver=ds.driver,
            dataset=ds.name,
            query=entity_id,
        )
        raise HTTPException(status_code=500, detail=e.message)
    return None


async def get_matchable_schemata(dataset: Datasets) -> set[Schema]:
    """Get the set of schema used in this dataset that are matchable or
    a parent schema to a matchable schema."""
    query = dataset.Q.select("DISTINCT schema")
    try:
        schemata: set[Schema] = set()
        for schema in query:
            schema = model.get(schema[0])
            if schema is not None and schema.matchable:
                schemata.update(schema.schemata)
        return schemata
    except ClickhouseError as e:
        log.error("Could not get matchable schema", error=str(e))
        log.warning(
            f"ClickhouseError: {e.code}: {e.message}",
            driver=dataset.driver,
            dataset=dataset.name,
            query=str(query),
        )
        return set()
