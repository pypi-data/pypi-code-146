"""
ftm property params like `name__ilike=%foo%` or `date__gte=2020`
"""

from followthemoney import model
from ftm_columnstore.query import Query
from pydantic import BaseModel, create_model


def _get_props() -> set[str]:
    props = set()
    for prop in model.properties:
        props.add(prop.name)
        for lookup in Query.OPERATORS.keys():
            props.add(f"{prop.name}__{lookup}")
    return props


FtmParams = create_model(
    "FtmParams", **{p: (str | None, None) for p in _get_props()}, __base__=BaseModel
)
