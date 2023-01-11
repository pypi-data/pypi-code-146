import datetime
import enum
import functools
from dataclasses import dataclass
from inspect import signature
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import attr
import pandas
import pendulum
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from typeguard import typechecked

from tecton._internals.errors import FV_INVALID_MOCK_SOURCES
from tecton._internals.fco import Fco
from tecton._internals.feature_definition import FeatureDefinition
from tecton._internals.type_utils import to_spark_schema_wrapper
from tecton.aggregation_functions import AggregationFunction
from tecton.declarative.base import BaseDataSource
from tecton.declarative.base import BaseEntity
from tecton.declarative.base import OutputStream
from tecton.declarative.basic_info import prepare_basic_info
from tecton.declarative.data_source import BatchSource
from tecton.declarative.data_source import PushSource
from tecton.declarative.data_source import RequestSource
from tecton.declarative.data_source import StreamSource
from tecton.declarative.filtered_source import FilteredSource
from tecton.declarative.run import declarative_run
from tecton.declarative.run import get_transformations
from tecton.declarative.transformation import Transformation
from tecton.declarative.transformation import transformation
from tecton.feature_services.feature_service_args import FeaturesConfig
from tecton.features_common.feature_configs import DatabricksClusterConfig
from tecton.features_common.feature_configs import DEFAULT_SPARK_VERSIONS
from tecton.features_common.feature_configs import DeltaConfig
from tecton.features_common.feature_configs import DynamoConfig
from tecton.features_common.feature_configs import EMRClusterConfig
from tecton.features_common.feature_configs import MonitoringConfig
from tecton.features_common.feature_configs import ParquetConfig
from tecton.features_common.feature_configs import RedisConfig
from tecton.types import Field
from tecton_core import logger as logger_lib
from tecton_core import time_utils
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.feature_view_utils import construct_aggregation_output_feature_name
from tecton_core.feature_view_utils import resolve_function_name
from tecton_core.id_helper import IdHelper
from tecton_core.materialization_context import BaseMaterializationContext
from tecton_core.pipeline_common import transformation_type_checker
from tecton_proto.args import feature_service_pb2
from tecton_proto.args import feature_view_pb2
from tecton_proto.args.feature_view_pb2 import BatchTriggerType as BatchTriggerTypeProto
from tecton_proto.args.feature_view_pb2 import EntityKeyOverride
from tecton_proto.args.feature_view_pb2 import FeatureViewArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewType
from tecton_proto.args.feature_view_pb2 import MaterializedFeatureViewArgs
from tecton_proto.args.feature_view_pb2 import StreamProcessingMode as StreamProcessingModeProto
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import FeatureViewNode
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import RequestContext as RequestContextProto
from tecton_proto.args.pipeline_pb2 import RequestDataSourceNode
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_spark.pipeline_helper import run_mock_odfv_pipeline
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper

# This is the mode used when the feature view decorator is used on a pipeline function, i.e. one that only contains
# references to transformations and constants.
PIPELINE_MODE = "pipeline"

# This is used for the low latency streaming feature views.
CONTINUOUS_MODE = "continuous"

# FilteredSource start offsets smaller (more negative) than this offset will be considered UNBOUNDED_PRECEEDING.
MIN_START_OFFSET = datetime.timedelta(days=-365 * 100)  # 100 years

logger = logger_lib.get_logger("DeclarativeFeatureView")


# Create a parallel enum class since Python proto extensions do not use an enum class.
# Keep up-to-date with StreamProcessingMode from tecton_proto/args/feature_view.proto.
class StreamProcessingMode(enum.Enum):
    TIME_INTERVAL = StreamProcessingModeProto.STREAM_PROCESSING_MODE_TIME_INTERVAL
    CONTINUOUS = StreamProcessingModeProto.STREAM_PROCESSING_MODE_CONTINUOUS


# Keep up-to-date with BatchTriggerType from tecton_proto/args/feature_view.proto.
class BatchTriggerType(enum.Enum):
    SCHEDULED = BatchTriggerTypeProto.BATCH_TRIGGER_TYPE_SCHEDULED
    MANUAL = BatchTriggerTypeProto.BATCH_TRIGGER_TYPE_MANUAL


