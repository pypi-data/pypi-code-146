from __future__ import annotations

from collections import defaultdict
import logging
from typing import Optional, Sequence, Tuple

import pandas as pd

from truera.analytics.loader.metarepo_client import MetarepoClient
from truera.authn.usercontext import RequestContext
from truera.client.private.communicator.query_service_communicator import \
    GrpcQueryServiceCommunicator
from truera.client.public.auth_details import AuthDetails
import truera.protobuf.public.common.data_locator_pb2 as dl_pb
import truera.protobuf.public.common_pb2 as common_pb
from truera.protobuf.public.qoi_pb2 import \
    QuantityOfInterest  # pylint: disable=no-name-in-module
from truera.protobuf.queryservice import query_service_pb2 as qs_pb
from truera.utils.datetime_util.datetime_parse_util import \
    parse_timestamp_from_dataframe
from truera.utils.truera_status import TruEraInternalError

value_extractors = {
    "BYTE": lambda x: x.byte_value,
    "INT16": lambda x: x.short_value,
    "INT32": lambda x: x.int_value,
    "INT64": lambda x: x.long_value,
    "FLOAT": lambda x: x.float_value,
    "DOUBLE": lambda x: x.double_value,
    "STRING": lambda x: x.string_value,
    "BOOLEAN": lambda x: x.bool_value,
    "TIMESTAMP": lambda x: x.timestamp_value.seconds
}

dtype_conversion_dict = {
    "BYTE": "int8",
    "INT16": "int16",
    "INT32": "int32",
    "INT64": "int64",
    "FLOAT": "float32",
    "DOUBLE": "float64",
    "STRING": "string",
    "BOOLEAN": "bool",
    "TIMESTAMP":
        "int64"  # Note: treated as int64 (only 'seconds' field is used)
}

TRUERA_SPLIT_ID_COL = "__truera_split_id__"


