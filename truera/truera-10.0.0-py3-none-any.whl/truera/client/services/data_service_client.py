import base64
from collections import defaultdict
from enum import Enum
import json
import logging
import os
from typing import List, Optional, Union

from google.protobuf.json_format import MessageToDict

from truera.client.client_utils import create_time_range
from truera.client.client_utils import DataOperationFailedError
from truera.client.client_utils import DataOperationPendingError
from truera.client.client_utils import InvalidArgumentCombinationException
from truera.client.client_utils import InvalidInputDataFormat
from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.data_service_communicator import \
    DataServiceCommunicator
from truera.client.public.communicator.data_service_http_communicator import \
    HttpDataServiceCommunicator
from truera.protobuf.public.common import schema_pb2 as schema_pb
from truera.protobuf.public.common.data_kind_pb2 import \
    DataKindDescribed  # pylint: disable=no-name-in-module
from truera.protobuf.public.data import filter_pb2 as filter_pb
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as messages_pb
from truera.protobuf.public.data_service import data_service_pb2 as ds_pb
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.protobuf.public.util.data_type_pb2 import \
    StaticDataTypeEnum  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.time_range_pb2 import \
    TimeRange  # pylint: disable=no-name-in-module


class SampleStrategy(Enum):
    INVALID = 0
    FIRST = 1
    RANDOM = 2


# pylint: disable=no-member
def map_strategy_to_proto(strategy) -> messages_pb.SampleStrategy:
    if strategy == SampleStrategy.FIRST or strategy.upper() == "FIRST":
        return messages_pb.SampleStrategy.SAMPLE_FIRST_N
    if strategy == SampleStrategy.RANDOM or strategy.upper() == "RANDOM":
        return messages_pb.SampleStrategy.SAMPLE_RANDOM

    raise ValueError("Unrecognized sample strategy: {}".format(strategy))