@attr.s(auto_attribs=True)
class Aggregation(object):
    """
    This class describes a single aggregation that is applied in a batch or stream feature view.

    :param column: Column name of the feature we are aggregating.
    :type column: str
    :param function: One of the built-in aggregation functions.
    :type function: Union[str, AggregationFunction]
    :param time_window: Duration to aggregate over. Example: ``datetime.timedelta(days=30)``.
    :type time_window: datetime.timedelta
    :param name: The name of this feature. Defaults to an autogenerated name, e.g. transaction_count_7d_1d.
    :type name: str

    `function` can be one of predefined numeric aggregation functions, namely ``"count"``, ``"sum"``, ``"mean"``, ``"min"``, ``"max"``, ``"var_samp"``, ``"var_pop"``, ``"variance"`` - alias for ``"var_samp"``, ``"stddev_samp"``, ``"stddev_pop"``, ``"stddev"`` - alias for ``"stddev_samp"``. For
    these numeric aggregations, you can pass the name of it as a string. Nulls are handled like Spark SQL `Function(column)`, e.g. SUM/MEAN/MIN/MAX/VAR_SAMP/VAR_POP/VAR/STDDEV_SAMP/STDDEV_POP/STDDEV of all nulls is null and COUNT of all nulls is 0.

    In addition to numeric aggregations, :class:`Aggregation` supports the last non-distinct and distinct N aggregation that will compute the last N non-distinct and distinct values for the column by timestamp. Right now only string column is supported as input to this aggregation, i.e., the resulting feature value will be a list of strings. The order of the value in the list is ascending based on the timestamp. Nulls are not included in the aggregated list.

    You can use it via the ```last()``` and  ``last_distinct()`` helper function like this:

    .. code-block:: python

        from tecton.aggregation_functions import last_distinct, last

        @batch_feature_view(
        ...
        aggregations=[
            Aggregation(
                column='my_column',
                function=last_distinct(15),
                time_window=datetime.timedelta(days=7)),
            Aggregation(
                column='my_column',
                function=last(15),
                time_window=datetime.timedelta(days=7)),
            ],
        ...
        )
        def my_fv(data_source):
            pass

    """

    column: str
    """Column name of the feature we are aggregating."""
    function: Union[str, AggregationFunction]
    """One of the built-in aggregation functions (`'count'`, `'sum'`, `'mean'`, `'min'`, `'max'`, `'var_samp'`, `'var_pop'`, `'variance'`, `'stddev_samp'`, `'stddev_pop'`, `'stddev'`)."""
    time_window: datetime.timedelta
    """Example: ``datetime.timedelta(days=30)``"""
    name: Optional[str] = None
    """Example: ``datetime.timedelta(days=30)``"""

    def _to_proto(self, aggregation_interval: datetime.timedelta, is_continuous: bool):
        proto = feature_view_pb2.FeatureAggregation()
        proto.column = self.column

        if isinstance(self.function, str):
            proto.function = self.function
        elif isinstance(self.function, AggregationFunction):
            proto.function = self.function.name
            for k, v in self.function.params.items():
                assert isinstance(v, int)
                proto.function_params[k].CopyFrom(feature_view_pb2.ParamValue(int64_value=v))
        else:
            raise TypeError(f"Invalid function type: {type(self.function)}")

        proto.time_window.FromTimedelta(self.time_window)

        if self.name:
            proto.name = self.name
        else:
            proto.name = construct_aggregation_output_feature_name(
                proto.column,
                resolve_function_name(proto.function, proto.function_params),
                proto.time_window,
                time_utils.timedelta_to_proto(aggregation_interval),
                is_continuous,
            )
        return proto


def get_source_input_params(user_function) -> List[str]:
    # Filter out the materailization context to avoid mapping data sources to it.
    return [
        param.name
        for param in signature(user_function).parameters.values()
        if not isinstance(param.default, BaseMaterializationContext)
    ]


def prepare_common_fv_args(basic_info, entities, pipeline_root) -> FeatureViewArgs:
    args = FeatureViewArgs()
    args.feature_view_id.CopyFrom(IdHelper.from_string(IdHelper.generate_string_id()))

    args.version = FrameworkVersion.FWV5.value

    args.info.CopyFrom(basic_info)

    args.entities.extend([EntityKeyOverride(entity_id=entity._id, join_keys=entity.join_keys) for entity in entities])
    args.pipeline.root.CopyFrom(pipeline_root)

    return args


def source_to_pipeline_node(
    source: Union[BaseDataSource, FilteredSource, RequestSource, FeatureDefinition, FeaturesConfig], input_name: str
):
    if isinstance(source, FeatureDefinition):
        source = FeaturesConfig(feature_view=source, namespace=source.name)

    pipeline_node = PipelineNode()
    if isinstance(source, BaseDataSource):
        node = DataSourceNode(
            virtual_data_source_id=source._id,
            window_unbounded=True,
            schedule_offset=time_utils.timedelta_to_proto(source.data_delay),
            input_name=input_name,
        )
        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, FilteredSource):
        node = DataSourceNode(
            virtual_data_source_id=source.source._id,
            schedule_offset=time_utils.timedelta_to_proto(source.source.data_delay),
            input_name=input_name,
        )
        if source.start_time_offset <= MIN_START_OFFSET:
            node.window_unbounded_preceding = True
        else:
            node.start_time_offset.FromTimedelta(source.start_time_offset)

        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, PushSource):
        node = DataSourceNode(virtual_data_source_id=source._id, input_name=input_name)
        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, RequestSource):
        request_schema = source.schema
        if isinstance(request_schema, List):
            wrapper = to_spark_schema_wrapper(request_schema)
        else:
            wrapper = SparkSchemaWrapper(request_schema)

        node = RequestDataSourceNode(
            request_context=RequestContextProto(schema=wrapper.to_proto()),
            input_name=input_name,
        )
        pipeline_node.request_data_source_node.CopyFrom(node)
    elif isinstance(source, FeaturesConfig):
        override_join_keys = None
        if source.override_join_keys:
            override_join_keys = [
                feature_service_pb2.ColumnPair(spine_column=k, feature_column=v)
                for k, v in sorted(source.override_join_keys.items())
            ]
        node = FeatureViewNode(
            feature_view_id=source.id,
            input_name=input_name,
            feature_view=feature_service_pb2.FeatureServiceFeaturePackage(
                feature_package_id=source.id,
                override_join_keys=override_join_keys,
                namespace=source.namespace,
                features=source.features,
            ),
        )
        pipeline_node.feature_view_node.CopyFrom(node)
    else:
        raise TypeError(f"Invalid source type: {type(source)}")
    return pipeline_node


