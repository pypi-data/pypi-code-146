from __future__ import annotations

# NOTE: The functions in this file are not tested in chalkpy
# The integration tests in engine/ validate the behavior of load_dataset
import base64
import json
from concurrent.futures import Future, ThreadPoolExecutor
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Union

from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

from chalk.features.pseudofeatures import CHALK_TS_FEATURE, Feature
from chalk.serialization.codec import FEATURE_CODEC

_DEFAULT_EXECUTOR = ThreadPoolExecutor(16)


class DatasetVersion(IntEnum):
    """Format of the parquet file. Used when loading a dataset so we know what format it is in"""

    # This is the format that bigquery dumps to when specifying an output bucket and output format
    # as part of an (async) query job
    # The output contains extra columns, and all column names are b32 encoded, because
    # bigquery does not support '.' in column names.
    # The client will have to decode column names before loading this data
    # All data, except for feature times, are json encoded
    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES = 1

    # This is the format returned by the dataset writer in engine/
    DATASET_WRITER = 2

    # This format uses separate columns for the observed at and timestamp columns
    # The observed at column is the actual timestamp from when the observation was observed,
    # whereas the timestamp column is the original timestamp that the user requested
    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2 = 3

    COMPUTE_RESOLVER_OUTPUT_V1 = 4


def _parallel_download(uris: List[str], executor: ThreadPoolExecutor) -> pl.DataFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[polars]")

    df_futures: list[Future[pl.DataFrame]] = []
    for uri in uris:
        df_futures.append(executor.submit(pl.read_parquet, uri))

    dfs = [df.result() for df in df_futures]
    dfs = [x.select(sorted(x.columns)) for x in dfs]
    df = pl.concat(dfs)
    return df


def _load_dataset_from_chalk_writer(uris: List[str]) -> pl.DataFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[polars]")
    # V1 datasets should contain just a single URI
    # This URI can be read directly
    # We need to filter the features to remove any pseudofeatures
    if len(uris) != 1:
        raise ValueError("v1 datasets should have just a single URI")
    df = pl.read_parquet(uris[0])
    return df


def _decode_col_name(col_name: str) -> str:
    x_split = col_name.split("_")
    if x_split[0] == "ca":
        assert len(x_split) == 2
        return x_split[1]
    elif x_split[0] == "cb":
        root_fqn_b32 = x_split[1]
        return base64.b32decode(root_fqn_b32.replace("0", "=").upper()).decode("utf8") + "_".join(x_split[2:])
    else:
        raise ValueError(f"Unexpected identifier: {x_split[0]}")


def _decode_column_names(column_names: List[str], ts_fqn: Optional[str]) -> Mapping[str, str]:
    ans: Dict[str, str] = {"__id__": "__id__"}
    found_ts = False
    for x in column_names:
        if x.endswith("__"):
            if x in ("__observed_at__", "__ts__", CHALK_TS_FEATURE.fqn) and ts_fqn is not None and not found_ts:
                ans[x] = ts_fqn
                found_ts = True
            continue
        feature_name = _decode_col_name("_".join(x.split("_")[:2]))
        try:
            _ = Feature.from_root_fqn(feature_name)
            ans[x] = feature_name
        except (ValueError, TypeError, KeyError):
            continue
    return ans


def _decode_column_names_bigquery_v2(column_names: List[str], ts_fqn: Optional[str]) -> Mapping[str, str]:
    ans: Dict[str, str] = {"__id__": "__id__", "__ts__": "__ts__"}
    for x in column_names:
        if x.endswith("__"):
            if x == "__oat__" and ts_fqn is not None:
                ans[x] = ts_fqn
            continue
        feature_name = _decode_col_name("_".join(x.split("_")[:2]))
        try:
            _ = Feature.from_root_fqn(feature_name)
            ans[x] = feature_name
        except (ValueError, TypeError, KeyError):
            continue
    return ans


def _json_decode(x: Optional[str]):
    if x is None:
        return None
    return json.loads(x)