# Internal client for performation data layer operations. It can only be used from within
# the deployment. It exposes 5 basic operations:
# load_data_source -> rowset id, status
#   Currently exposed as separate functions based on the location of the data:
#       load_data_source_local -- Create a rowset from a file accessible to the data service
# get_rowset_status -> status
#   Since attaching to a data source is inherently async, this function lets the caller check
#   to see if the operation is completed. Can also be used to check the status of filters
# apply_filter -> rowset_id
#   Apply a filter to an already existing rowset
# materialize_data -> materialize operation id
#   Write out a split for a rowset - this may change significantly once we can write more than
#   one file into the split, but the basic idea is unchanged.
# get_materialize_data_status -> status
#   Because materializing a rowset is inherently async, this function lets the caller check to
#   see if the operation is completed.
#
# It is expected that the typical caller will call these operations in that order with filter
# being applied 0 to N times.
class DataServiceClient:

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self, communicator: DataServiceCommunicator, logger=None
    ) -> None:
        self.logger = logger if logger else logging.getLogger(__name__)
        self.communicator = communicator

    @classmethod
    def create(
        cls,
        connection_string: str = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if use_http:
            communicator = HttpDataServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.data_service_grpc_communicator import \
                GrpcDataServiceCommunicator
            communicator = GrpcDataServiceCommunicator(
                connection_string, auth_details, logger
            )
        return DataServiceClient(communicator, logger)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    # Shared function for all locations of data to be parsed -- this is to help the externally used
    # versions of this function have fewer parameters since at least some parameters will be hardcoded
    # in all cases.
    def _load_data_source_input_file(
        self,
        project_id: str,
        uri: str,
        name: str,
        description: str,
        format: messages_pb.Format,
        creation_reason: bool,
        data_kind: DataKindDescribed,
        ds_type: messages_pb.DataSourceType = messages_pb.DataSourceType.
        DS_LOCAL,
        file_time_range: TimeRange = None,
        *,
        credentials: messages_pb.Credentials = None,
        credential_id=None,
        request_context=None,
        data_collection_id: str = None,
    ):
        self.logger.debug(
            "Call to load data source: project_id=%s, uri=%s, ds_type=%s, format=%s",
            project_id, uri, str(ds_type), str(format)
        )
        load_data_info = messages_pb.LoadDataInfo(
            project_id=project_id,
            name=name,
            description=description,
            type=ds_type,
            uri=uri,
            creation_reason=creation_reason,
            format=format,
            data_collection_id=data_collection_id,
            describes_file_kind=data_kind,
            file_time_range=file_time_range
        )

        if credential_id:
            # pylint: disable=protobuf-type-error
            load_data_info.credential_id = credential_id
        elif credentials:
            load_data_info.credentials.CopyFrom(credentials)

        load_request = ds_pb.LoadDataRequest(data_source_info=load_data_info)
        response = self.communicator.load_data_source(
            load_request, request_context=request_context
        )
        return response.rowset_id, response.rowset_state.status

    # Shared function for all relational database reads -- this is to help the externally used
    # versions of this function have fewer parameters since at least some parameters will be hardcoded
    # in all cases.
    def _load_data_source_relational_database(
        self,
        project_id: str,
        uri: str,
        name: str,
        description: str,
        ds_type: messages_pb.DataSourceType,
        database_name: str,
        table_name: str,
        creation_reason: messages_pb.CreationReason,
        data_kind: DataKindDescribed,
        *,
        credentials: messages_pb.Credentials = None,
        credential_id: str = None,
        request_context=None,
        columns: Optional[List[schema_pb.ColumnDetails]] = None,
        data_collection_id: str = None,
    ):
        if columns is None:
            columns = []
        self.logger.debug(
            "Call to load data source: project_id=%s, uri=%s, ds_type=%s",
            project_id, uri, str(ds_type)
        )
        load_data_info = messages_pb.LoadDataInfo(
            project_id=project_id,
            name=name,
            description=description,
            type=ds_type,
            uri=uri,
            creation_reason=creation_reason,
            db_info=messages_pb.DatabaseInfo(
                database_name=database_name,
                table_name=table_name,
                columns=columns
            ),
            data_collection_id=data_collection_id,
            describes_file_kind=data_kind
        )

        if credential_id:
            # pylint: disable=protobuf-type-error
            load_data_info.credential_id = credential_id
        else:
            load_data_info.credentials.CopyFrom(credentials)

        load_request = ds_pb.LoadDataRequest(data_source_info=load_data_info)
        response = self.communicator.load_data_source(
            load_request, request_context=request_context
        )
        return response.rowset_id, response.rowset_state.status

    def put_secret_cred(self, credentials, request_context=None):
        req = ds_pb.PutCredentialRequest(credentials=credentials)
        return self.communicator.put_secret_cred(
            req, request_context=request_context
        ).id

    def get_credential_metadata(self, credential_id, credential_name):
        if credential_id:
            req = ds_pb.GetCredentialMetadataRequest(id=credential_id)
        else:
            req = ds_pb.GetCredentialMetadataRequest(name=credential_name)
        return self.communicator.get_credential_metadata(
            req
        ).credential_metadata

    def delete_credential(self, credential_id):
        req = ds_pb.DeleteCredentialRequest(id_to_delete=credential_id)
        return self.communicator.delete_credential(req)

    def load_data_source_local(
        self,
        project_id: str,
        uri: str,
        format: messages_pb.Format,
        *,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        request_context=None,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = None
    ):
        ds_name = self._get_ds_name(name, uri, creation_reason, split_uri=True)

        return self._load_data_source_input_file(
            project_id,
            uri,
            ds_name,
            description or uri,
            format,
            creation_reason,
            data_kind=data_kind,
            request_context=request_context,
            data_collection_id=data_collection_id,
        )

    def load_data_source_wasb_blob(
        self,
        project_id: str,
        uri: str,
        format: messages_pb.Format,
        *,
        account_key: str = None,
        credential_id: str = None,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        request_context=None,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = None,
    ):
        ds_name = self._get_ds_name(name, uri, creation_reason)
        return self._load_data_source_input_file(
            project_id,
            uri,
            ds_name,
            description or uri,
            format,
            creation_reason,
            data_kind=data_kind,
            ds_type=messages_pb.DataSourceType.DS_WASB_BLOB,
            credentials=messages_pb.Credentials(secret=account_key),
            credential_id=credential_id,
            request_context=request_context,
            data_collection_id=data_collection_id
        )

    def load_data_source_s3_bucket(
        self,
        project_id: str,
        uri: str,
        format: messages_pb.Format,
        *,
        access_key_id: str = None,
        secret_access_key: str = None,
        credential_id: str = None,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        request_context=None,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = None,
        file_time_range: TimeRange = None
    ):
        ds_name = self._get_ds_name(name, uri, creation_reason)
        return self._load_data_source_input_file(
            project_id,
            uri,
            ds_name,
            description or uri,
            format,
            creation_reason,
            data_kind=data_kind,
            ds_type=messages_pb.DataSourceType.DS_S3_BUCKET,
            credentials=messages_pb.Credentials(
                identity=access_key_id, secret=secret_access_key
            ),
            credential_id=credential_id,
            request_context=request_context,
            data_collection_id=data_collection_id,
            file_time_range=file_time_range
        )

    def load_data_source_mysql_table(
        self,
        project_id: str,
        uri: str,
        database_name: str,
        table_name: str,
        *,
        username: str = None,
        password: str = None,
        credential_id: str = None,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        request_context=None,
        columns: Optional[List[schema_pb.ColumnDetails]] = None,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = None
    ):
        if columns is None:
            columns = []

        return self._load_data_source_relational_database(
            project_id,
            uri,
            self._get_ds_name(name, uri, creation_reason),
            description or uri,
            messages_pb.DataSourceType.DS_MYSQL,
            database_name,
            table_name,
            creation_reason,
            data_kind=data_kind,
            credentials=messages_pb.Credentials(
                identity=username, secret=password
            ),
            credential_id=credential_id,
            request_context=request_context,
            columns=columns,
            data_collection_id=data_collection_id
        )

    def load_data_source_hive_table(
        self,
        project_id: str,
        uri: str,
        database_name: str,
        table_name: str,
        *,
        username: str = None,
        password: str = None,
        credential_id: str = None,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        request_context=None,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = None
    ):
        return self._load_data_source_relational_database(
            project_id,
            uri,
            self._get_ds_name(name, uri, creation_reason),
            description or uri,
            messages_pb.DataSourceType.DS_HIVE,
            database_name,
            table_name,
            creation_reason,
            data_kind=data_kind,
            credentials=messages_pb.Credentials(
                identity=username, secret=password
            ),
            credential_id=credential_id,
            request_context=request_context,
            data_collection_id=data_collection_id
        )

    def load_data_source_jdbc(
        self,
        project_id: str,
        uri: str,
        database_name: str,
        table_name: str,
        *,
        username: str = None,
        password: str = None,
        credential_id: str = None,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        request_context=None,
        columns: Optional[List[schema_pb.ColumnDetails]] = None,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = None
    ):
        if columns is None:
            columns = []
        return self._load_data_source_relational_database(
            project_id,
            uri,
            self._get_ds_name(name, uri, creation_reason),
            description or uri,
            messages_pb.DataSourceType.DS_JDBC,
            database_name,
            table_name,
            creation_reason,
            data_kind=data_kind,
            credentials=messages_pb.Credentials(
                identity=username, secret=password
            ),
            credential_id=credential_id,
            request_context=request_context,
            columns=columns,
            data_collection_id=data_collection_id
        )

    def load_data_source_big_query_table(
        self,
        project_id: str,
        database_name: str,
        table_name: str,
        *,
        password: str = None,
        credential_id: str = None,
        name: str = None,
        description: str = None,
        creation_reason=messages_pb.CreationReason.DS_CR_USER_REQUESTED,
        data_kind: DataKindDescribed = None,
        request_context=None,
        columns: Optional[List[schema_pb.ColumnDetails]] = None
    ):
        if columns is None:
            columns = []
        self.logger.info(
            f"Connecting to BigQuery data source {database_name}.{table_name}"
        )
        # make password (service acc key) readable by spark bigquery connector
        if password is not None:
            try:
                json.loads(password)
            except ValueError as e:
                raise InvalidInputDataFormat(
                    "Could not read BigQuery Service Account Key as valid JSON."
                )
            password = base64.b64encode(password.encode("utf-8")
                                       ).decode("utf-8")

        return self._load_data_source_relational_database(
            project_id,
            None,
            name,
            description,
            messages_pb.DataSourceType.DS_BIGQUERY,
            database_name,
            table_name,
            creation_reason,
            data_kind=data_kind,
            credentials=messages_pb.Credentials(secret=password),
            credential_id=credential_id,
            request_context=request_context
        )

    def _get_ds_name(self, name, uri, creation_reason, *, split_uri=False):
        if name:
            return name
        if creation_reason != messages_pb.CreationReason.DS_CR_USER_REQUESTED:
            return ""
        if split_uri:
            return os.path.splitext(os.path.basename(uri))[0]
        return os.path.basename(uri)

    def get_rowset_status_full_response(
        self,
        project_id: str,
        *,
        rowset_id: str = None,
        throw_on_error: bool = True,
        request_context=None,
        data_source_name=None
    ) -> ds_pb.RowsetStatusResponse:
        self.logger.debug(
            "Call to get rowset status: project_id=%s, rowset_id=%s",
            project_id, rowset_id
        )

        if rowset_id:
            load_status_request = ds_pb.GetRowsetStatusRequest(
                project_id=project_id, rowset_id=rowset_id
            )
        elif data_source_name:
            load_status_request = ds_pb.GetRowsetStatusRequest(
                project_id=project_id, data_source_name=data_source_name
            )
        else:
            raise InvalidArgumentCombinationException(
                "No rowset id or data source name provided."
            )

        try:
            response = self.communicator.get_rowset_status(
                load_status_request, request_context=request_context
            )
        except Exception as e:
            response = ds_pb.RowsetStatusResponse(
                rowset_id=rowset_id,
                rowset_state=messages_pb.RowsetState(
                    status=messages_pb.RowsetStatus.RS_STATUS_FAILED,
                    error=str(e)
                )
            )

        if throw_on_error and response.rowset_state.status == messages_pb.RowsetStatus.RS_STATUS_FAILED:
            raise DataOperationFailedError(
                "Error on rowset {} in project {} failed with the following message:\n {}"
                .format(
                    rowset_id or data_source_name, project_id,
                    response.rowset_state.error
                )
            )
        return response

    def get_rowset_status(
        self,
        project_id: str,
        rowset_id: str,
        *,
        throw_on_error: bool = True,
        request_context=None,
        data_source_name=None
    ):
        response = self.get_rowset_status_full_response(
            project_id,
            rowset_id=rowset_id,
            throw_on_error=throw_on_error,
            request_context=request_context,
            data_source_name=data_source_name
        )
        return response.rowset_state.status, response.rowset_state.error

    def get_rowset_metadata(self, rowset_id: str):
        req = ds_pb.GetRowsetMetadataRequest(rowset_id=rowset_id)
        return self.communicator.get_rowset_metadata(req)

    def get_rowset_columns(
        self,
        project_id: str,
        rowset_id: str,
        throw_on_error: bool = True,
        request_context=None
    ):
        self.logger.debug(
            "Call to get rowset columns: project_id=%s, rowset_id=%s",
            project_id, rowset_id
        )
        get_columns_request = ds_pb.GetRowsetColumnsRequest(
            project_id=project_id, rowset_id=rowset_id
        )
        response = self.communicator.get_columns(
            get_columns_request, request_context=request_context
        )
        if throw_on_error and response.status == messages_pb.RowsetStatus.RS_STATUS_FAILED:
            raise DataOperationFailedError(
                "Error on rowset {} in project {} failed with the following message:\n {}"
                .format(rowset_id, project_id, response.error)
            )

        return response.columns, response.status, response.error

    def get_sample_rows(
        self,
        project_id: str,
        rowset_id: str,
        count: int,
        *,
        throw_on_error: bool = True,
        as_data_frame: bool = False,
        request_context=None
    ):
        self.logger.debug(
            "Call to get sample rows: project_id=%s, rowset_id=%s, count=%d",
            project_id, rowset_id, count
        )
        get_rows_req = ds_pb.GetRowsRequest(
            project_id=project_id, rowset_id=rowset_id, count=count
        )
        response = self.communicator.get_rows(
            get_rows_req, request_context=request_context
        )
        if throw_on_error and response.status == messages_pb.RowsetStatus.RS_STATUS_FAILED:
            raise DataOperationFailedError(
                "Error on rowset {} in project {} failed with the following message:\n {}"
                .format(rowset_id, project_id, response.error)
            )
        if as_data_frame:
            return DataServiceClient.proto_table_to_pandas(response)
        return response.rows, response.schema, response.status, response.error

    def apply_filter(
        self,
        project_id: str,
        rowset_id: str,
        filter_expression: filter_pb.FilterExpression,
        request_context=None
    ):
        self.logger.debug(
            "Call to filter: project_id=%s, rowset_id=%s, filter=%s",
            project_id, rowset_id, str(filter_expression)
        )
        filter_request = ds_pb.ApplyFilterRequest(
            project_id=project_id,
            rowset_id=rowset_id,
            filter=filter_expression
        )
        return self.communicator.apply_filter_to_rowset(
            filter_request, request_context=request_context
        ).rowset_id

    def join_rowsets(
        self,
        rowsets: List[str],
        join_columns: List[str],
        *,
        perform_column_rename: bool = True,
        join_type=messages_pb.JoinType.DS_JT_INNER,
        join_types: Optional[List[object]] = None
    ):
        if join_types is None:
            join_types = []
        join_type_info = f"join types {join_types}." if len(
            join_types
        ) > 0 else "default inner join."

        self.logger.info(
            f"Call to join: rowsets {rowsets} on {join_columns} with {join_type_info}"
        )

        rowsets_transformed_to_rowset_with_id = [
            messages_pb.RowsetWithId(
                rowset_id=rowsets[index],
                id_column=join_columns,
                join_type=(
                    join_type if len(join_types) == 0 else join_types[index]
                )
            ) for index in range(len(rowsets))
        ]

        join_request = ds_pb.JoinRequest(
            rowsets=rowsets_transformed_to_rowset_with_id,
            perform_column_rename=perform_column_rename
        )

        return self.communicator.join_rowsets(join_request).rowset_id

    def delete_rowset(self, rowset_id: str, *, delete_children=False):
        req = ds_pb.DeleteRowsetRequest(
            rowset_id=rowset_id, including_children=delete_children
        )
        return self.communicator.delete_rowset(req).deleted_rowset_ids

    def materialize_data(
        self,
        project_id: str,
        rowset_id: str,
        data_collection_id: str,
        approx_max_rows: int,
        sample_strategy: str,
        seed: int = 0,
        split_name: str = "",
        split_type: str = "",
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_INVALID,
        cache_info: messages_pb.CreateCacheInfo = None,
        existing_split_id: str = "",
        outputFiles: List[messages_pb.MaterializedOutputFile] = [],
        id_column: str = "",
        timestamp_column: str = "",
        *,
        uniquified_columns_expected=False,
        split_time_range_begin=None,
        split_time_range_end=None,
        idempotency_id=""
    ):
        self.logger.debug(
            "Call to materialize data: project_id=%s, rowset_id=%s, data_collection=%s, split_name=%s, strategy=%s, rows=%d, seed=%s, existing_split_id=%s, cache_info=%s",
            project_id, rowset_id, data_collection_id, split_name,
            sample_strategy, approx_max_rows, seed, existing_split_id,
            cache_info
        )

        materialize_request = ds_pb.MaterializeDataRequest(
            rowset_id=rowset_id,
            sample_strategy=map_strategy_to_proto(sample_strategy),
            approx_max_rows=approx_max_rows,
            sample_seed=seed,
            data_info=messages_pb.MaterializeDataInfo(
                project_id=project_id,
                output_data_collection_id=data_collection_id,
                cache_info=cache_info,
                system_columns=messages_pb.SystemColumnDetails(id_columns=[])
            ),
            uniquified_columns_expected=uniquified_columns_expected,
            idempotency_id=idempotency_id
        )

        if id_column:
            materialize_request.data_info.system_columns.id_columns.append(
                schema_pb.ColumnDetails(name=id_column)
            )
        if timestamp_column:
            materialize_request.data_info.system_columns.timestamp_column.CopyFrom(
                schema_pb.ColumnDetails(name=timestamp_column)
            )

        if existing_split_id:
            materialize_request.data_info.existing_split_id = existing_split_id
        elif split_name and split_type:
            materialize_request.data_info.create_split_info.CopyFrom(
                messages_pb.CreateSplitInfo(
                    output_split_name=split_name,
                    output_split_type=split_type,
                    output_split_time_range=create_time_range(
                        split_time_range_begin, split_time_range_end
                    ),
                    output_split_mode=split_mode
                )
            )
        else:
            raise ValueError(
                "Must provide either an existing_split_id or a split_name and split_type to create"
            )

        for outputFile in outputFiles:
            materialize_request.data_info.projections.append(outputFile)

        return self.materialize_data_from_request(
            materialize_request
        ).materialize_operation_id

    def materialize_data_from_request(
        self,
        materialize_request: ds_pb.MaterializeDataRequest,
        request_context=None
    ):
        return self.communicator.materialize_data(
            materialize_request, request_context=request_context
        )

    def get_materialize_data_status(
        self,
        project_id: str,
        materialize_operation_id: str,
        throw_on_error: bool = True,
        request_context=None
    ) -> ds_pb.MaterializeDataResponse:
        self.logger.debug(
            "Call get materialize status: project_id=%s, materialize_operation_id=%s",
            project_id, materialize_operation_id
        )
        get_status_request = ds_pb.GetMaterializeDataStatusRequest(
            materialize_operation_id=materialize_operation_id,
            project_id=project_id
        )
        try:
            response = self.communicator.get_materialize_data_status(
                get_status_request, request_context=request_context
            )
        except Exception as e:
            if throw_on_error:
                raise e
            else:
                response = ds_pb.MaterializeDataResponse(
                    status=messages_pb.MaterializeStatus.
                    MATERIALIZE_STATUS_FAILED,
                    error=e.message
                )

        if throw_on_error and response.status == messages_pb.MaterializeStatus.MATERIALIZE_STATUS_FAILED:
            raise DataOperationFailedError(
                "Materialize data operation {} in project {} failed with the following error: {}"
                .format(materialize_operation_id, project_id, response.error)
            )

        return response

    def delete_materialize_data_operation(self, materialize_operation_id: str):
        req = ds_pb.DeleteMaterializeOperationRequest(
            materialize_operation_id=materialize_operation_id
        )
        return self.communicator.delete_materialize_operation(req)

    def get_credentials(self, project_id, *, limit=50, last_key=""):
        self.logger.debug(
            f"Call get credentials: project_id={project_id}, limit={limit}, last_key={last_key}"
        )

        self._check_limit(limit)

        get_credentials_request = ds_pb.GetCredentialsRequest(
            project_id=project_id, last_key=last_key, limit=limit
        )

        response = self.communicator.get_credentials(get_credentials_request)
        return response.credential_metadata, response.has_more_data

    def get_rowsets(
        self,
        project_id,
        *,
        limit=50,
        last_key="",
        root_rowset_id="",
        only_root_rowsets=False,
        include_system_requested=False
    ):
        self.logger.debug(
            f"Call get rowsets: project_id={project_id}, limit={limit}, last_key={last_key}, root_rowset_id={root_rowset_id}"
        )

        self._check_limit(limit)
        if include_system_requested:
            request_list = [
                messages_pb.CreationReason.Value(reason)
                for reason in messages_pb.CreationReason.keys()
            ]
        else:
            request_list = [messages_pb.CreationReason.DS_CR_USER_REQUESTED]

        get_rowsets_request = ds_pb.GetRowsetsRequest(
            project_id=project_id,
            last_key=last_key,
            limit=limit,
            root_rowset_id=root_rowset_id,
            only_with_creation_reasons=request_list,
            only_root_rowsets=only_root_rowsets
        )

        response = self.communicator.get_rowsets(get_rowsets_request)
        return response.rowsets, response.has_more_data

    def get_materialize_operations(self, project_id, *, limit=50, last_key=""):
        self.logger.debug(
            f"Call get materialize operations: project_id={project_id}, limit={limit}, last_key={last_key}"
        )

        self._check_limit(limit)

        get_materialize_operations_request = ds_pb.GetMaterializeOperationsRequest(
            project_id=project_id, last_key=last_key, limit=limit
        )

        response = self.communicator.get_materialize_operations(
            get_materialize_operations_request
        )
        return response.materialize_operations, response.has_more_data

    def register_schema(
        self,
        project_id,
        data_collection_id,
        schemas,
        *,
        request_context=None,
        start_streaming=True
    ):
        req = ds_pb.RegisterSchemaRequest(
            schemas=schemas,
            project_id=project_id,
            data_collection_id=data_collection_id,
            start_streaming=start_streaming,
        )
        return self.communicator.register_schema(
            req, request_context=request_context
        )

    def get_schema(self, schema_id, *, as_json=False, request_context=None):
        req = ds_pb.GetSchemaRequest(schema_id=schema_id)
        message = self.communicator.get_schema(
            req, request_context=request_context
        ).schema

        if as_json:
            return MessageToDict(
                message,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        return message

    def delete_schema(self, schema_id, force=False):
        req = ds_pb.DeleteSchemaRequest(schema_id=schema_id, force=force)
        return self.communicator.delete_schema(req)

    def start_streaming_ingestion(
        self,
        project_id,
        data_collection_id,
        input_topic_name,
    ) -> str:
        req = ds_pb.StartStreamingIngestionRequest(
            input_topic_name=input_topic_name,
            project_id=project_id,
            data_collection_id=data_collection_id
        )
        return self.communicator.start_streaming_ingestion(req)

    def get_streaming_ingestion_status(self, streaming_ingestion_id):
        req = ds_pb.GetStreamingIngestionStatusRequest(
            streaming_ingestion_id=streaming_ingestion_id
        )
        return self.communicator.get_streaming_ingestion_status(req)

    def stop_streaming_ingestion(
        self, streaming_ingestion_id=None, project_id=None
    ):
        req = ds_pb.StopStreamingIngestionRequest(
            streaming_ingestion_id=streaming_ingestion_id,
            project_id=project_id,
        )
        return self.communicator.stop_streaming_ingestion(req)

    def _check_limit(self, limit):
        limit_limit = 250
        if limit > limit_limit:
            raise ValueError(
                f"Limit cannot be set above {limit_limit} but was set to {limit}."
            )

    @classmethod
    def _dtype_enum_to_row_type_attr(cls, dtype_enum):
        if dtype_enum == StaticDataTypeEnum.STRING:
            return 'string_value'
        if dtype_enum == StaticDataTypeEnum.BOOL:
            return 'bool_value'
        if dtype_enum in [StaticDataTypeEnum.INT8, StaticDataTypeEnum.INT16]:
            return 'short_value'
        if dtype_enum == StaticDataTypeEnum.INT32:
            return 'int_value'
        if dtype_enum == StaticDataTypeEnum.INT64:
            return 'long_value'
        if dtype_enum == StaticDataTypeEnum.UINT8:
            return 'byte_value'
        if dtype_enum == StaticDataTypeEnum.FLOAT32:
            return 'float_value'
        if dtype_enum == StaticDataTypeEnum.FLOAT64:
            return 'double_value'
        if dtype_enum in [
            StaticDataTypeEnum.DATETIME, StaticDataTypeEnum.DATETIME64
        ]:
            return 'timestamp_value'
        raise ValueError(
            "Unimplemented datatype : " +
            StaticDataTypeEnum.STRING.Name(dtype_enum)
        )

    @classmethod
    def _schema_to_dtypes_attr_list(cls, schema):
        # the index in list is same as column_index
        dtypes_attr_list = []
        for i in range(len(schema)):
            column_details = schema[i]
            data_type_attr = column_details.data_type.WhichOneof('data_type')
            if data_type_attr == 'static_data_type':
                attr = DataServiceClient._dtype_enum_to_row_type_attr(
                    column_details.data_type.static_data_type
                )
                dtypes_attr_list.append(attr)
            else:
                raise ValueError(
                    "Data type specification " + data_type_attr +
                    " not supported."
                )
        return dtypes_attr_list

    @classmethod
    def proto_table_to_pandas(cls, table):
        import pandas as pd
        if type(table) is tuple:
            rows = table[0]
            schema = table[1]
        elif type(table) is ds_pb.GetRowsResponse:
            if table.status == messages_pb.RowsetStatus.RS_STATUS_STARTED:
                message = "Data still being fetched, please retry the operation."
                if table.error:
                    message += " Details: " + table.error
                raise DataOperationPendingError(message=message)
            assert table.status == messages_pb.RowsetStatus.RS_STATUS_OK
            rows = table.rows
            schema = table.schema
        else:
            raise ValueError(
                "Table should be either a tuple of (rows, schema) or GetRowsResponse, found "
                + type(table)
            )
        col_names = [s.name for s in schema]
        table_dict = defaultdict(list)
        dtype_attr_list = DataServiceClient._schema_to_dtypes_attr_list(schema)
        for row in rows:
            for col in row.columns:
                col_index = col.column_index
                attr = dtype_attr_list[col_index]

                if col.WhichOneof("typed_value") == "null_indicator":
                    table_dict[col_names[col_index]].append(None)
                else:
                    table_dict[col_names[col_index]].append(getattr(col, attr))
        return pd.DataFrame(table_dict)