def transformation_to_pipeline_node(
    pipeline_function: Callable,
    params_to_sources: Dict[
        str, Union[BaseDataSource, FilteredSource, RequestSource, FeatureDefinition, FeaturesConfig]
    ],
) -> PipelineNode:
    pipeline_kwargs = sources_to_pipeline_nodes(params_to_sources)
    pipeline_fn_result = pipeline_function(**pipeline_kwargs)
    return pipeline_fn_result


def test_binding_user_function(fn, inputs):
    # this function binds the top-level pipeline function only, for transformation binding, see transformation.__call__
    pipeline_signature = signature(fn)
    try:
        pipeline_signature.bind(**inputs)
    except TypeError as e:
        raise TypeError(f"while binding inputs to pipeline function, TypeError: {e}")


def sources_to_pipeline_nodes(
    params_to_sources: Dict[
        str, Union[BaseDataSource, FilteredSource, RequestSource, FeatureDefinition, FeaturesConfig]
    ]
) -> Dict[str, PipelineNode]:
    kwargs = {}
    for param_name, source in params_to_sources.items():
        pipeline_node = source_to_pipeline_node(source=source, input_name=param_name)
        kwargs[param_name] = pipeline_node

    return kwargs


class OnDemandFeatureView(FeatureDefinition):
    """
    OnDemandFeatureView class to include in Feature Services or to use in unit testing.

    **Do not instantiate this class directly.** Use :class:`tecton.declarative.on_demand_feature_view` instead.
    """

    def __init__(
        self,
        *,  # All arguments must be specified with keywords
        schema,
        transform,
        name: str,
        description: Optional[str],
        tags: Optional[Dict[str, str]],
        pipeline_function,
        owner: Optional[str],
        sources: List[Union[RequestSource, FeatureDefinition, FeaturesConfig]],
        user_function,
    ):
        """
        **Do not directly use this constructor.** Internal constructor for OnDemandFeatureView.

        :param schema: Spark schema declaring the expected output.
        :param transform: Transformation used to produce the feature values.
        :param name: Unique, human friendly name.
        :param description: A human readable description.
        :param tags: Arbitrary key-value pairs of tagging metadata.
        :param pipeline_function: Pipeline definition function.
        :param owner: Owner name, used to organize features.
        :param sources: The data source inputs to the feature view.
        :param user_function: User-defined function.

        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)

        self.fn_params = get_source_input_params(user_function)
        params_to_sources = dict(zip(self.fn_params, sources))

        pipeline_root = transformation_to_pipeline_node(
            pipeline_function=pipeline_function, params_to_sources=params_to_sources
        )

        args = prepare_common_fv_args(basic_info=basic_info, entities=[], pipeline_root=pipeline_root)
        args.feature_view_type = FeatureViewType.FEATURE_VIEW_TYPE_ON_DEMAND

        transformation_type_checker(basic_info.name, pipeline_root, "pipeline", ["pipeline", "pandas", "python"])
        # We bind to user_function since pipeline_function may be artificially created and just accept **kwargs
        test_binding_user_function(user_function, params_to_sources)

        if isinstance(schema, list):
            wrapper = to_spark_schema_wrapper(schema)
        else:
            wrapper = SparkSchemaWrapper(schema)
        args.on_demand_args.schema.CopyFrom(wrapper.to_proto())

        self._args = args
        self.inferred_transform = transform
        self.pipeline_function = pipeline_function
        self.schema = schema
        self.sources = sources

        Fco._register(self)

    @typechecked
    def run(self, **mock_sources: Union[Dict[str, Any], pandas.DataFrame]) -> Union[Dict[str, Any], pandas.DataFrame]:
        """
        Run the OnDemandFeatureView using mock sources.

        :param mock_sources: Required. Keyword args with the same expected keys
            as the OnDemandFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        Example:
            .. code-block:: python

                @on_demand_feature_view(
                    sources=[transaction_request],
                    mode='python',
                    schema=output_schema,
                )
                def transaction_amount_is_high(transaction_request):
                    return {'transaction_amount_is_high': transaction_request['amount'] > 10000}

                # Test using `run` API.
                result = transaction_amount_is_high.run(transaction_request={'amount': 100})

        :return: A `Dict` object for the "python" mode and a `pandas.DataFrame` object for the "pandas" mode".
        """
        if set(self.fn_params) != set(mock_sources.keys()):
            raise FV_INVALID_MOCK_SOURCES(mock_sources.keys(), self.fn_params)

        return run_mock_odfv_pipeline(
            self._args.pipeline, get_transformations(self._args), self._args.info.name, mock_sources
        )


@typechecked
def on_demand_feature_view(
    *,
    mode: str,
    sources: List[Union[RequestSource, FeatureDefinition, FeaturesConfig]],
    schema: Union[List[Field]],
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    name: Optional[str] = None,
):
    """
    Declare an On-Demand Feature View

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("python" or "pandas" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: The data source inputs to the feature view. An input can be a RequestSource or a materialized Feature View.
    :param schema: Tecton schema matching the expected output (of either a dictionary or a Pandas DataFrame).
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :return: An object of type :class:`tecton.feature_views.OnDemandFeatureView`.

    An example declaration of an on-demand feature view using Python mode.
    With Python mode, the function sources will be dictionaries, and the function is expected to return a dictionary matching the schema from `output_schema`.
    Tecton recommends using Python mode for improved online serving performance.

    .. code-block:: python

        from tecton import RequestSource, on_demand_feature_view
        from tecton.types import Field, Float64, Int64
        import pandas

        # Define the request schema
        transaction_request = RequestSource(schema=[Field("amount", Float64)])

        # Define the output schema
        output_schema = [Field("transaction_amount_is_high", Int64)]

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='pandas',
            schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
            description='Whether the transaction amount is considered high (over $10000)'
        )

        def transaction_amount_is_high(transaction_request):
            result = {}
            result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
            return result

    An example declaration of an on-demand feature view using Pandas mode.
    With Pandas mode, the function sources will be Pandas Dataframes, and the function is expected to return a Dataframe matching the schema from `output_schema`.

    .. code-block:: python

        from tecton import RequestSource, on_demand_feature_view
        from tecton.types import Field, Float64, Int64
        import pandas

        # Define the request schema
        transaction_request = RequestSource(schema=[Field("amount", Float64)])

        # Define the output schema
        output_schema = [Field("transaction_amount_is_high", Int64)]

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='pandas',
            schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
            description='Whether the transaction amount is considered high (over $10000)'
        )
        def transaction_amount_is_high(transaction_request):
            import pandas as pd

            df = pd.DataFrame()
            df['transaction_amount_is_high'] = (transaction_request['amount'] >= 10000).astype('int64')
            return df
    """

    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            transform = transformation(mode=mode, description=description, owner=owner, tags=tags, name=name)(
                user_function
            )

            def pipeline_function(**kwargs):
                return transform(**kwargs)

        feature_view = OnDemandFeatureView(
            schema=schema,
            transform=transform,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            sources=sources,
            description=description,
            owner=owner,
            tags=tags,
            user_function=user_function,
        )
        functools.update_wrapper(wrapper=feature_view, wrapped=user_function)

        return feature_view

    return decorator


@dataclass
class MaterializedFeatureView(FeatureDefinition):
    """
    Stream/Batch Feature View class to include in Feature Services or to use in unit testing.

    **Do not instantiate this class directly.** Use a decorator-based constructor instead:

    - :class:`tecton.declarative.batch_feature_view`
    - :class:`tecton.declarative.stream_feature_view`

    """

    def __init__(
        self,
        args: FeatureViewArgs,
        inferred_transform: Optional[Transformation],
        pipeline_function: Optional[Callable[..., PipelineNode]],
        sources: Sequence[Union[BaseDataSource, FilteredSource]],
    ):
        """
        **Do not directly use this constructor.** Internal constructor for materialized FeatureViews.
        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()
        self._args = args
        self.inferred_transform = inferred_transform
        self.pipeline_function = pipeline_function
        self.sources = sources

        Fco._register(self)

    def __hash__(self):
        return self.name.__hash__()

    def run(
        self,
        spark: SparkSession,
        start_time: Optional[datetime.datetime],
        end_time: Optional[datetime.datetime],
        aggregation_level: Optional[str] = None,
        **mock_sources: DataFrame,
    ):
        """
        Run the FeatureView using mock data sources. This requires a local spark session.

        :param start_time: The start time of the time window to materialize. If not set, defaults to `end_time` minus `batch_schedule`.

        :param end_time: The end time of the time window to materialize. If not set, defaults to `start_time` plus `batch_schedule`

        :param aggregation_level: For feature views with aggregations, `aggregation_level` configures what stage of the aggregation to run up to.

            The query for Aggregate Feature Views operates in three logical steps:

                1) The feature view query is run over the provided time range. The user defined transformations are applied over the data source.

                2) The result of #1 is aggregated into tiles the size of the aggregation_interval.

                3) The tiles from #2 are combined to form the final feature values. The number of tiles that are combined is based off of the time_window of the aggregation.

            For testing and debugging purposes, to see the output of #1, use ``aggregation_level="disabled"``. For #2, use ``aggregation_level="partial"``. For #3, use ``aggregation_level="full"``.

            ``aggregation_level="full"`` is the default behavior.

        :param \*\*mock_sources: kwargs with expected same keys as the FeatureView's inputs parameter. Each input name
            maps to a Spark DataFrame that should be evaluated for that node in the pipeline.

        Example:

        .. code-block:: python

            from datetime import datetime, timedelta
            import pandas
            from fraud.features.batch_features.user_credit_card_issuer import user_credit_card_issuer


            # The `tecton_pytest_spark_session` is a PyTest fixture that provides a
            # Tecton-defined PySpark session for testing Spark transformations and feature
            # views.
            def test_user_distinct_merchant_transaction_count_30d(tecton_pytest_spark_session):
                input_pandas_df = pandas.DataFrame({
                    "user_id": ["user_1", "user_2", "user_3", "user_4"],
                    "signup_timestamp": [datetime(2022, 5, 1)] * 4,
                    "cc_num": [1000000000000000, 4000000000000000, 5000000000000000, 6000000000000000],
                })
                input_spark_df = tecton_pytest_spark_session.createDataFrame(input_pandas_df)

                # Simulate materializing features for May 1st.
                output = user_credit_card_issuer.run(
                    spark=tecton_pytest_spark_session,
                    start_time=datetime(2022, 5, 1),
                    end_time=datetime(2022, 5, 2),
                    fraud_users_batch=input_spark_df)

                actual = output.toPandas()

                expected = pandas.DataFrame({
                    "user_id": ["user_1", "user_2", "user_3", "user_4"],
                    "signup_timestamp":  [datetime(2022, 5, 1)] * 4,
                    "credit_card_issuer": ["other", "Visa", "MasterCard", "Discover"],
                })

                pandas.testing.assert_frame_equal(actual, expected)


        :return: A :class:`tecton.TectonDataFrame` object.
        """
        return declarative_run(self._args, spark, start_time, end_time, aggregation_level, mock_sources)


