from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pendulum
from pyspark.sql.streaming import StreamingQuery

from tecton import conf
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.fco import Fco
from tecton.interactive import snowflake_api
from tecton.interactive import spark_api
from tecton.interactive.data_frame import TectonDataFrame
from tecton.unified import data_source as unified_data_source
from tecton_core import specs
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_core.logger import get_logger
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.common.id_pb2 import Id
from tecton_proto.data.batch_data_source_pb2 import BatchDataSource as BatchDataSourceProto
from tecton_proto.data.stream_data_source_pb2 import StreamDataSource as StreamDataSourceProto
from tecton_proto.data.virtual_data_source_pb2 import VirtualDataSource as VirtualDataSourceProto
from tecton_proto.metadataservice.metadata_service_pb2 import GetVirtualDataSourceRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetVirtualDataSourceSummaryRequest

logger = get_logger("DataSource")


class BaseDataSource(Fco):
    ds_proto: VirtualDataSourceProto
    ds_spec: specs.DataSourceSpec
    batch_ds: BatchDataSourceProto
    stream_ds: Optional[StreamDataSourceProto]
    fco_container: FcoContainer

    @classmethod
    def _from_proto_and_data_sources(
        cls,
        ds_proto: VirtualDataSourceProto,
        fco_container: FcoContainer,
        batch_ds: Optional[BatchDataSourceProto],
        stream_ds: Optional[StreamDataSourceProto],
    ) -> "BaseDataSource":
        """
        Create a new data source instance.
        :param ds_proto: VirtualDataSource proto to be unpacked into a class instance.
        :param batch_ds: BatchDataSource instance representing batch DS to be included
                         into this DS.
        :param stream_ds: Optional StreamDataSource instance representing streaming DS to be
                          included into this DS. If present, this DS class
                          represents a stream DS backed up with a batch DS.
        """
        obj = cls.__new__(cls)
        obj.ds_proto = ds_proto
        obj.ds_spec = specs.DataSourceSpec.from_data_proto(ds_proto)
        obj.fco_container = fco_container
        obj.batch_ds = batch_ds
        obj.stream_ds = stream_ds
        return obj

    @classmethod
    def _create_from_proto(cls, ds_proto, fco_container: FcoContainer) -> "BaseDataSource":
        """
        Creates a new :class:`BaseDataSource` class from persisted Virtual DS proto.

        :param ds_proto: VirtualDataSource proto struct.
        :param fco_container: FcoContainer object.
        :return: :class:`BaseDataSource` class instance.
        """
        batch_ds = ds_proto.batch_data_source
        stream_ds = None
        if ds_proto.HasField("stream_data_source"):
            stream_ds = ds_proto.stream_data_source

        return cls._from_proto_and_data_sources(ds_proto, fco_container, batch_ds, stream_ds)

    @property  # type: ignore
    @sdk_public_method
    def is_streaming(self) -> bool:
        """
        Whether or not it's a StreamDataSource.
        """
        return self.stream_ds is not None

    @property  # type: ignore
    @sdk_public_method
    def columns(self) -> List[str]:
        """
        Returns streaming DS columns if it's present. Otherwise, returns batch DS columns.
        """
        if self.ds_proto.data_source_type == DataSourceType.PUSH:
            schema = self.ds_proto.schema.tecton_schema
            return [field.name for field in schema.columns]

        if self.is_streaming:
            assert self.stream_ds is not None
            schema = self.stream_ds.spark_schema
        else:
            schema = self.ds_proto.batch_data_source.spark_schema

        return [field.name for field in schema.fields]

    @property
    def _proto(self):
        """
        Returns VirtualDataSource proto.
        """
        return self.ds_proto

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "data_source"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "data_sources"

    @property
    def _fco_metadata(self):
        return self._proto.fco_metadata

    def _id_proto(self) -> Id:
        return self._proto.virtual_data_source_id

    @property  # type: ignore
    @sdk_public_method
    def id(self) -> str:
        """
        Returns a unique ID for the data source.
        """
        return IdHelper.to_string(self._id_proto())

    @sdk_public_method
    def get_dataframe(
        self,
        start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        *,
        apply_translator: bool = True,
    ) -> TectonDataFrame:
        """
        Returns this data source's data as a Tecton DataFrame.

        :param start_time: The interval start time from when we want to retrieve source data.
            If no timezone is specified, will default to using UTC.
            Can only be defined if ``apply_translator`` is True.
        :param end_time: The interval end time until when we want to retrieve source data.
            If no timezone is specified, will default to using UTC.
            Can only be defined if ``apply_translator`` is True.
        :param apply_translator: If True, the transformation specified by ``raw_batch_translator``
            will be applied to the dataframe for the data source. ``apply_translator`` is not applicable
            to batch sources configured with ``spark_batch_config`` because it does not have a
            ``post_processor``.

        :return: A Tecton DataFrame containing the data source's raw or translated source data.

        :raises TectonValidationError: If ``apply_translator`` is False, but ``start_time`` or
            ``end_time`` filters are passed in.
        """
        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_dataframe_for_data_source(self.ds_spec, start_time, end_time)
        else:
            return spark_api.get_dataframe_for_data_source(self.ds_spec, start_time, end_time, apply_translator)

    @sdk_public_method
    def summary(self) -> Displayable:
        """
        Displays a human readable summary of this data source.
        """
        request = GetVirtualDataSourceSummaryRequest()
        request.fco_locator.id.CopyFrom(self.ds_proto.virtual_data_source_id)
        request.fco_locator.workspace = self.workspace

        response = metadata_service.instance().GetVirtualDataSourceSummary(request)
        return Displayable.from_fco_summary(response.fco_summary)


