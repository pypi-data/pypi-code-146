from datetime import datetime
from typing import Dict
from typing import Optional
from typing import Union

import pandas

from tecton.interactive.data_frame import TectonDataFrame
from tecton.interactive.run_api import resolve_times
from tecton.interactive.run_api import validate_and_get_aggregation_level
from tecton.interactive.run_api import validate_batch_mock_inputs_keys
from tecton_athena import sql_helper
from tecton_athena.athena_session import get_session
from tecton_athena.data_catalog_helper import generate_sql_table_from_pandas_df
from tecton_core.errors import TectonAthenaNotImplementedError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.time_utils import get_timezone_aware_datetime

TEMP_INPUT_PREFIX = "_TT_TEMP_INPUT_"


def get_historical_features(
    feature_set_config: FeatureSetConfig,
    spine: Optional[Union[pandas.DataFrame, str]] = None,
    timestamp_key: Optional[str] = None,
    include_feature_view_timestamp_columns: bool = False,
    from_source: bool = False,
    save: bool = False,
    save_as: Optional[str] = None,
    start_time: datetime = None,
    end_time: datetime = None,
    entities: Optional[Union[pandas.DataFrame]] = None,
) -> TectonDataFrame:
    if from_source:
        raise TectonAthenaNotImplementedError(
            "Retrieving features directly from data sources (i.e. using from_source=True) is not supported with Athena retrieval. Use from_source=False and feature views that have offline materialization enabled."
        )
    if save or save_as is not None:
        raise TectonAthenaNotImplementedError("save is not supported for Athena")
    if timestamp_key is None and spine is not None:
        raise TectonAthenaNotImplementedError("timestamp_key must be specified")
    if entities is not None:
        raise TectonAthenaNotImplementedError("entities is not supported right now")
    if spine is not None and (start_time or end_time):
        raise TectonAthenaNotImplementedError("If a spine is provided, start_time and end_time must not be provided")

    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    return TectonDataFrame._create(
        sql_helper.get_historical_features(
            spine=spine,
            timestamp_key=timestamp_key,
            feature_set_config=feature_set_config,
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
            start_time=start_time,
            end_time=end_time,
        )
    )


def run_batch(
    fd: FeatureDefinition,
    mock_inputs: Optional[Dict[str, pandas.DataFrame]],
    feature_start_time: Optional[datetime],
    feature_end_time: Optional[datetime],
    aggregation_level: Optional[str],
) -> TectonDataFrame:
    if mock_inputs is not None:
        validate_batch_mock_inputs_keys(mock_inputs, fd)

    aggregation_level = validate_and_get_aggregation_level(
        fd, aggregate_tiles=None, aggregation_level=aggregation_level
    )

    if fd.is_temporal_aggregate:
        for agg_feature in fd.feature_view_proto.temporal_aggregate.features:
            if agg_feature.function not in sql_helper.AGGREGATION_PLANS:
                raise TectonAthenaNotImplementedError(
                    f"Unsupported aggregation function {agg_feature.function} in Athena pipeline"
                )

    session = get_session()
    mock_sql_inputs = None
    if mock_inputs is not None:
        mock_sql_inputs = {
            input_name: generate_sql_table_from_pandas_df(df, f"{TEMP_INPUT_PREFIX}{input_name.upper()}_TABLE", session)
            for (input_name, df) in mock_inputs.items()
        }

    # Validate input start and end times. Set defaults if they are None.
    feature_start_time = get_timezone_aware_datetime(feature_start_time)
    feature_end_time = get_timezone_aware_datetime(feature_end_time)
    feature_start_time, feature_end_time, _ = resolve_times(
        fd, feature_start_time, feature_end_time, aggregation_level, FrameworkVersion.FWV5
    )
    sql_str = sql_helper.generate_run_batch_sql(
        feature_definition=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        aggregation_level=aggregation_level,
        mock_sql_inputs=mock_sql_inputs,
    )

    return TectonDataFrame._create(session.read_sql(sql_str))
