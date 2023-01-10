from functools import lru_cache

from banal import clean_dict
from fastapi import Path, Query, Request

from ftm_columnstore.dataset import Datasets, get_dataset

from ..settings import EXPOSE_DATASETS
from .params import FtmParams


@lru_cache
def get_datasets(names: str | None = None) -> Datasets:
    if names is None:
        return get_dataset(EXPOSE_DATASETS)
    return get_dataset(names)


PATH_DATASET = Path(
    EXPOSE_DATASETS,
    description="Data source or collection name to be queries",
    example="luanda_leaks",
)
QUERY_PREFIX = Query("", min_length=1, description="Search prefix")


def get_ftm_filters(request: Request) -> dict[str, str]:
    return clean_dict(dict(FtmParams(**request.query_params)))
