import logging
from typing import Iterator, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.data_quality_communicator import \
    DataQualityCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.dataquality import dataquality_service_pb2 as dq_pb


class HttpDataQualityCommunicator(DataQualityCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/dataquality/dataquality"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def get_split_rule_evaluation_results(
        self, req: dq_pb.GetSplitRuleEvaluationResultsRequest
    ) -> Iterator[dq_pb.GetSplitRuleEvaluationResultsResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/get_split_rule_evaluation_results"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp_arr = []
        with self.http_communicator.get_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.iter_lines(decode_unicode=True):
                json_resp_arr.append(body)
        json_resp_arr = "".join(json_resp_arr)
        return self.http_communicator._json_to_proto(
            json_resp_arr, dq_pb.GetSplitRuleEvaluationResultsResponse()
        )

    def get_all_rule_definitions(
        self, req: dq_pb.GetAllRuleDefinitionsRequest
    ) -> Iterator[dq_pb.GetAllRuleDefinitionsResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/get_all_rule_definitions"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp_arr = []
        with self.http_communicator.get_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.iter_lines(decode_unicode=True):
                json_resp_arr.append(body)
        json_resp_arr = "".join(json_resp_arr)
        return self.http_communicator._json_to_proto(
            json_resp_arr, dq_pb.GetAllRuleDefinitionsResponse()
        )

    def update_metric_definition(
        self, req: dq_pb.UpdateMetricDefinitionRequest
    ) -> Iterator[dq_pb.UpdateMetricDefinitionResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/rule_id/{req.rule_id}/metric_id/{req.metric_id}/update_metric_definition"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, dq_pb.UpdateMetricDefinitionResponse()
        )

    def update_rule_definition(
        self, req: dq_pb.UpdateRuleDefinitionRequest
    ) -> Iterator[dq_pb.UpdateRuleDefinitionResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/rule_id/{req.rule_id}/update_rule_definition"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, dq_pb.UpdateRuleDefinitionResponse()
        )

    def generate_rule_definition_from_split(
        self, req: dq_pb.GenerateRuleDefinitionFromSplitRequest
    ) -> Iterator[dq_pb.GenerateRuleDefinitionFromSplitResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/split_id/{req.split_id}/overwrite_existing/{req.overwrite_existing_rule}/generate_rule_from_split"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, dq_pb.GenerateRuleDefinitionFromSplitResponse()
        )

    def check_rule_definition_exists(
        self, req: dq_pb.CheckRuleDefinitionExistsRequest
    ) -> Iterator[dq_pb.CheckRuleDefinitionExistsResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/check_rule_definition_exists"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, dq_pb.CheckRuleDefinitionExistsResponse()
        )
