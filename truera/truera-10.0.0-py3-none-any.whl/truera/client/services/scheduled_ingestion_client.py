from datetime import datetime
import logging
from typing import Union

from crontab import CronTab
from google.protobuf.json_format import Parse
from google.protobuf.timestamp_pb2 import \
    Timestamp  # pylint: disable=no-name-in-module

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.scheduled_ingestion_communicator import \
    ScheduledIngestionServiceCommunicator
from truera.client.public.communicator.scheduled_ingestion_http_communicator import \
    HttpScheduledIngestionServiceCommunicator
import truera.client.services.data_service_client as ds_client
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb
from truera.protobuf.public.data_service import data_service_pb2 as ds_pb
from truera.protobuf.public.scheduled_ingestion_service import \
    scheduled_ingestion_service_pb2 as scheduled_ingestion_pb

_DEFAULT_SCHEDULE = scheduled_ingestion_pb.Schedule(
    schedule=[
        scheduled_ingestion_pb.CronElement(
            repeat_every_value=1,
            type=scheduled_ingestion_pb.CronElementType.TDK_HOUR_OF_DAY
        )
    ]
)


def _datetime_to_timestamp(dt: datetime) -> Timestamp:
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp


class InvalidOperationTreeError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ScheduledIngestionClient():

    def __init__(
        self,
        communicator: ScheduledIngestionServiceCommunicator,
        ds_client: ds_client.DataServiceClient,
        logger=None
    ) -> None:
        self.logger = logger if logger else logging.getLogger(__name__)
        self.communicator = communicator
        self.data_service_client = ds_client

    @classmethod
    def create(
        cls,
        connection_string: str = None,
        data_service_client: ds_client.DataServiceClient = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if use_http:
            communicator = HttpScheduledIngestionServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.scheduled_ingestion_grpc_communicator import \
                GrpcScheduledIngestionServiceCommunicator
            communicator = GrpcScheduledIngestionServiceCommunicator(
                connection_string, auth_details, logger
            )
        return ScheduledIngestionClient(
            communicator, data_service_client, logger
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    def schedule_new(
        self,
        tree: scheduled_ingestion_pb.DataServiceRequestTree = None,
        json: str = None,
        schedule: scheduled_ingestion_pb.Schedule = _DEFAULT_SCHEDULE,
        historical_start_time: datetime = None
    ):
        template = Parse(
            json, scheduled_ingestion_pb.DataServiceRequestTree()
        ) if json is not None else tree

        if not template:
            raise ValueError("Either tree or json required.")

        return self._schedule_ingestion(
            template, schedule, historical_start_time
        ).workflow_id

    def schedule(
        self,
        project_id: str,
        template_operation_id: str,
        append: bool = False,
        schedule: scheduled_ingestion_pb.Schedule = _DEFAULT_SCHEDULE,
        historical_start_time: datetime = None
    ):
        materialize_status = self.data_service_client.get_materialize_data_status(
            project_id, template_operation_id, throw_on_error=False
        )

        self._assert_tree_property(
            condition_to_check=(
                lambda: materialize_status.status == ds_messages_pb.
                MaterializeStatus.MATERIALIZE_STATUS_SUCCEDED
            ),
            condition_text=
            "materialize_status.status == ds_messages_pb.MaterializeStatus.MATERIALIZE_STATUS_SUCCEDED",
            context=f"Operation id: {template_operation_id}"
        )

        existing_split_id = materialize_status.output_split_id if append else None

        request_template = self.build_request_tree(
            materialize_status, project_id, existing_split_id=existing_split_id
        )

        return self._schedule_ingestion(
            request_template, schedule, historical_start_time
        ).workflow_id

    def _schedule_ingestion(
        self,
        request_template: scheduled_ingestion_pb.DataServiceRequestTree,
        schedule: scheduled_ingestion_pb.Schedule = _DEFAULT_SCHEDULE,
        historical_start_time: datetime = None
    ) -> scheduled_ingestion_pb.ScheduleIngestionResponse:
        req = scheduled_ingestion_pb.ScheduleIngestionRequest(
            request_template=request_template,
            schedule=schedule,
            historical_start_time=_datetime_to_timestamp(
                historical_start_time or datetime.utcnow()
            )
        )
        return self.communicator.schedule_ingestion(req)

    def get(self, workflow_id: str):
        req = scheduled_ingestion_pb.GetScheduleRequest(workflow_id=workflow_id)
        return self.communicator.get_schedule(req)

    def get_workflows(
        self,
        project_id: str,
        data_collection_id: str,
        last_key: str = None,
        limit: int = 50,
    ) -> scheduled_ingestion_pb.GetWorkflowsResponse:
        req = scheduled_ingestion_pb.GetWorkflowsRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            last_key=last_key,
            limit=limit,
        )
        return self.communicator.get_workflows(req)

    def cancel(
        self, workflow_id: str
    ) -> scheduled_ingestion_pb.CancelWorkflowResponse:
        req = scheduled_ingestion_pb.CancelWorkflowRequest(
            workflow_id=workflow_id
        )
        return self.communicator.cancel_workflow(req)

    def run_single_ingestion(
        self,
        tree: scheduled_ingestion_pb.DataServiceRequestTree = None
    ) -> scheduled_ingestion_pb.RunSingleIngestionResponse:
        req = scheduled_ingestion_pb.RunSingleIngestionRequest(
            request_template=tree
        )
        return self.communicator.run_single_ingestion(req)

    def run_single_ingestion_sync(
        self,
        tree: scheduled_ingestion_pb.DataServiceRequestTree = None,
    ) -> scheduled_ingestion_pb.RunSingleIngestionSyncResponse:
        req = scheduled_ingestion_pb.RunSingleIngestionSyncRequest(
            request_template=tree
        )
        return self.communicator.run_single_ingestion_sync(req)

    def get_run_status(
        self, workflow_id: str, run_id: str
    ) -> scheduled_ingestion_pb.GetRunStatusResponse:
        req = scheduled_ingestion_pb.GetRunStatusRequest(
            workflow_id=workflow_id, run_id=run_id
        )
        return self.communicator.get_run_status(req)

    def build_request_tree(
        self,
        materialize_status_response: ds_pb.MaterializeDataResponse,
        project_id: str,
        override_split_name: str = None,
        existing_split_id: str = None
    ):
        materialize_rowset_id = materialize_status_response.rowset_id
        parent = self._recurse_build_tree(materialize_rowset_id, project_id)
        data_info = materialize_status_response.original_request.data_info
        if existing_split_id:
            data_info.ClearField("split_info")
            data_info.existing_split_id = existing_split_id
        elif data_info.create_split_info and data_info.create_split_info.output_split_name:
            data_info.create_split_info.output_split_name = override_split_name or data_info.create_split_info.output_split_name + "_${uuid()}"

        req = scheduled_ingestion_pb.DataServiceRequestTree(
            materialize=materialize_status_response.original_request
        )
        req.parents.extend([parent])
        return req

    def _recurse_build_tree(self, rowset_id: str, project_id: str):
        rowset = self.data_service_client.get_rowset_metadata(rowset_id).rowset
        if rowset.op_type == ds_messages_pb.RowsetOperationType.RO_FILTER:
            return self._get_filter_request(rowset, project_id)
        elif rowset.op_type == ds_messages_pb.RowsetOperationType.RO_JOIN:
            return self._get_join_request(rowset, project_id)
        else:
            # NONE -> LOAD, we will assert is_root == true
            return self._get_load_request(rowset, project_id)

    def _get_filter_request(
        self, rowset: ds_messages_pb.Rowset, project_id: str
    ):
        rowset_id = rowset.id
        self._assert_tree_property(
            condition_to_check=(
                lambda: rowset.WhichOneof("operationInfo") == "filter"
            ),
            condition_text="rowset.WhichOneof(\"operationInfo\") == \"filter\"",
            context=f"Rowset id: {rowset.id}"
        )
        self._assert_tree_property(
            condition_to_check=(lambda: len(rowset.immediate_parent_id) == 1),
            condition_text="len(rowset.immediate_parent_id) == 1",
            context=f"Rowset id: {rowset.id}"
        )
        request = ds_pb.ApplyFilterRequest(
            rowset_id=rowset_id, project_id=project_id, filter=rowset.filter
        )

        parents = [
            self._recurse_build_tree(rowset.immediate_parent_id[0], project_id)
        ]
        req = scheduled_ingestion_pb.DataServiceRequestTree(filter=request)
        req.parents.extend(parents)
        return req

    def _get_join_request(self, rowset: ds_messages_pb.Rowset, project_id: str):
        self._assert_tree_property(
            condition_to_check=(
                lambda: rowset.WhichOneof("operationInfo") == "join_details"
            ),
            condition_text=
            "rowset.WhichOneof(\"operationInfo\") == \"join_details\"",
            context=f"Rowset id: {rowset.id}"
        )
        self._assert_tree_property(
            condition_to_check=(lambda: len(rowset.immediate_parent_id) >= 2),
            condition_text="len(rowset.immediate_parent_id) >= 2",
            context=f"Rowset id: {rowset.id}"
        )
        join_details = rowset.join_details
        # note that rowset.immediate_parent_id is a repeated field
        rowset_parents = rowset.immediate_parent_id
        request = ds_pb.JoinRequest(
            rowsets=join_details.join_inputs,
            perform_column_rename=join_details.perform_column_rename,
            join_type=join_details.join_type
        )

        parents = [
            self._recurse_build_tree(parent_id, project_id)
            for parent_id in rowset_parents
        ]
        req = scheduled_ingestion_pb.DataServiceRequestTree(join=request)
        req.parents.extend(parents)
        return req

    def _get_load_request(self, rowset: ds_messages_pb.Rowset, project_id: str):
        self._assert_tree_property(
            condition_to_check=(lambda: rowset.is_root),
            condition_text="rowset.is_root",
            context=f"Rowset id: {rowset.id}"
        )
        self._assert_tree_property(
            condition_to_check=(lambda: len(rowset.immediate_parent_id) == 1),
            condition_text="len(rowset.immediate_parent_id) == 1)",
            context=f"Rowset id: {rowset.id}"
        )
        self._assert_tree_property(
            condition_to_check=(lambda: "" == rowset.immediate_parent_id[0]),
            condition_text="\"\" == rowset.immediate_parent_id[0]",
            context=f"Rowset id: {rowset.id}"
        )
        self._assert_tree_property(
            condition_to_check=(lambda: len(rowset.root_data) == 1),
            condition_text="len(rowset.root_data) == 1)",
            context=f"Rowset id: {rowset.id}"
        )
        request = ds_pb.LoadDataRequest(data_source_info=rowset.root_data[0])

        parents = []

        req = scheduled_ingestion_pb.DataServiceRequestTree(load_req=request)
        req.parents.extend(parents)
        return req

    def _assert_tree_property(
        self, condition_to_check, condition_text, context
    ):
        if not condition_to_check():
            message = f"Provided tree did not conform to expected condition: {condition_text}. Additional context: {context}."
            raise InvalidOperationTreeError(message)

    def serialize_schedule(
        self, cron_schedule: str
    ) -> scheduled_ingestion_pb.Schedule:
        parsed = CronTab(cron_schedule)
        segment_mapping = {
            'minute': scheduled_ingestion_pb.CronElementType.TDK_MINUTE_OF_HOUR,
            'hour': scheduled_ingestion_pb.CronElementType.TDK_HOUR_OF_DAY,
            'day': scheduled_ingestion_pb.CronElementType.TDK_DAY_OF_MONTH,
            'month': scheduled_ingestion_pb.CronElementType.TDK_MONTH_OF_YEAR,
            'weekday': scheduled_ingestion_pb.CronElementType.TDK_DAY_OF_WEEK,
        }
        base = scheduled_ingestion_pb.Schedule()
        for matcher, element_type in segment_mapping.items():
            crontab_matcher = getattr(parsed.matchers, matcher)
            if (crontab_matcher.any):
                continue
            element = scheduled_ingestion_pb.CronElement(
                value=sorted([value for value in crontab_matcher.allowed]),
                type=element_type,
            )
            base.schedule.append(element)

        return base
