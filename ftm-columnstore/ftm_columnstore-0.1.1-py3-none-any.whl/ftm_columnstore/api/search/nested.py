from typing import Dict, List, Set, Tuple, Union

from followthemoney.property import Property
from followthemoney.types import registry
from yente.data.common import EntityResponse
from yente.data.entity import Entity
from yente.logs import get_logger

from ..routers.util import get_datasets
from .search import result_entities

log = get_logger(__name__)

Value = Union[str, EntityResponse]
Entities = Dict[str, Entity]
Inverted = Dict[str, Set[Tuple[Property, str]]]


def nest_entity(
    entity: Entity, entities: Entities, inverted: Inverted, path: Set[str]
) -> EntityResponse:
    props: Dict[str, List[Value]] = {}
    next_path = set([entity.id]).union(path)

    # Find other entities pointing to the one we're processing:
    for (prop, adj_id) in inverted.get(entity.id, {}):
        if adj_id in path or len(path) > 1:
            continue
        adj = entities.get(adj_id)
        if adj is not None:
            nested = nest_entity(adj, entities, inverted, next_path)
            props.setdefault(prop.name, [])
            props[prop.name].append(nested)

    # Expand nested entities:
    for prop in entity.iterprops():
        if prop.type != registry.entity:
            continue
        values: List[Value] = []
        for value in entity.get(prop):
            if value in path:
                continue
            adj = entities.get(value)
            if adj is not None:
                nested = nest_entity(adj, entities, inverted, next_path)
                values.append(nested)
            else:
                values.append(value)
        props[prop.name] = values
        if not len(values):
            props.pop(prop.name)
    serialized = EntityResponse.from_entity(entity)
    serialized.properties.update(props)
    return serialized


async def serialize_entity(root: Entity, nested: bool = False) -> EntityResponse:
    # FIXME how many levels should be nested
    if not nested:
        return EntityResponse.from_entity(root)
    inverted: Inverted = {}

    entities: Entities = {root.id: root}

    ds = get_datasets()
    resp = ds.expand(root)
    for adj in result_entities(resp):
        entities[adj.id] = adj

        for prop, value in adj.itervalues():
            if prop.type != registry.entity:
                continue

            inverted.setdefault(value, set())
            if prop.reverse is not None:
                inverted[value].add((prop.reverse, adj.id))

    return nest_entity(root, entities, inverted, set())
