from __future__ import annotations

import logging
from typing import Optional, Sequence, Union

from truera.client.client_utils import get_qoi_from_string
from truera.client.errors import NotFoundError
from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.configuration_service_http_communicator import \
    HttpConfigurationServiceCommunicator
from truera.protobuf.aiq.config_pb2 import \
    AnalyticsConfig  # pylint: disable=no-name-in-module
from truera.protobuf.configuration import configuration_service_pb2 as cs_pb
from truera.protobuf.public.aiq.accuracy_pb2 import \
    AccuracyType  # pylint: disable=no-name-in-module


class ConfigurationServiceClient(object):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails = None,
        logger=None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if (not use_http):
            from truera.client.private.communicator.configuration_service_grpc_communicator import \
                GrpcConfigurationServiceCommunicator
        self.logger = logger or logging.getLogger(__name__)
        self.auth_details = auth_details
        self.communicator = HttpConfigurationServiceCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        ) if use_http else GrpcConfigurationServiceCommunicator(
            connection_string, auth_details, logger
        )

    def _get_analytics_configuration(
        self, project_id: str
    ) -> cs_pb.GetAnalyticsConfigurationResponse:
        request = cs_pb.GetAnalyticsConfigurationRequest()
        request.project_id = project_id
        return self.communicator.get_analytics_configuration(request)

    def get_num_default_influences(self, project_id: str) -> int:
        ret = self._get_analytics_configuration(project_id)
        return ret.analytics_config.num_bulk_instances

    def get_num_internal_qii_samples(self, project_id: str) -> int:
        ret = self._get_analytics_configuration(project_id)
        return ret.analytics_config.num_samples

    def get_influence_algorithm_type(self, project_id: str) -> str:
        ret = self._get_analytics_configuration(project_id)
        if ret.analytics_config.algorithm_type == AnalyticsConfig.AlgorithmType.TRUERA_QII:
            return "truera-qii"
        elif ret.analytics_config.algorithm_type == AnalyticsConfig.AlgorithmType.INTEGRATED_GRADIENTS:
            return "integrated-gradients"
        else:
            return "shap"

    def update_analytics_configuration(
        self,
        project_id: str,
        *,
        num_default_influences: Optional[int] = None,
        num_internal_qii_samples: Optional[int] = None,
        influence_algorithm_type: Optional[AnalyticsConfig.AlgorithmType] = None
    ) -> None:
        get_response = self._get_analytics_configuration(project_id)
        request = cs_pb.UpdateAnalyticsConfigurationRequest()
        request.analytics_config.CopyFrom(get_response.analytics_config)
        if num_default_influences is not None:
            request.analytics_config.num_bulk_instances = num_default_influences  # pylint: disable=protobuf-type-error
        if num_internal_qii_samples is not None:
            request.analytics_config.num_samples = num_internal_qii_samples  # pylint: disable=protobuf-type-error
        if influence_algorithm_type is not None:
            request.analytics_config.algorithm_type = influence_algorithm_type  # pylint: disable=protobuf-type-error
        self.communicator.update_analytics_configuration(request)

    def get_metric_configuration(
        self, project_id: str
    ) -> cs_pb.GetMetricConfigurationResponse:
        get_request = cs_pb.GetMetricConfigurationRequest()
        get_request.project_id = project_id
        return self.communicator.get_metric_configuration(get_request)

    def get_default_performance_metrics(
        self, project_id: str
    ) -> Sequence[AccuracyType.Type]:
        return self.get_metric_configuration(
            project_id
        ).metric_configuration.accuracy_type

    def update_metric_configuration(
        self,
        project_id: str,
        *,
        score_type: Optional[str] = None,
        maximum_model_runner_failure_rate: Optional[float] = None,
        performance_metrics: Optional[Sequence[AccuracyType.Type]] = None
    ) -> None:
        get_response = self.get_metric_configuration(project_id)
        request = cs_pb.UpdateMetricConfigurationRequest()
        request.metric_configuration.CopyFrom(get_response.metric_configuration)
        if score_type is not None:
            request.metric_configuration.score_type = get_qoi_from_string(
                score_type
            )
        if maximum_model_runner_failure_rate is not None:
            request.metric_configuration.maximum_model_runner_failure_rate = maximum_model_runner_failure_rate  # pylint: disable=protobuf-type-error
        if performance_metrics is not None:
            del request.metric_configuration.accuracy_type[:]
            request.metric_configuration.accuracy_type.extend(
                performance_metrics
            )
        self.communicator.update_metric_configuration(request)

    def get_classification_threshold(
        self,
        project_id: str,
        model_id: str,
        score_type: str,
        infer_threshold_if_not_set: bool = False
    ) -> Optional[float]:
        request = cs_pb.GetClassificationThresholdConfigurationRequest()
        request.model_id.project_id = project_id
        request.model_id.model_id = model_id
        request.score_type = get_qoi_from_string(score_type)
        request.infer_threshold_if_not_set = infer_threshold_if_not_set
        try:
            response = self.communicator.get_classification_threshold_configuration(
                request
            )
            if response.HasField("threshold_config"):
                return response.threshold_config.threshold
            return None
        except NotFoundError:
            return None  # threshold config does not exist

    def update_classification_threshold_configuration(
        self,
        project_id: str,
        model_id: str,
        *,
        classification_threshold: float,
        score_type: str,
    ) -> None:
        request = cs_pb.UpdateClassificationThresholdConfigurationRequest()
        request.threshold_config.model_id.project_id = project_id
        request.threshold_config.model_id.model_id = model_id
        request.threshold_config.threshold = classification_threshold
        request.threshold_config.score_type = get_qoi_from_string(score_type)
        self.communicator.update_classification_threshold_configuration(request)

    def set_base_split(
        self, project_id: str, data_collection_id: str, data_split_id: str
    ) -> None:
        request = cs_pb.SetBaseSplitRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_id=data_split_id
        )
        self.communicator.set_base_split(request)

    def get_base_split(
        self,
        project_id: str,
        data_collection_id: str,
        infer_base_split_if_not_set: bool = False
    ) -> str:
        request = cs_pb.GetBaseSplitRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            infer_base_split_if_not_set=infer_base_split_if_not_set
        )
        return self.communicator.get_base_split(request).split_id
