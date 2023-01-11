from abc import ABC
from abc import abstractmethod
from typing import Iterator

from truera.protobuf.configuration import configuration_service_pb2 as cs_pb


class ConfigurationServiceCommunicator(ABC):

    @abstractmethod
    def get_analytics_configuration(
        self, req: cs_pb.GetAnalyticsConfigurationRequest
    ) -> Iterator[cs_pb.GetAnalyticsConfigurationResponse]:
        pass

    @abstractmethod
    def update_analytics_configuration(
        self, req: cs_pb.UpdateAnalyticsConfigurationRequest
    ) -> Iterator[cs_pb.UpdateAnalyticsConfigurationResponse]:
        pass

    @abstractmethod
    def get_metric_configuration(
        self, req: cs_pb.GetMetricConfigurationRequest
    ) -> Iterator[cs_pb.GetMetricConfigurationResponse]:
        pass

    @abstractmethod
    def update_metric_configuration(
        self, req: cs_pb.UpdateMetricConfigurationRequest
    ) -> Iterator[cs_pb.UpdateMetricConfigurationResponse]:
        pass

    @abstractmethod
    def get_classification_threshold_configuration(
        self, req: cs_pb.GetClassificationThresholdConfigurationRequest
    ) -> Iterator[cs_pb.GetClassificationThresholdConfigurationResponse]:
        pass

    @abstractmethod
    def update_classification_threshold_configuration(
        self, req: cs_pb.UpdateClassificationThresholdConfigurationRequest
    ) -> Iterator[cs_pb.UpdateClassificationThresholdConfigurationResponse]:
        pass

    @abstractmethod
    def set_base_split(
        self, req: cs_pb.SetBaseSplitRequest
    ) -> Iterator[cs_pb.SetBaseSplitRequestResponse]:
        pass

    @abstractmethod
    def get_base_split(
        self, req: cs_pb.GetBaseSplitRequest
    ) -> Iterator[cs_pb.GetBaseSplitRequestResponse]:
        pass
