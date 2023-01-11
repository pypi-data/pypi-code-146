from datetime import datetime
from typing import Dict
from typing import Optional
from typing import Union

import pandas
import pendulum

from tecton.interactive.data_frame import TectonDataFrame
from tecton.interactive.run_api import resolve_times
from tecton.interactive.run_api import validate_and_get_aggregation_level
from tecton.interactive.run_api import validate_batch_mock_inputs_keys
from tecton.snowflake_context import SnowflakeContext
from tecton_core import conf
from tecton_core import specs
from tecton_core.errors import TectonSnowflakeNotImplementedError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_snowflake import schema_derivation_utils
from tecton_snowflake import sql_helper


def get_historical_features(
    feature_set_config: FeatureSetConfig,
    spine: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, TectonDataFrame, str]] = None,
    timestamp_key: Optional[str] = None,
    include_feature_view_timestamp_columns: bool = False,
    from_source: bool = False,
    save: bool = False,
    save_as: Optional[str] = None,
    start_time: datetime = None,
    end_time: datetime = None,
    entities: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, TectonDataFrame]] = None,
    append_prefix: bool = True,  # Whether to append the prefix to the feature column name
) -> TectonDataFrame:
    # TODO(TEC-6991): Dataset doesn't really work with snowflake as it has spark dependency.
    # Need to rewrite it with snowflake context or remove this param for snowflake.
    if save or save_as is not None:
        raise TectonSnowflakeNotImplementedError("save is not supported for Snowflake")

    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        if entities is not None:
            # Convert entities to a snowflake dataframe
            if isinstance(entities, pandas.DataFrame):
                entities = TectonDataFrame._create(entities).to_snowflake()
            elif isinstance(entities, TectonDataFrame):
                entities = entities.to_snowflake()

        return TectonDataFrame._create_with_snowflake(
            sql_helper.get_historical_features_with_snowpark(
                spine=spine,
                session=SnowflakeContext.get_instance().get_session(),
                timestamp_key=timestamp_key,
                feature_set_config=feature_set_config,
                include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                append_prefix=append_prefix,
                from_source=from_source,
            )
        )
    else:
        if timestamp_key is None and spine is not None:
            raise TectonSnowflakeNotImplementedError("timestamp_key must be specified using Snowflake without Snowpark")
        if entities is not None:
            raise TectonSnowflakeNotImplementedError("entities is only supported for Snowflake with Snowpark enabled")
        return TectonDataFrame._create(
            sql_helper.get_historical_features(
                spine=spine,
                connection=SnowflakeContext.get_instance().get_connection(),
                timestamp_key=timestamp_key,
                feature_set_config=feature_set_config,
                include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
                start_time=start_time,
                end_time=end_time,
                append_prefix=append_prefix,
                from_source=from_source,
            )
        )


def run_batch(
    fd: FeatureDefinition,
    mock_inputs: Dict[str, pandas.DataFrame],
    feature_start_time: Optional[datetime],
    feature_end_time: Optional[datetime],
    aggregate_tiles: bool = None,
    aggregation_level: str = None,
) -> TectonDataFrame:
    fv_proto = fd.feature_view_proto
    validate_batch_mock_inputs_keys(mock_inputs, fd)
    mock_sql_inputs = None

    feature_start_time = get_timezone_aware_datetime(feature_start_time)
    feature_end_time = get_timezone_aware_datetime(feature_end_time)

    aggregation_level = validate_and_get_aggregation_level(fd, aggregate_tiles, aggregation_level)

    if fd.is_temporal_aggregate:
        for feature in fd.fv_spec.aggregate_features:
            aggregate_function = sql_helper.AGGREGATION_PLANS[feature.function]
            if not aggregate_function:
                raise TectonSnowflakeNotImplementedError(
                    f"Unsupported aggregation function {feature.function} in snowflake pipeline"
                )

    session = None
    connection = None
    if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        session = SnowflakeContext.get_instance().get_session()
    else:
        connection = SnowflakeContext.get_instance().get_connection()

    if mock_inputs:
        mock_sql_inputs = {
            key: sql_helper.generate_sql_table_from_pandas_df(
                df=df, session=session, connection=connection, table_name=f"_TT_TEMP_INPUT_{key.upper()}_TABLE"
            )
            for (key, df) in mock_inputs.items()
        }

    # Validate input start and end times. Set defaults if None.
    feature_start_time, feature_end_time, _ = resolve_times(
        fd, feature_start_time, feature_end_time, aggregation_level, FrameworkVersion.FWV5
    )
    sql_str = sql_helper.generate_run_batch_sql(
        feature_definition=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        aggregation_level=aggregation_level,
        mock_sql_inputs=mock_sql_inputs,
        materialization_context=BoundMaterializationContext._create_internal(
            pendulum.instance(feature_start_time),
            pendulum.instance(feature_end_time),
            fd.fv_spec.batch_schedule,
        ),
        session=session,
        from_source=True,  # For run() we don't use materialized data
    )
    if session is not None:
        return TectonDataFrame._create_with_snowflake(session.sql(sql_str))
    else:
        cur = connection.cursor()
        cur.execute(sql_str, _statement_params={"SF_PARTNER": "tecton-ai"})
        return TectonDataFrame._create(cur.fetch_pandas_all())


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: datetime = None,
    end_time: datetime = None,
) -> TectonDataFrame:
    if not conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        raise TectonSnowflakeNotImplementedError("get_dataframe is only supported with Snowpark enabled")

    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    session = SnowflakeContext.get_instance().get_session()
    return TectonDataFrame._create_with_snowflake(
        sql_helper.get_dataframe_for_data_source(session, data_source.batch_source, start_time, end_time)
    )


# For notebook driven development
def derive_batch_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
) -> spark_schema_pb2.SparkSchema:
    if not ds_args.HasField("snowflake_ds_config"):
        raise ValueError(f"Invalid batch source args: {ds_args}")

    connection = SnowflakeContext.get_instance().get_connection()
    return schema_derivation_utils.get_snowflake_schema(ds_args, connection)
