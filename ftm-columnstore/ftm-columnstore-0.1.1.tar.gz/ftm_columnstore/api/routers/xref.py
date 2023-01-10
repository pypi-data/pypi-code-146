import csv
from io import StringIO
from typing import Generator

import orjson
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from followthemoney import model
from nomenklatura.entity import CE
from nomenklatura.loader import MemoryLoader
from yente import settings
from yente.data.common import ErrorResponse
from yente.logs import get_logger

from ftm_columnstore import phonetic, xref
from ftm_columnstore.dataset import get_dataset

from .util import PATH_DATASET

log = get_logger(__name__)
router = APIRouter()


def stream_entities(entities: Generator[CE, None, None]) -> Generator[str, None, None]:
    for entity in entities:
        yield orjson.dumps(entity.to_dict()) + b"\n"


def stream_csv(res: Generator[xref.Match, None, None]) -> Generator[str, None, None]:
    yield ",".join(xref.MATCH_COLUMNS) + "\n"
    for row in res:
        io = StringIO()
        w = csv.writer(io)
        w.writerow(row.values())
        yield io.getvalue()


def stream_nk(
    result: Generator[MemoryLoader, None, None]
) -> Generator[str, None, None]:
    for loader in result:
        resolver = loader.resolver
        for edge in resolver.edges.values():
            yield edge.to_line() + "\n"


@router.get(
    "/xref/{dataset}",
    summary="Cross-referencing",
    tags=["Matching"],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
def xref_dataset(
    request: Request,
    # response: StreamingResponse,
    dataset: str = PATH_DATASET,
    schema: str = Query(settings.BASE_SCHEMA, title="Types of entities"),
    against: str | None = Query(None, title="Other dataset(s) (comma seperated)"),
    threshold: float = Query(0.5, title="score threshold", lt=1, gt=0),
    limit: int = Query(100_000, title="number of results"),
    algorithm: phonetic.TPhoneticAlgorithm = Query(
        "metaphone1", title="Metaphone algorithm to create candidate chunks"
    ),
    output: xref.TOutputFormat = Query("csv", title="Output format"),
) -> StreamingResponse:
    # FIXME consolidate with cli invocation
    """
    Perform xref in 3 possible ways:

    a dataset against itself:
        use `dataset` as dataset path parameter

    a dataset against 1 or more other datasets:
        use `dataset` as dataset path parameter
        and `?against=dataset2,dataset3...`

    datasets against each other:
        use `dataset1,dataset2,...` as dataset path parameter
    """
    if "," in dataset and against is not None:
        raise HTTPException(
            400, detail="Either use multiple datasets or 1 dataset against others"
        )

    if model.get(schema) is None:
        raise HTTPException(400, detail="Invalid schema")

    xkwargs = {
        "auto_threshold": threshold,
        "schema": schema,
        "limit": limit,
        "algorithm": algorithm,
        "scored": True,
    }
    format_kwargs = {
        "auto_threshold": threshold,
        "left_dataset": None,
        "min_datasets": 1,
    }

    datasets = [get_dataset(d) for d in dataset.split(",")]
    if len(datasets) == 1:
        dataset = datasets[0]
        # we have a base dataset
        if against is None:
            # perform dataset against itself
            result = xref.xref_dataset(dataset, **xkwargs)
        else:
            # perform dataset against others
            datasets.extend([get_dataset(d) for d in against.split(",")])
            format_kwargs["left_dataset"] = str(dataset)
            format_kwargs["min_datasets"] = 2
            result = xref.xref_datasets(datasets, dataset, **xkwargs)
    else:
        if not len(datasets) > 1:
            raise HTTPException(
                400,
                detail="Specify at least 2 or more comma separated datasets via `against` query",
            )
        # perform full xref between datasets
        format_kwargs["min_datasets"] = 2
        result = xref.xref_datasets(datasets, **xkwargs)

    log.info(f"/xref/{dataset}", action="xref", schema=schema, against=against)

    # FIXME StrEnum py 3.11
    if output == "entities":
        return StreamingResponse(
            stream_entities(
                xref.get_candidates(result, as_entities=True, **format_kwargs)
            )
        )

    if output == "csv":
        return StreamingResponse(
            stream_csv(xref.get_candidates(result, **format_kwargs))
        )

    if output == "nk":
        return StreamingResponse(stream_nk(result))