@typechecked
def stream_feature_view(
    *,
    mode: str,
    source: Union[StreamSource, FilteredSource],
    entities: List[BaseEntity],
    aggregation_interval: Optional[datetime.timedelta] = None,
    stream_processing_mode: Optional[StreamProcessingMode] = None,
    aggregations: List[Aggregation] = [],
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]] = None,
    batch_trigger: BatchTriggerType = BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[List[str]] = None,
    batch_compute: Optional[Union[DatabricksClusterConfig, EMRClusterConfig]] = None,
    stream_compute: Optional[Union[DatabricksClusterConfig, EMRClusterConfig]] = None,
    offline_store: Optional[Union[ParquetConfig, DeltaConfig]] = ParquetConfig(),
    online_store: Optional[Union[DynamoConfig, RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[OutputStream] = None,
):
    """
    Declare a Stream Feature View.

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("spark_sql" or "pyspark" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param source: The data source input to the feature view.
    :param entities: The entities this feature view is associated with.
    :param aggregation_interval: How frequently the feature value is updated (for example, `"1h"` or `"6h"`)
    :param stream_processing_mode: Whether aggregations should be "batched" in time intervals or be updated continuously.
        Continuously aggregated features are fresher but more expensive. One of `StreamProcessingMode.TIME_INTERVAL` or
        `StreamProcessingMode.CONTINUOUS`. Defaults to `StreamProcessingMode.TIME_INTERVAL`.
    :param aggregations: A list of :class:`Aggregation` structs
    :param online: Whether the feature view should be materialized to the online feature store. (Default: False)
    :param offline: Whether the feature view should be materialized to the offline feature store. (Default: False)
    :param ttl: The TTL (or "look back window") for features defined by this feature view. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
    :param feature_start_time: When materialization for this feature view should start from. (Required if offline=true)
    :param batch_trigger: Defines the mechanism for initiating batch materialization jobs.
        One of `BatchTriggerType.SCHEDULED` or `BatchTriggerType.MANUAL`.
        The default value is `BatchTriggerType.SCHEDULED`, where Tecton will run materialization jobs based on the
        schedule defined by the ``batch_schedule`` parameter. If set to `BatchTriggerType.MANUAL`, then batch
        materialization jobs must be explicitly initiated by the user through either the Tecton SDK or Airflow operator.
    :param batch_schedule: The interval at which batch materialization should be scheduled.
    :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
    :param batch_compute: Batch materialization cluster configuration.
    :param stream_compute: Streaming materialization cluster configuration.
    :param offline_store: Configuration for how data is written to the offline feature store.
    :param online_store: Configuration for how data is written to the online feature store.
    :param monitor_freshness: If true, enables monitoring when feature data is materialized to the online feature store.
    :param expected_feature_freshness: Threshold used to determine if recently materialized feature data is stale. Data is stale if ``now - most_recent_feature_value_timestamp > expected_feature_freshness``. For feature views using Tecton aggregations, data is stale if ``now - round_up_to_aggregation_interval(most_recent_feature_value_timestamp) > expected_feature_freshness``. Where ``round_up_to_aggregation_interval()`` rounds up the feature timestamp to the end of the ``aggregation_interval``. Value must be at least 2 times ``aggregation_interval``. If not specified, a value determined by the Tecton backend is used.
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param timestamp_field: The column name that refers to the timestamp for records that are produced by the
        feature view. This parameter is optional if exactly one column is a Timestamp type.
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param max_batch_aggregation_interval: (Advanced) Configure the time range materialized by each backfill jobs. This can help optimize large backfill jobs.
    :param output_stream: Configuration for a stream to write feature outputs to, specified as a :class:`tecton.declarative.output_stream.KinesisOutputStream` or :class:`tecton.declarative.output_stream.KafkaOutputStream`.
    :return: An object of type :class:`tecton.declarative.feature_view.MaterializedFeatureView`.

    Example `StreamFeatureView` declaration:

    .. code-block:: python

        from datetime import datetime, timedelta
        from entities import user
        from transactions_stream import transactions_stream
        from tecton import Aggregation, FilteredSource, stream_feature_view

        @stream_feature_view(
            source=FilteredSource(transactions_stream),
            entities=[user],
            mode="spark_sql",
            ttl=timedelta(days=30),
            online=True,
            offline=True,
            batch_schedule=timedelta(days=1),
            feature_start_time=datetime(2020, 10, 10),
            tags={"release": "production"},
            owner="kevin@tecton.ai",
            description="Features about the users most recent transaction in the past 60 days. Updated continuously.",
        )
        def user_last_transaction_features(transactions_stream):
            return f'''
                SELECT
                    USER_ID,
                    TIMESTAMP,
                    AMOUNT as LAST_TRANSACTION_AMOUNT,
                    CATEGORY as LAST_TRANSACTION_CATEGORY
                FROM
                    {transactions_stream}
                '''

    Example `StreamFeatureView` declaration using aggregates:

    .. code-block:: python

        from datetime import datetime, timedelta
        from entities import user
        from transactions_stream import transactions_stream
        from tecton import Aggregation, FilteredSource, stream_feature_view

        @stream_feature_view(
            source=FilteredSource(transactions_stream),
            entities=[user],
            mode="spark_sql",
            aggregation_interval=timedelta(minutes=10),
            aggregations=[
                Aggregation(column="AMOUNT", function="mean", time_window=timedelta(hours=1)),
                Aggregation(column="AMOUNT", function="mean", time_window=timedelta(hours=24)),
                Aggregation(column="AMOUNT", function="mean", time_window=timedelta(hours=72)),
                Aggregation(column="AMOUNT", function="sum", time_window=timedelta(hours=1)),
                Aggregation(column="AMOUNT", function="sum", time_window=timedelta(hours=24)),
                Aggregation(column="AMOUNT", function="sum", time_window=timedelta(hours=72)),
            ],
            online=True,
            feature_start_time=datetime(2020, 10, 10),
            tags={"release": "production"},
            owner="kevin@tecton.ai",
            description="Transaction amount statistics and total over a series of time windows, updated every ten minutes.",
        )
        def user_recent_transaction_aggregate_features(transactions_stream):
            return f'''
                SELECT
                    USER_ID,
                    AMOUNT,
                    TIMESTAMP
                FROM
                    {transactions_stream}
                '''
    """

    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            inferred_transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = transformation(mode, name, description, owner, tags=tags)(user_function)

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        if aggregations:
            _stream_processing_mode = stream_processing_mode or StreamProcessingMode.TIME_INTERVAL
        else:
            _stream_processing_mode = stream_processing_mode

        args = build_materialized_feature_view_args(
            feature_view_type=FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            sources=[source],
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=_stream_processing_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=DataSourceType.STREAM_WITH_BATCH,
            user_function=user_function,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=output_stream,
            incremental_backfills=False,
        )

        featureView = MaterializedFeatureView(args, inferred_transform, pipeline_function, [source])
        functools.update_wrapper(featureView, user_function)

        return featureView

    return decorator


class StreamFeatureView(MaterializedFeatureView):
    """
    Declare a Stream Feature View that takes in a PushSource.
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        source: Union[PushSource, FilteredSource],
        entities: List[BaseEntity],
        online: Optional[bool] = False,
        offline: Optional[bool] = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]] = None,
        batch_trigger: Optional[BatchTriggerType] = BatchTriggerType.SCHEDULED,
        batch_schedule: Optional[datetime.timedelta] = None,
        batch_compute: Optional[Union[DatabricksClusterConfig, EMRClusterConfig]] = None,
        offline_store: Optional[Union[ParquetConfig, DeltaConfig]] = ParquetConfig(),
        online_store: Optional[DynamoConfig] = None,
        monitor_freshness: bool = False,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        timestamp_field: Optional[str] = None,
        aggregations: Optional[List[Aggregation]] = None,
        incremental_backfills: Optional[bool] = False,
    ) -> None:
        # TODO(TEC-12332): Use a shared StreamFeatureView class for both push and non-push (i.e. standard) stream feature views.
        if not isinstance(source, PushSource) and not (
            isinstance(source, FilteredSource) and isinstance(source.source, PushSource)
        ):
            raise ValueError(
                "StreamFeatureView can only be used with a PushSource or a FilteredSource with a PushSource."
            )

        args = build_materialized_feature_view_args(
            feature_view_type=FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            pipeline_function=None,
            sources=[source],
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=None,
            stream_processing_mode=StreamProcessingMode.CONTINUOUS,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=None,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=DataSourceType.PUSH,
            user_function=None,
            max_batch_aggregation_interval=None,
            output_stream=None,
            incremental_backfills=incremental_backfills,
        )

        super().__init__(
            args,
            pipeline_function=None,
            inferred_transform=None,
            sources=[source],
        )


@typechecked
def batch_feature_view(
    *,
    mode: str,
    sources: Sequence[Union[BatchSource, FilteredSource]],
    entities: List[BaseEntity],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: List[Aggregation] = [],
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]] = None,
    batch_trigger: BatchTriggerType = BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[List[str]] = None,
    batch_compute: Optional[Union[DatabricksClusterConfig, EMRClusterConfig]] = None,
    offline_store: Optional[Union[ParquetConfig, DeltaConfig]] = ParquetConfig(),
    online_store: Optional[Union[DynamoConfig, RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    incremental_backfills: bool = False,
):
    """
    Declare a Batch Feature View.

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("spark_sql", "pyspark", "snowflake_sql", "snowpark", or "athena" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: The data source inputs to the feature view.
    :param entities: The entities this feature view is associated with.
    :param aggregation_interval: How frequently the feature value is updated (for example, `"1h"` or `"6h"`)
    :param aggregations: A list of :class:`Aggregation` structs.
    :param online: Whether the feature view should be materialized to the online feature store. (Default: False)
    :param offline: Whether the feature view should be materialized to the offline feature store. (Default: False)
    :param ttl: The TTL (or "look back window") for features defined by this feature view. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
    :param feature_start_time: When materialization for this feature view should start from. (Required if offline=true)
    :param batch_schedule: The interval at which batch materialization should be scheduled.
    :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
    :param batch_trigger: Defines the mechanism for initiating batch materialization jobs.
        One of `BatchTriggerType.SCHEDULED` or `BatchTriggerType.MANUAL`.
        The default value is `BatchTriggerType.SCHEDULED`, where Tecton will run materialization jobs based on the
        schedule defined by the ``batch_schedule`` parameter. If set to `BatchTriggerType.MANUAL`, then batch
        materialization jobs must be explicitly initiated by the user through either the Tecton SDK or Airflow operator.
    :param batch_compute: Batch materialization cluster configuration.
    :param offline_store: Configuration for how data is written to the offline feature store.
    :param online_store: Configuration for how data is written to the online feature store.
    :param monitor_freshness: If true, enables monitoring when feature data is materialized to the online feature store.
    :param expected_feature_freshness: Threshold used to determine if recently materialized feature data is stale. Data is stale if ``now - most_recent_feature_value_timestamp > expected_feature_freshness``. For feature views using Tecton aggregations, data is stale if ``now - round_up_to_aggregation_interval(most_recent_feature_value_timestamp) > expected_feature_freshness``. Where ``round_up_to_aggregation_interval()`` rounds up the feature timestamp to the end of the ``aggregation_interval``. Value must be at least 2 times ``aggregation_interval``. If not specified, a value determined by the Tecton backend is used.
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param timestamp_field: The column name that refers to the timestamp for records that are produced by the
        feature view. This parameter is optional if exactly one column is a Timestamp type. This parameter is
        required if using Tecton on Snowflake without Snowpark.
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param max_batch_aggregation_interval: (Advanced) Configure the time range materialized by each backfill jobs. This can help optimize large backfill jobs.
    :param incremental_backfills: If set to `True`, the feature view will be backfilled one interval at a time as
        if it had been updated "incrementally" since its feature_start_time. For example, if `batch_schedule` is 1 day
        and `feature_start_time` is 1 year prior to the current time, then the backfill will run 365 separate
        materialization jobs to fill the historical feature data.
    :return: An object of type :class:`tecton.declarative.feature_view.MaterializedFeatureView`.

    Example BatchFeatureView declaration:

    .. code-block:: python

        from datetime import datetime
        from datetime import timedelta

        from fraud.entities import user
        from fraud.data_sources.credit_scores_batch import credit_scores_batch

        from tecton import batch_feature_view, Aggregation, FilteredSource

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            entities=[user],
            mode='spark_sql',
            online=True,
            offline=True,
            feature_start_time=datetime(2020, 10, 10),
            batch_schedule=timedelta(days=1),
            ttl=timedelta(days=60),
            description="Features about the users most recent transaction in the past 60 days. Updated daily.",
            )

        def user_last_transaction_features(credit_scores_batch):
            return f'''
                SELECT
                    USER_ID,
                    TIMESTAMP,
                    AMOUNT as LAST_TRANSACTION_AMOUNT,
                    CATEGORY as LAST_TRANSACTION_CATEGORY
                FROM
                    {credit_scores_batch}
            '''

    Example BatchFeatureView declaration using aggregates:

    .. code-block:: python

        from datetime import datetime
        from datetime import timedelta

        from fraud.entities import user
        from fraud.data_sources.credit_scores_batch import credit_scores_batch

        from tecton import batch_feature_view, Aggregation, FilteredSource

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            entities=[user],
            mode='spark_sql',
            online=True,
            offline=True,
            feature_start_time=datetime(2020, 10, 10),
            aggregations=[
                Aggregation(column="amount", function="mean", time_window=timedelta(days=1)),
                Aggregation(column="amount", function="mean", time_window=timedelta(days=30)),
            ],
            aggregation_interval=timedelta(days=1),
            description="Transaction amount statistics and total over a series of time windows, updated daily.",
            )

        def user_recent_transaction_aggregate_features(credit_scores_batch):
            return f'''
                SELECT
                    USER_ID,
                    AMOUNT,
                    TIMESTAMP
                FROM
                    {credit_scores_batch}
            '''
    """

    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            inferred_transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = transformation(mode, name, description, owner, tags=tags)(user_function)

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        stream_processing_mode = StreamProcessingMode.TIME_INTERVAL if aggregations else None

        args = build_materialized_feature_view_args(
            feature_view_type=FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            sources=sources,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=DataSourceType.BATCH,
            user_function=user_function,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=None,
            incremental_backfills=incremental_backfills,
        )

        featureView = MaterializedFeatureView(args, inferred_transform, pipeline_function, sources)
        functools.update_wrapper(featureView, user_function)

        return featureView

    return decorator


def _build_default_cluster_config():
    return feature_view_pb2.ClusterConfig(
        implicit_config=feature_view_pb2.DefaultClusterConfig(**DEFAULT_SPARK_VERSIONS)
    )


def _build_pipeline(
    fv_name: str,
    user_function: Optional[Callable],
    pipeline_function: Optional[Callable[..., PipelineNode]],
    data_source_type: DataSourceType,
    sources: Sequence[Union[BaseDataSource, FilteredSource]],
) -> PipelineNode:
    if user_function is None:
        assert (
            data_source_type == DataSourceType.PUSH
        ), "Only Stream Feature Views with PushSource are allowed no transformations"
        assert len(sources) == 1, "Feature Views can only have one PushSource"
        source = sources[0]
        assert isinstance(
            source, (FilteredSource, PushSource)
        ), "Unsupported Data Source type for FeatureView with PushSource"
        input_name = source.name if isinstance(source, PushSource) else source.source.name
        pipeline_root = source_to_pipeline_node(source=source, input_name=input_name)
    else:
        assert data_source_type != DataSourceType.PUSH, "Push sources cannot have a transformation"
        fn_params = get_source_input_params(user_function)
        params_to_sources = dict(zip(fn_params, sources))
        pipeline_root = transformation_to_pipeline_node(pipeline_function, params_to_sources)
        # we bind to user_function since pipeline_function may be artificially created and just accept **kwargs
        test_binding_user_function(user_function, params_to_sources)

    transformation_type_checker(
        fv_name,
        pipeline_root,
        "pipeline",
        ["pipeline", "spark_sql", "pyspark", "snowflake_sql", "athena"],
    )

    return pipeline_root


@typechecked
def build_materialized_feature_view_args(
    name: str,
    pipeline_function: Optional[Callable[..., PipelineNode]],
    sources: Sequence[Union[BaseDataSource, FilteredSource]],
    entities: List[BaseEntity],
    online: bool,
    offline: bool,
    offline_store: Union[ParquetConfig, DeltaConfig],
    online_store: Optional[Union[DynamoConfig, RedisConfig]],
    aggregation_interval: Optional[datetime.timedelta],
    aggregations: Optional[List[Aggregation]],
    ttl: Optional[datetime.timedelta],
    feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]],
    batch_schedule: Optional[datetime.timedelta],
    online_serving_index: Optional[List[str]],
    batch_compute: Optional[Union[DatabricksClusterConfig, EMRClusterConfig]],
    stream_compute: Optional[Union[DatabricksClusterConfig, EMRClusterConfig]],
    monitor_freshness: bool,
    expected_feature_freshness: Optional[datetime.timedelta],
    alert_email: Optional[str],
    description: Optional[str],
    owner: Optional[str],
    tags: Optional[Dict[str, str]],
    feature_view_type: FeatureViewType,
    timestamp_field: Optional[str],
    data_source_type: DataSourceType,
    user_function: Optional[Callable],
    incremental_backfills: bool,
    stream_processing_mode: Optional[StreamProcessingMode] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[OutputStream] = None,
    batch_trigger: Optional[BatchTriggerType] = None,
) -> FeatureViewArgs:
    """Build feature view args proto for materialized feature views (i.e. batch and stream feature views)."""
    pipeline_root = _build_pipeline(name, user_function, pipeline_function, data_source_type, sources)

    batch_compute_proto = batch_compute._to_cluster_proto() if batch_compute else None

    stream_compute_proto = None
    if stream_compute:
        stream_compute_proto = stream_compute._to_cluster_proto()
    elif data_source_type == DataSourceType.STREAM_WITH_BATCH:
        stream_compute_proto = _build_default_cluster_config()

    monitoring = None
    if monitor_freshness:
        monitoring = MonitoringConfig(monitor_freshness, expected_feature_freshness, alert_email)

    aggregation_protos = None
    if aggregations:
        # TODO(jake): Move these assertions to backend validations.
        assert ttl is None, "`ttl` is automatically set for aggregations to the `aggregation_interval`"
        assert not incremental_backfills, "`incremental_backfills` cannot be used with aggregations"

        is_continuous = stream_processing_mode == StreamProcessingMode.CONTINUOUS
        if aggregation_interval is None:
            aggregation_interval = datetime.timedelta(seconds=0)

        if is_continuous:
            assert aggregation_interval == datetime.timedelta(
                seconds=0
            ), "If `stream_processing_mode=StreamProcessingMode.CONTINUOUS`, `aggregation_interval` must be unset or zero."
        else:
            assert aggregation_interval > datetime.timedelta(
                seconds=0
            ), "`aggregation_interval` or `stream_processing_mode=StreamProcessingMode.CONTINUOUS` is required if specifying aggregations."

        aggregation_protos = [agg._to_proto(aggregation_interval, is_continuous) for agg in aggregations]
    else:
        assert aggregation_interval is None, "`aggregation_interval` can only be specified when using `aggregations`"

    return FeatureViewArgs(
        feature_view_id=IdHelper.from_string(IdHelper.generate_string_id()),
        version=FrameworkVersion.FWV5.value,
        info=prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags),
        entities=[EntityKeyOverride(entity_id=entity._id, join_keys=entity.join_keys) for entity in entities],
        pipeline=Pipeline(root=pipeline_root),
        feature_view_type=feature_view_type,
        online_serving_index=online_serving_index if online_serving_index else None,
        online_enabled=online,
        offline_enabled=offline,
        materialized_feature_view_args=MaterializedFeatureViewArgs(
            timestamp_field=timestamp_field,
            feature_start_time=time_utils.datetime_to_proto(feature_start_time),
            batch_schedule=time_utils.timedelta_to_proto(batch_schedule),
            offline_store=offline_store._to_proto(),
            online_store=online_store._to_proto() if online_store else None,
            max_batch_aggregation_interval=time_utils.timedelta_to_proto(max_batch_aggregation_interval),
            monitoring=monitoring._to_proto() if monitoring else None,
            data_source_type=data_source_type,
            incremental_backfills=incremental_backfills,
            batch_trigger=batch_trigger.value,
            output_stream=output_stream._to_proto() if output_stream else None,
            batch_compute=batch_compute_proto,
            stream_compute=stream_compute_proto,
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            stream_processing_mode=stream_processing_mode.value if stream_processing_mode else None,
            aggregations=aggregation_protos,
            aggregation_interval=time_utils.timedelta_to_proto(aggregation_interval),
        ),
    )