def _json_encode(x: Optional[Any]):
    if x is None:
        return None
    return json.dumps(x)


def _load_dataset_bigquery(
    uris: List[str],
    executor: Optional[ThreadPoolExecutor],
    version: DatasetVersion,
):
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[polars]")
    # V2 datasets are in multiple files, and have column names encoded
    # due to DB limitations (e.g. bigquery does not support '.' in column names)
    # In addition, the datasets may contain extra columns (e.g. replaced observed at)
    # All values are JSON encoded
    if executor is None:
        executor = _DEFAULT_EXECUTOR
    df = _parallel_download(uris, executor)

    ts_fqn = None  # TODO ideally we would like to allow queries and returns of ts features
    if version == DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES:
        decoded_col_names = _decode_column_names(
            df.columns,
            ts_fqn=ts_fqn,
        )
        # Filter out the __observed_at__ and __replaced_observed_at__ columns
        df = df.select(list(decoded_col_names.keys()))

        # Base32-decode the column names
        df = df.rename(dict(decoded_col_names))
    elif version == DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2:
        decoded_col_names = _decode_column_names_bigquery_v2(
            df.columns,
            ts_fqn=ts_fqn,
        )

        # Filter out the __observed_at__ and __replaced_observed_at__ columns
        df = df.select(list(decoded_col_names.keys()))

        # Base32-decode the column names
        df = df.rename(dict(decoded_col_names))

        # Use the __ts__ column if the __oat__ column is null
        if ts_fqn is not None:
            df = df.with_columns(
                pl.when(pl.col(ts_fqn).is_null()).then(pl.col("__ts__")).otherwise(pl.col(ts_fqn)).alias(ts_fqn)
            )
        # Drop the "__ts__ column"
        df = df.drop("__ts__")
    elif version == DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1:
        unique_features = set(df.select(pl.col("feature_name").unique())["feature_name"].to_list())
        cols = [pl.col("value").filter(pl.col("feature_name") == fqn).first().alias(fqn) for fqn in unique_features]

        df = df.groupby("pkey").agg(cols)
        decoded_stmts = []
        for col in df.columns:
            if col == "pkey":
                continue
            if col == ts_fqn:
                decoded_stmts.append(pl.col(col).dt.with_time_zone("UTC"))
            else:
                decoded_stmts.append(
                    pl.col(col).apply(_json_decode, return_dtype=FEATURE_CODEC.get_polars_dtype(fqn=col))
                )
        df = df.select(decoded_stmts)
        return df.select(sorted(df.columns))

    else:
        raise ValueError(f"Unsupported version: {version}")

    # it might be a good idea to remember that we used to rename this __id__ column to the primary key
    # We also need to remove columns like feature.__oat__ and feature.__rat__
    df = df.select([col for col in df.columns if not col.endswith("__")])

    # The parquet file is all JSON-encoded except for the ts column
    decoded_stmts = []
    for col, dtype in df.schema.items():
        if col == ts_fqn or isinstance(dtype, pl.Datetime):
            # Assuming that the only datetime column is for timestamps
            decoded_stmts.append(pl.col(col).dt.with_time_zone("UTC"))
        else:
            decoded_stmts.append(pl.col(col).apply(_json_decode, return_dtype=FEATURE_CODEC.get_polars_dtype(fqn=col)))

    df = df.select(decoded_stmts)
    return df.select(sorted(df.columns))


def load_dataset(
    uris: List[str],
    version: DatasetVersion,
    executor: Optional[ThreadPoolExecutor] = None,
) -> pl.DataFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[polars]")
    if version == DatasetVersion.DATASET_WRITER:
        return _load_dataset_from_chalk_writer(uris)
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
    ):
        return _load_dataset_bigquery(uris, executor, version)
    if version in {DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1}:
        return _load_dataset_bigquery(uris, executor, version)
    raise ValueError(
        f"The dataset version ({version}) is not supported by this installed version of the Chalk client. Please upgrade your chalk client and try again."
    )
