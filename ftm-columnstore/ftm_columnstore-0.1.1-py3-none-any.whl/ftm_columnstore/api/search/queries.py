from typing import Any, Dict, Generator, List, Optional, Tuple, Union

from followthemoney.schema import Schema
from followthemoney.types.name import NameType
from yente.logs import get_logger

from ftm_columnstore.dataset import Datasets
from ftm_columnstore.query import EntityQuery
from ftm_columnstore.util import expand_schema

from ..routers.util import get_datasets

log = get_logger(__name__)

FilterDict = Dict[str, Union[bool, str, List[str]]]
Clause = Dict[str, Any]

NAMES_FIELD = NameType.group or "names"

ACTUAL_FIELDS = {"countries": "country", "datasets": "dataset"}


def filter_query(
    ds: Datasets | None = None,
    schema: Schema | None = None,
    filters: FilterDict = {},
) -> EntityQuery:
    filterqs: Clause = {}
    if ds is None:
        ds = get_datasets()
    if schema is not None:
        schemata = [s.name for s in expand_schema(schema)]
        filterqs["schema__in"] = schemata
    for field, values in filters.items():
        field = ACTUAL_FIELDS.get(field, field)
        if isinstance(values, (bool, str)):
            filterqs[field] = values
            continue
        values = [v for v in values if len(v)]
        if len(values):
            filterqs[f"{field}__in"] = values

    return ds.EQ.where(**filterqs)


def entities_query(
    ds: Datasets,
    schema: Schema,
    filters: FilterDict = {},
) -> EntityQuery:
    return filter_query(ds=ds, schema=schema, filters=filters)


def iter_sorts(sorts: List[str]) -> Generator[Tuple[str, str], None, None]:
    for sort in sorts:
        order = "asc"
        if ":" in sort:
            sort, order = sort.rsplit(":", 1)
        if order not in ["asc", "desc"]:
            order = "asc"
        yield sort, order


def parse_sorts(sorts: List[str], default: Optional[str] = None) -> List[Any]:
    """Accept sorts of the form: <field>:<order>, e.g. first_seen:desc."""
    objs: List[Tuple[str, bool]] = []
    for sort, order in iter_sorts(sorts):
        objs.append((sort, order == "asc"))
    if default is not None:
        objs.append((default, True))
    return objs
