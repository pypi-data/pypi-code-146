from __future__ import annotations

from typing import List

from google.protobuf.timestamp_pb2 import \
    Timestamp  # pylint: disable=no-name-in-module

from truera.client.column_info import create_materialized_output_file
from truera.client.errors import NotFoundError
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.services.scheduled_ingestion_client import _DEFAULT_SCHEDULE
from truera.client.truera_workspace import TrueraWorkspace
from truera.protobuf.public.common.data_kind_pb2 import \
    DATA_KIND_PRE  # pylint: disable=no-name-in-module
from truera.protobuf.public.common.data_kind_pb2 import \
    DataKindDescribed  # pylint: disable=no-name-in-module
from truera.protobuf.public.common.schema_pb2 import \
    ColumnDetails  # pylint: disable=no-name-in-module
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb
from truera.protobuf.public.data_service import data_service_pb2 as ds_pb
from truera.protobuf.public.qoi_pb2 import \
    QuantityOfInterest  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    DataType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    StaticDataTypeEnum  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.split_mode_pb2 import \
    SplitMode  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.time_range_pb2 import \
    TimeRange  # pylint: disable=no-name-in-module

DEFAULT_ID_COLUMN_NAME = "row_id"
TIMESTAMP_COLUMN_NAME = "inference_time"
EVENT_ID_COLUMN_NAME = "event_id"
OUTPUT_COLUMN_NAME = "output"

DEFAULT_MAX_ROWS_PER_INGESTION = 1_000_000
DEFAULT_MATERIALIZE_SPLIT_TYPE = "prod"
DEFAULT_SCHEMA_DATA_KIND = DATA_KIND_PRE


