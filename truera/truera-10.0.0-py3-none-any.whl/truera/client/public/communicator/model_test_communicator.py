from abc import ABC
from abc import abstractmethod
from typing import Iterator

from truera.protobuf.public.modeltest import modeltest_service_pb2


class ModelTestCommunicator(ABC):

    @abstractmethod
    def create_tests_from_split(
        self, req: modeltest_service_pb2.CreateTestsFromSplitRequest
    ) -> Iterator[modeltest_service_pb2.CreateTestsFromSplitResponse]:
        pass

    @abstractmethod
    def start_test_creation_workflow(
        self, req: modeltest_service_pb2.StartTestCreationWorkflowRequest
    ) -> Iterator[modeltest_service_pb2.StartTestCreationWorkflowResponse]:
        pass

    @abstractmethod
    def create_performance_test(
        self, req: modeltest_service_pb2.CreatePerformanceTestRequest
    ) -> Iterator[modeltest_service_pb2.CreatePerformanceTestResponse]:
        pass

    @abstractmethod
    def create_performance_test_group(
        self, req: modeltest_service_pb2.CreatePerformanceTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreatePerformanceTestGroupResponse]:
        pass

    @abstractmethod
    def create_fairness_test(
        self, req: modeltest_service_pb2.CreateFairnessTestRequest
    ) -> Iterator[modeltest_service_pb2.CreateFairnessTestResponse]:
        pass

    @abstractmethod
    def create_fairness_test_group(
        self, req: modeltest_service_pb2.CreateFairnessTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreateFairnessTestGroupResponse]:
        pass

    @abstractmethod
    def create_stability_test(
        self, req: modeltest_service_pb2.CreateStabilityTestRequest
    ) -> Iterator[modeltest_service_pb2.CreateStabilityTestResponse]:
        pass

    @abstractmethod
    def create_stability_test_group(
        self, req: modeltest_service_pb2.CreateStabilityTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreateStabilityTestGroupResponse]:
        pass

    @abstractmethod
    def create_feature_importance_test(
        self, req: modeltest_service_pb2.CreateFeatureImportanceTestRequest
    ) -> Iterator[modeltest_service_pb2.CreateFeatureImportanceTestResponse]:
        pass

    @abstractmethod
    def create_feature_importance_test_group(
        self, req: modeltest_service_pb2.CreateFeatureImportanceTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.CreateFeatureImportanceTestGroupResponse
                 ]:
        pass

    @abstractmethod
    def delete_model_test(
        self, req: modeltest_service_pb2.DeleteModelTestRequest
    ) -> Iterator[modeltest_service_pb2.DeleteModelTestResponse]:
        pass

    @abstractmethod
    def delete_model_test_group(
        self, req: modeltest_service_pb2.DeleteModelTestGroupRequest
    ) -> Iterator[modeltest_service_pb2.DeleteModelTestGroupResponse]:
        pass

    @abstractmethod
    def get_model_tests(
        self, req: modeltest_service_pb2.GetModelTestsRequest
    ) -> Iterator[modeltest_service_pb2.GetModelTestsResponse]:
        pass

    @abstractmethod
    def get_model_test_groups(
        self, req: modeltest_service_pb2.GetModelTestGroupsRequest
    ) -> Iterator[modeltest_service_pb2.GetModelTestGroupsResponse]:
        pass

    @abstractmethod
    def delete_model_test_for_split(
        self, req: modeltest_service_pb2.DeleteModelTestsForSplitRequest
    ) -> Iterator[modeltest_service_pb2.DeleteModelTestsForSplitResponse]:
        pass

    @abstractmethod
    def get_test_results_for_model(
        self, req: modeltest_service_pb2.GetTestResultsForModelRequest
    ) -> Iterator[modeltest_service_pb2.GetTestResultsForModelResponse]:
        pass

    @abstractmethod
    def get_data_splits_from_regex(
        self, req: modeltest_service_pb2.GetDataSplitsFromRegexRequest
    ) -> Iterator[modeltest_service_pb2.GetDataSplitsFromRegexResponse]:
        pass
