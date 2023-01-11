import logging
from typing import Iterator, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.client.public.communicator.model_test_communicator import \
    ModelTestCommunicator
from truera.protobuf.public.modeltest import modeltest_service_pb2


class HttpModelTestCommunicator(ModelTestCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/testservice/modeltest"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def create_tests_from_split(
        self, req: modeltest_service_pb2.CreateTestsFromSplitRequest
    ) -> Iterator[modeltest_service_pb2.CreateTestsFromSplitResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_split/{req.split_id}/create_tests_from_split"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.CreateTestsFromSplitResponse()
        )

    def start_test_creation_workflow(
        self, req: modeltest_service_pb2.StartTestCreationWorkflowRequest
    ) -> Iterator[modeltest_service_pb2.StartTestCreationWorkflowResponse]:
        uri = f"{self.connection_string}/{req.test_creation_request.project_id}/data_split/{req.test_creation_request.split_id}/start_test_creation_workflow"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.StartTestCreationWorkflowResponse()
        )

    def create_performance_test(
        self, req: modeltest_service_pb2.CreatePerformanceTestRequest
    ) -> Iterator[modeltest_service_pb2.CreatePerformanceTestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_split/{req.split_id}/create_performance_test"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.CreatePerformanceTestResponse()
        )

    def create_performance_test_group(
        self, req: modeltest_service_pb2.CreatePerformanceTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreatePerformanceTestGroupResponse]:
        uri = f"{self.connection_string}/create_performance_test_group"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp,
            modeltest_service_pb2.CreatePerformanceTestGroupResponse()
        )

    def create_fairness_test(
        self, req: modeltest_service_pb2.CreateFairnessTestRequest
    ) -> Iterator[modeltest_service_pb2.CreateFairnessTestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_split/{req.split_id}/create_fairness_test"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.CreateFairnessTestResponse()
        )

    def create_fairness_test_group(
        self, req: modeltest_service_pb2.CreateFairnessTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreateFairnessTestGroupResponse]:
        uri = f"{self.connection_string}/create_fairness_test_group"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.CreateFairnessTestGroupResponse()
        )

    def create_stability_test(
        self, req: modeltest_service_pb2.CreateStabilityTestRequest
    ) -> Iterator[modeltest_service_pb2.CreateStabilityTestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_split/{req.split_id}/create_stability_test"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.CreateStabilityTestResponse()
        )

    def create_stability_test_group(
        self, req: modeltest_service_pb2.CreateStabilityTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreateStabilityTestGroupResponse]:
        uri = f"{self.connection_string}/create_stability_test_group"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.CreateStabilityTestGroupResponse()
        )

    def create_feature_importance_test(
        self, req: modeltest_service_pb2.CreateFeatureImportanceTestRequest
    ) -> Iterator[modeltest_service_pb2.CreateFeatureImportanceTestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_split/{req.split_id}/create_feature_importance_test"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp,
            modeltest_service_pb2.CreateFeatureImportanceTestResponse()
        )

    def create_feature_importance_test_group(
        self, req: modeltest_service_pb2.CreateFeatureImportanceTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreateFeatureImportanceTestGroupResponse
                 ]:
        uri = f"{self.connection_string}/create_feature_importance_test_group"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp,
            modeltest_service_pb2.CreateFeatureImportanceTestGroupResponse()
        )

    def delete_model_test(
        self, req: modeltest_service_pb2.DeleteModelTestRequest
    ) -> Iterator[modeltest_service_pb2.DeleteModelTestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/test_id/{req.test_id}/delete_model_test"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.DeleteModelTestResponse()
        )

    def delete_model_test_group(
        self, req: modeltest_service_pb2.DeleteModelTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.DeleteModelTestGroupResponse]:
        uri = f"{self.connection_string}/{req.project_id}/test_group_id/{req.test_group_id}/delete_model_test_group"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.DeleteModelTestGroupResponse()
        )

    def delete_model_test_for_split(
        self, req: modeltest_service_pb2.DeleteModelTestsForSplitRequest
    ) -> Iterator[modeltest_service_pb2.DeleteModelTestsForSplitResponse]:
        uri = f"{self.connection_string}/{req.project_id}/split_id/{req.split_id}/delete_model_test_for_split"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.DeleteModelTestsForSplitResponse()
        )

    def get_model_tests(
        self, req: modeltest_service_pb2.GetModelTestsRequest
    ) -> Iterator[modeltest_service_pb2.GetModelTestsResponse]:
        uri = f"{self.connection_string}/{req.project_id}/get_model_tests"
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
            json_resp_arr, modeltest_service_pb2.GetModelTestsResponse()
        )

    def get_model_test_groups(
        self, req: modeltest_service_pb2.GetModelTestGroupsRequest
    ) -> Iterator[modeltest_service_pb2.GetModelTestGroupsResponse]:
        uri = f"{self.connection_string}/{req.project_id}/get_model_test_groups"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.GetModelTestGroupsResponse()
        )

    def get_test_results_for_model(
        self, req: modeltest_service_pb2.GetTestResultsForModelRequest
    ) -> Iterator[modeltest_service_pb2.GetTestResultsForModelResponse]:
        uri = f"{self.connection_string}/{req.project_id}/model_id/{req.model_id}/get_test_results_for_model"
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
            json_resp_arr,
            modeltest_service_pb2.GetTestResultsForModelResponse()
        )

    def get_data_splits_from_regex(
        self, req: modeltest_service_pb2.GetDataSplitsFromRegexRequest
    ) -> Iterator[modeltest_service_pb2.GetDataSplitsFromRegexResponse]:
        uri = f"{self.connection_string}/{req.project_id}/get_data_splits_from_regex"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, modeltest_service_pb2.GetDataSplitsFromRegexResponse()
        )