def setup_monitoring(
    tru: TrueraWorkspace,
    split_name: str,
    datacapture_uri: str,
    credential_name: str,
    *,
    cron_schedule: str = None,
    id_column_name: str = None,
    initial_split_time_range: TimeRange = None,
    max_rows_per_ingestion: int = DEFAULT_MAX_ROWS_PER_INGESTION,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    column_names: List[str] = None,
    column_data_types: List[StaticDataTypeEnum] = None
) -> str:
    """Sets up scheduled ingestion of SageMaker data capture logs into TruEra.

    Will first ingest the last hour (or initial_split_time_range if provided) as an initial split.
    If successful, scheduled ingestion will be set up based on the cron_schedule (once per hour by default).

    Args:
        tru: TrueraWorkspace with project, data_collection, and model set
        split_name: Name of the new data split for data ingestion
        datacapture_uri: URI of SageMaker data capture, s3a://<prefix>/<variant>
        credential_name: Name of the credential to assume when accessing S3. If one with the name does not exist, a new credential will be created if aws_access_key_id and aws_secret_access_key are provided.
        cron_schedule (optional): Schedule to run ingestion. Defaults to "0 * * * *" (once per hour).
        id_column_name (optional): ID column in input data.
        initial_split_time_range (optional): TimeRange for the initial ingestion
        max_rows_per_ingestion (optional): Max number of rows per ingestion. Defaults to 1_000_000.
        aws_access_key_id (optional): AWS access key ID to create a new credential
        aws_secret_access_key (optional): AWS secret access key to create a new credential
        column_names (optional): Name of the columns of model input
        column_data_types (optional): Data types of the columns of model input

    Returns:
        str: Workflow ID of the scheduled ingestion
    """
    tru._ensure_project()
    tru._ensure_data_collection()
    tru._ensure_project()
    tru.set_environment("remote")

    if split_name in tru.get_data_splits():
        raise AlreadyExistsError(f"Data split {split_name} already exists.")

    credential_id = _check_existing_or_create_credentials(
        tru,
        credential_name=credential_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    tru.logger.info("Initializing split...")
    materialize_operation_id = ingest_logs_as_split(
        tru,
        split_name=split_name,
        datacapture_uri=datacapture_uri,
        credential_id=credential_id,
        time_range=initial_split_time_range,
        max_rows=max_rows_per_ingestion,
        id_column_name=id_column_name,
        column_names=column_names,
        column_data_types=column_data_types
    )

    si_client = tru.current_tru.scheduled_ingestion_client
    schedule = _DEFAULT_SCHEDULE if cron_schedule is None else si_client.serialize_schedule(
        cron_schedule
    )
    workflow_id = si_client.schedule(
        project_id=tru.current_tru.project.id,
        template_operation_id=materialize_operation_id,
        schedule=schedule,
        append=True
    )
    tru.logger.info(
        f"SageMaker data ingestion scheduled with workflow id '{workflow_id}' and schedule '{schedule}'"
    )
    return workflow_id


def _check_existing_or_create_credentials(
    tru: TrueraWorkspace,
    credential_name: str,
    *,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None
) -> str:
    """Returns credential id. Creates one if one does not already exist."""
    try:
        credential = tru.get_credential_metadata(credential_name)
        tru.logger.info(f"Using existing credential: {credential_name}")
        return credential.id
    except NotFoundError:
        if aws_access_key_id and aws_secret_access_key:
            credential = tru.add_credential(
                name=credential_name,
                identity=aws_access_key_id,
                secret=aws_secret_access_key
            )
            tru.logger.info(f"Created credential {credential_name}")
            return credential.id
        else:
            raise ValueError(
                f"Credential {credential_name} does not exist. Specify both aws_access_key_id and aws_secret_access_key to create one instead"
            )


def build_datacapture_load_request(
    column_details: List[ColumnDetails], s3_uri: str, credential_id: str,
    project_id: str, data_collection_id: str, file_time_range: TimeRange
) -> ds_pb.LoadDataRequest:
    data_format = ds_messages_pb.Format(
        file_type=ds_messages_pb.FT_SAGEMAKER_MONITORING_LOG,
        columns=column_details
    )
    load_data_info = ds_messages_pb.LoadDataInfo(
        project_id=project_id,
        data_collection_id=data_collection_id,
        describes_file_kind=DATA_KIND_PRE,
        creation_reason=ds_messages_pb.DS_CR_SYSTEM_REQUESTED,
        type=ds_messages_pb.DS_S3_BUCKET,
        uri=s3_uri,
        credential_id=credential_id,
        format=data_format,
        file_time_range=file_time_range
    )
    return ds_pb.LoadDataRequest(data_source_info=load_data_info)


def build_materialize_request(
    column_names: List[str],
    project_id: str,
    data_collection_id: str,
    model_id: str,
    *,
    id_column_name: str = DEFAULT_ID_COLUMN_NAME,
    rowset_id: str = None,
    existing_split_id: str = None,
    new_split_name: str = None,
    score_type: QuantityOfInterest = None,
    approx_max_rows: int = DEFAULT_MAX_ROWS_PER_INGESTION,
    split_type: str = DEFAULT_MATERIALIZE_SPLIT_TYPE
) -> ds_pb.MaterializeDataRequest:
    if id_column_name in column_names:
        column_names.remove(id_column_name)

    projections = [
        create_materialized_output_file(
            ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
            MFT_PRETRANSFORM,
            column_names=[
                EVENT_ID_COLUMN_NAME, TIMESTAMP_COLUMN_NAME, id_column_name,
                *column_names
            ]
        ),
        create_materialized_output_file(
            ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
            MFT_PREDICTIONCACHE,
            column_names=[OUTPUT_COLUMN_NAME]
        )
    ]

    create_cache_info = ds_messages_pb.CreateCacheInfo(
        model_id=model_id, score_type=score_type
    )

    data_info = ds_messages_pb.MaterializeDataInfo(
        project_id=project_id,
        output_data_collection_id=data_collection_id,
        cache_info=create_cache_info,
        system_columns=ds_messages_pb.SystemColumnDetails(
            id_columns=[ColumnDetails(name=id_column_name)],
            timestamp_column=ColumnDetails(name=TIMESTAMP_COLUMN_NAME)
        ),
        projections=projections
    )

    if existing_split_id is not None:
        data_info.existing_split_id.CopyFrom(existing_split_id)
    elif new_split_name is not None:
        data_info.create_split_info.CopyFrom(
            ds_messages_pb.CreateSplitInfo(
                output_split_name=new_split_name,
                output_split_type=split_type,
                output_split_mode=SplitMode.SPLIT_MODE_DATA_REQUIRED
            )
        )
    else:
        raise ValueError("Expecting either existing_split_id or new_split_name")

    return ds_pb.MaterializeDataRequest(
        rowset_id=rowset_id,
        sample_strategy=ds_messages_pb.SAMPLE_FIRST_N,
        approx_max_rows=approx_max_rows,
        data_info=data_info
    )


def ingest_logs_as_split(
    tru: TrueraWorkspace,
    split_name: str,
    datacapture_uri: str,
    credential_id: str,
    *,
    time_range: TimeRange = None,
    max_rows: int = DEFAULT_MAX_ROWS_PER_INGESTION,
    id_column_name: str = DEFAULT_ID_COLUMN_NAME,
    asynchronous: bool = False,
    column_names: List[str] = None,
    column_data_types: List[StaticDataTypeEnum] = None
) -> str:
    project_id = tru.current_tru.project.id
    model_id = tru.current_tru.model.model_id
    data_collection_id = tru.current_tru.data_collection.id
    score_type = tru.current_tru.artifact_interaction_client.get_project_metadata(
        project_name=tru._get_current_active_project_name(), as_json=False
    ).settings.score_type

    column_details = get_column_details_for_parsing(
        tru, column_names=column_names, column_data_types=column_data_types
    )

    time_range = time_range or get_default_time_range()

    ingestion_client = tru.get_ingestion_client()
    ds_communicator = ingestion_client._data_service_client.communicator

    load_request = build_datacapture_load_request(
        column_details=column_details,
        s3_uri=datacapture_uri,
        credential_id=credential_id,
        project_id=project_id,
        data_collection_id=data_collection_id,
        file_time_range=time_range
    )
    rowset_id = ds_communicator.load_data_source(load_request).rowset_id
    materialize_request = build_materialize_request(
        column_names=[c.name for c in column_details],
        project_id=project_id,
        data_collection_id=data_collection_id,
        model_id=model_id,
        rowset_id=rowset_id,
        id_column_name=id_column_name,
        approx_max_rows=max_rows,
        new_split_name=split_name,
        score_type=score_type
    )
    materialize_operation_id = ds_communicator.materialize_data(
        materialize_request
    ).materialize_operation_id
    if not asynchronous:
        tru.logger.info("Waiting for ingestion to complete...")
        ingestion_client._wait_for_materialize_operation(
            materialize_operation_id=materialize_operation_id
        )
        tru.logger.info("Ingestion complete.")
    return materialize_operation_id


def get_default_time_range(delta_min=60, offset_min=0):
    """Returns time range spanning the previous hour. 
    Set delta_min to increase the window of time. Set offset_min to offset backwards in time."""
    now = Timestamp()
    now.GetCurrentTime()
    now.FromSeconds(now.ToSeconds() - offset_min * 60)
    start = Timestamp()
    start.FromSeconds(now.ToSeconds() - delta_min * 60)
    return TimeRange(begin=start, end=now)


def get_column_details_for_parsing(
    tru: TrueraWorkspace,
    column_names: List[str] = None,
    column_data_types: List[StaticDataTypeEnum] = None,
    data_kind: DataKindDescribed = DEFAULT_SCHEMA_DATA_KIND
) -> List[ColumnDetails]:
    """Returns column details that are used for parsing."""

    if column_names:
        if column_data_types is None:
            tru.logger.warning(
                "column_data_types not specified, columns will be parsed as strings"
            )
            column_data_types = [None] * len(column_names)
        if len(column_data_types) != len(column_names):
            raise ValueError(
                "Length of column_data_types needs to be the same as the length of column_names"
            )
        return [
            ColumnDetails(
                name=name, data_type=DataType(static_data_type=dtype)
            ) for name, dtype in zip(column_names, column_data_types)
        ]

    # Column details not provided, retrieve from data collection metadata
    data_collection_schemas = tru.current_tru.ar_client.get_data_collection_metadata(
        project_id=tru.current_tru.project.id,
        data_collection_id=tru.current_tru.data_collection.id
    ).schemas
    for schema in data_collection_schemas:
        if schema.describes_file == data_kind:
            return tru.current_tru.data_service_client.get_schema(
                schema.schema_id_for_parsing
            ).column_details

    raise ValueError(
        f"Data collection '{tru.current_tru.data_collection.name}' does not have a schema. Please ingest a split first or manually specify column_names and optionally column_data_types"
    )