class BatchDataSource(BaseDataSource):
    """
    BatchDataSource abstracts batch data sources.

    BatchFeatureViews and BatchWindowAggregateFeatureViews ingest data from BatchDataSources.
    """

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "batch_data_source"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "batch_data_sources"


class StreamDataSource(BaseDataSource):
    """
    StreamDataSource is an abstraction data over streaming data sources.

    StreamFeatureViews and StreamWindowAggregateFeatureViews ingest data from StreamDataSources.

    A StreamDataSource contains a stream data source config, as well as a batch data source config for backfills.
    """

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "stream_data_source"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "stream_data_sources"

    @sdk_public_method
    def start_stream_preview(
        self, table_name: str, *, apply_translator: bool = True, option_overrides: Optional[Dict[str, str]] = None
    ) -> StreamingQuery:
        """
        Starts a streaming job to write incoming records from this DS's stream to a temporary table with a given name.

        After records have been written to the table, they can be queried using ``spark.sql()``. If ran in a Databricks
        notebook, Databricks will also automatically visualize the number of incoming records.

        This is a testing method, most commonly used to verify a StreamDataSource is correctly receiving streaming events.
        Note that the table will grow infinitely large, so this is only really useful for debugging in notebooks.

        :param table_name: The name of the temporary table that this method will write to.
        :param apply_translator: Whether to apply this data source's ``raw_stream_translator``.
            When True, the translated data will be written to the table. When False, the
            raw, untranslated data will be written. ``apply_translator`` is not applicable to stream sources configured
            with ``spark_stream_config`` because it does not have a ``post_processor``.
        :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set
            by the data source. Can be used to configure behavior only for the preview, e.g. setting
            ``startingOffsets:latest`` to preview only the most recent events in a Kafka stream.
        """
        return spark_api.start_stream_preview(self.ds_spec, table_name, apply_translator, option_overrides)


class PushSource(BaseDataSource):
    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "push_source"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "push_sources"


@sdk_public_method
def get_data_source(
    name, workspace_name: Optional[str] = None
) -> Union[
    BatchDataSource, StreamDataSource, PushSource, unified_data_source.BatchSource, unified_data_source.StreamSource
]:
    """
    Fetch an existing :class:`BatchDataSource` or :class:`StreamDataSource` by name.

    :param name: An unique name of the registered Data Source.

    :return: A :class:`BatchDataSource` or :class:`StreamDataSource` class instance.

    :raises TectonValidationError: if a data source with the passed name is not found.
    """
    if workspace_name == None:
        logger.warning(
            "`tecton.get_data_source('<name>')` is deprecated. Please use `tecton.get_workspace('<workspace_name>').get_data_source('<name>')` instead."
        )

    request = GetVirtualDataSourceRequest()
    request.name = name
    request.workspace = workspace_name or conf.get_or_none("TECTON_WORKSPACE")

    response = metadata_service.instance().GetVirtualDataSource(request)
    fco_container = FcoContainer.from_proto(response.fco_container)
    data_source_spec = fco_container.get_single_root()

    # this looks not very intuitive, why not use factory pattern and build the correct derived class instead of this logic?
    if data_source_spec is None:
        raise errors.DATA_SOURCE_NOT_FOUND(name)

    assert isinstance(data_source_spec, specs.DataSourceSpec)
    ds_proto = data_source_spec.data_proto

    if ds_proto.fco_metadata.framework_version != FrameworkVersion.FWV5.value:
        raise errors.UNSUPPORTED_FRAMEWORK_VERSION

    if conf.get_bool("UNIFIED_TECTON_OBJECTS_ENABLED"):
        if data_source_spec.stream_source is not None:
            return unified_data_source.StreamSource._from_spec(data_source_spec)
        else:
            return unified_data_source.BatchSource._from_spec(data_source_spec)
    else:
        if ds_proto.data_source_type == DataSourceType.STREAM_WITH_BATCH:
            return StreamDataSource._create_from_proto(ds_proto, fco_container)
        elif ds_proto.data_source_type == DataSourceType.PUSH:
            return PushSource._create_from_proto(ds_proto, fco_container)
        else:
            return BatchDataSource._create_from_proto(ds_proto, fco_container)