class QueryServiceClient(object):

    def __init__(
        self,
        connection_string: str,
        metarepo_client: MetarepoClient,
        auth_details: AuthDetails = None,
        logger=None
    ):
        self.communicator = GrpcQueryServiceCommunicator(
            connection_string, auth_details, logger
        )
        self.metarepo_client = metarepo_client
        self.logger = logger or logging.getLogger(__name__)
        self.value_extractors_dict = value_extractors
        self.dtypes_dict = dtype_conversion_dict

    def echo(self, request_id: str, message: str) -> qs_pb.EchoResponse:
        self.logger.info(
            f"QueryServiceClient::echo request_id={request_id}, message={message}"
        )
        request = qs_pb.EchoRequest(request_id=request_id, message=message)
        response = self.communicator.echo(request)
        return response

    def getPreprocessedData(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, include_system_data: bool, request_id: str,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        return self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_PRE",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getProcessedOrPreprocessedData(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, include_system_data: bool, request_id: str,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        processed_data = self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_POST",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

        return processed_data if not None else self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_PRE",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getLabels(
        self, project_id: str, data_collection_id: str,
        query_spec: qs_pb.QuerySpec, include_system_data: bool, request_id: str,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        return self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_LABEL",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getExtraData(
        self,
        project_id: str,
        data_collection_id: str,
        query_spec: qs_pb.QuerySpec,
        include_system_data: bool,
        request_id: str,
        request_context: RequestContext,
    ) -> pd.DataFrame:
        return self._read_static_data(
            project_id=project_id,
            data_collection_id=data_collection_id,
            query_spec=query_spec,
            expected_data_kind="DATA_KIND_EXTRA",
            include_system_data=include_system_data,
            request_id=request_id,
            request_context=request_context
        )

    def getModelPredictions(
        self, project_id: str, model_id: str, query_spec: qs_pb.QuerySpec,
        quantity_of_interest: QuantityOfInterest, include_system_data: bool,
        request_context: RequestContext
    ) -> Optional[pd.DataFrame]:
        # TODO: once iceberg contain split_id remove this resolution
        split_proto = self.metarepo_client.get_datasplit_by_id(
            split_id=query_spec.split_id, request_ctx=request_context
        )
        query_spec.split_id = split_proto.id
        request = qs_pb.QueryRequest(
            id=request_context.get_request_id(),
            project_id=project_id,
            prediction_request=qs_pb.PredictionRequest(
                model_id=model_id,
                qoi=quantity_of_interest,
                query_spec=query_spec
            )
        )
        dataframe = self._pb_stream_to_dataframe(
            self.communicator.query(request, request_context)
        )
        # standardize prediction col name for downstream use
        prediction_col_name = None
        for col in dataframe.columns:
            if col != split_proto.timestamp_column_name and col != split_proto.unique_id_column_name:
                prediction_col_name = col
        assert prediction_col_name
        return parse_timestamp_from_dataframe(
            dataframe,
            split_proto.timestamp_column_name,
            include_timestamp_col=include_system_data
        ).set_index(split_proto.unique_id_column_name)

    def getModelInfluences(
        self,
        project_id: str,
        request_context: RequestContext,
        query_spec: qs_pb.QuerySpec,
        options: common_pb.FeatureInfluenceOptions,
        model_id: Optional[str] = None,
        include_system_data: bool = False,
    ) -> Optional[pd.DataFrame]:
        split_proto = self.metarepo_client.get_datasplit_by_id(
            split_id=query_spec.split_id, request_ctx=request_context
        )
        query_spec.split_id = split_proto.id
        request = qs_pb.QueryRequest(
            id=request_context.get_request_id(),
            project_id=project_id,
            feature_influence_request=qs_pb.FeatureInfluenceRequest(
                model_id=model_id, query_spec=query_spec, options=options
            )
        )
        response_stream = self.communicator.query(request, request_context)
        dataframe = self._pb_stream_to_dataframe(response_stream)

        dataframe = self._resolve_split_metadata(
            dataframe=dataframe,
            include_system_data=include_system_data,
            split_proto=split_proto,
            cols_to_drop=[]
        )
        return dataframe

    def _read_static_data(
        self,
        *,
        project_id: str,
        data_collection_id: str,
        query_spec: qs_pb.QuerySpec,
        expected_data_kind: str,
        include_system_data: bool,
        request_id: str,
        request_context: RequestContext,
    ) -> Optional[pd.DataFrame]:
        split_proto = self.metarepo_client.get_datasplit_by_id(
            split_id=query_spec.split_id, request_ctx=request_context
        )
        query_spec.split_id = split_proto.id
        request = qs_pb.QueryRequest(
            id=request_id,
            project_id=project_id,
            raw_data_request=qs_pb.RawDataRequest(
                data_kind=expected_data_kind,
                data_collection_id=data_collection_id,
                query_spec=query_spec
            )
        )
        response_stream = self.communicator.query(request, request_context)
        dataframe = self._pb_stream_to_dataframe(response_stream)

        dataframe = self._resolve_split_metadata(
            dataframe=dataframe,
            include_system_data=include_system_data,
            split_proto=split_proto,
            cols_to_drop=[TRUERA_SPLIT_ID_COL]
        )
        return dataframe

    def _get_table_data_locator(
        self, data_collection_id: str, data_kind: str, catalog: str,
        request_id: str, request_context: RequestContext
    ) -> Optional[dl_pb.DataLocator]:

        try:
            locators = self.metarepo_client.search_table_data_locators(
                data_collection_id=data_collection_id,
                base_data_kind=data_kind,
                catalog=catalog,
                request_ctx=request_context
            )
        except Exception as ex:
            self.logger.error(
                f"encountered error while searching for table data locators: data_collection_id={data_collection_id}, data_kind={data_kind}, request_id={request_id}, error={str(ex)}"
            )
            raise ex
        locators_count = len(locators)
        if locators_count == 0:
            self.logger.info(
                f"could not find table data locators: data_collection_id={data_collection_id}, data_kind={data_kind}, request_id={request_id}"
            )
            return None

        if locators_count == 1:
            return locators[0]

        # locators_count > 1
        error_msg = f"found {locators_count} table data locators: data_collection_id={data_collection_id}, data_kind={data_kind}, request_id={request_id}"
        self.logger.error(error_msg)
        raise TruEraInternalError(error_msg)

    @staticmethod
    def _generate_query(data_locator: dl_pb.DataLocator, split_id: str) -> str:
        # convert enum name to what we really want (naming conventions...)
        catalog = common_pb.TableCatalog.Name(data_locator.table.catalog)
        if catalog != 'TABLE_CATALOG_ICEBERG':  # defined in: protocol/truera/protobuf/public/common.proto
            raise TruEraInternalError(f"Unknown catalog name: {catalog}")
        catalog = "iceberg"
        schema = data_locator.table.schema
        table = data_locator.table.name
        return f"""SELECT * FROM "{catalog}"."{schema}"."{table}" WHERE {TRUERA_SPLIT_ID_COL} = '{split_id}'"""

    def _pb_stream_to_dataframe(
        self, response_stream: qs_pb.QueryResponse
    ) -> pd.DataFrame:
        first_element = True
        dataframes = []
        extractors = None
        dtypes = None
        table_metadata = None

        for stream_element in response_stream:
            table = stream_element.row_major_value_table
            # only the first element contains the table's metadata
            if first_element:
                first_element = False
                extractors, dtypes, table_metadata = self._process_metadata(
                    table, stream_element.request_id
                )
            # create a dataframe from single pb message/stream element
            df_data = [
                self._extract_row_values(table_metadata, row, extractors)
                for row in table.rows
            ]
            dataframes.append(pd.DataFrame(df_data))

        if len(dataframes) == 0:
            raise TruEraInternalError(
                "QueryServiceClient::_pb_stream_to_dataframe got empty response from query service"
            )
        return pd.concat(
            dataframes, ignore_index=True, copy=False
        ).astype(dtypes).rename(
            columns={tm.index: tm.name for tm in table_metadata}
        )

    def _process_metadata(
        self, table: qs_pb.QueryResponse.row_major_value_table, request_id: str
    ) -> Tuple[dict, dict, Sequence[qs_pb.ColumnMetadata]]:
        if len(table.metadata) == 0:
            raise TruEraInternalError(
                "table metadata is not available. request_id={}.".
                format(request_id)
            )
        # python formatter is a gift that keeps on giving
        return self._value_extractors_for_response(
            table
        ), self._dtypes_for_response(table), table.metadata

    @staticmethod
    def _extract_row_values(table_metadata, row, extractors) -> dict:
        row_dict = defaultdict()
        for column_meta in table_metadata:
            cell = row.columns[column_meta.index]
            value_extractor = extractors.get(column_meta.index)
            value = value_extractor(cell)
            row_dict[column_meta.index] = value
        return row_dict

    # use qs_pb.ValueType and self.value_extractors_dict to assign a value extractor to each column based on response metadata
    def _value_extractors_for_response(
        self, table: qs_pb.QueryResponse.row_major_value_table
    ) -> dict:
        return {
            column_meta.index: self.value_extractors_dict.get(
                qs_pb.ValueType.Name(column_meta.type)
            ) for column_meta in table.metadata
        }

    # use qs_pb.ValueType and self.dtypes_dict to get dtypes for the dataframe based on response metadata
    def _dtypes_for_response(
        self, table: qs_pb.QueryResponse.row_major_value_table
    ) -> dict:
        return {
            column_meta.index:
            self.dtypes_dict.get(qs_pb.ValueType.Name(column_meta.type))
            for column_meta in table.metadata
        }

    def _resolve_split_metadata(
        self, dataframe, include_system_data, split_proto, cols_to_drop
    ):
        if include_system_data:
            # get datetime from integer epoch, but cast to string for AIQ purposes
            dataframe[split_proto.timestamp_column_name] = pd.to_datetime(
                dataframe[split_proto.timestamp_column_name], unit="s"
            ).astype(str)
        else:
            cols_to_drop.append(split_proto.timestamp_column_name)
        dataframe.drop(cols_to_drop, axis="columns", inplace=True)
        dataframe.set_index(split_proto.unique_id_column_name, inplace=True)
        return dataframe
