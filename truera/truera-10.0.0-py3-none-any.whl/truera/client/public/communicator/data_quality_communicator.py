from abc import ABC
from abc import abstractmethod
from typing import Iterator

from truera.protobuf.dataquality import dataquality_service_pb2 as dq_pb


class DataQualityCommunicator(ABC):

    @abstractmethod
    def get_split_rule_evaluation_results(
        self, req: dq_pb.GetSplitRuleEvaluationResultsRequest
    ) -> Iterator[dq_pb.GetSplitRuleEvaluationResultsResponse]:
        pass

    @abstractmethod
    def get_all_rule_definitions(
        self, req: dq_pb.GetAllRuleDefinitionsRequest
    ) -> Iterator[dq_pb.GetAllRuleDefinitionsResponse]:
        pass

    @abstractmethod
    def update_metric_definition(
        self, req: dq_pb.UpdateMetricDefinitionRequest
    ) -> Iterator[dq_pb.UpdateMetricDefinitionResponse]:
        pass

    @abstractmethod
    def update_rule_definition(
        self, req: dq_pb.UpdateRuleDefinitionRequest
    ) -> Iterator[dq_pb.UpdateRuleDefinitionResponse]:
        pass

    @abstractmethod
    def generate_rule_definition_from_split(
        self, req: dq_pb.GenerateRuleDefinitionFromSplitRequest
    ) -> Iterator[dq_pb.GenerateRuleDefinitionFromSplitResponse]:
        pass

    @abstractmethod
    def check_rule_definition_exists(
        self, req: dq_pb.CheckRuleDefinitionExistsRequest
    ) -> Iterator[dq_pb.CheckRuleDefinitionExistsResponse]:
        pass
