"""Helper functions."""
# Standard Modules
import dataclasses
from functools import reduce
from operator import getitem
from typing import List

# Local Modules
from cofactr.kb.entity.types import Mainsnak


def get_path(data, keys, default=None):
    """Access a nested dictionary."""
    try:
        return reduce(getitem, keys, data)
    except (KeyError, IndexError):
        return default


def find_preferred(data: List[Mainsnak], default=None):
    """Find preferred value."""
    return next(
        (x for x in data if x.get("rank") == "preferred"), data[0] if data else default
    )


def drop_deprecated(data: List[Mainsnak]):
    """Drop deprecated values."""
    return filter(lambda x: x.get("rank") == "deprecated", data)


identity = lambda x: x


def parse_entities(ids, entities, entity_dataclass):
    """Parse entities.

    Returns:
        Dictionary mapping ID to entity object.
    """

    id_to_entity = {e.id: e for e in entities}

    if "deprecated_ids" in {
        field.name for field in dataclasses.fields(entity_dataclass)
    }:
        for entity in entities:
            deprecated_ids = entity.deprecated_ids

            for deprecated_id in deprecated_ids:
                id_to_entity[deprecated_id] = entity

    return {id_: id_to_entity[id_] for id_ in ids if id_ in id_to_entity}
