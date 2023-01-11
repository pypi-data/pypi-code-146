import logging
from typing import Iterator, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.configuration_service_communicator import \
    ConfigurationServiceCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.configuration import configuration_service_pb2 as cs_pb


class HttpConfigurationServiceCommunicator(ConfigurationServiceCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/configservice/configuration"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def get_analytics_configuration(
        self, req: cs_pb.GetAnalyticsConfigurationRequest
    ) -> Iterator[cs_pb.GetAnalyticsConfigurationResponse]:
        uri = f"{self.connection_string}/{req.project_id}/get_analytics_configuration"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.GetAnalyticsConfigurationResponse()
        )

    def update_analytics_configuration(
        self, req: cs_pb.UpdateAnalyticsConfigurationRequest
    ) -> Iterator[cs_pb.UpdateAnalyticsConfigurationResponse]:
        uri = f"{self.connection_string}/{req.analytics_config.project_id}/update_analytics_configuration"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.UpdateAnalyticsConfigurationResponse()
        )

    def get_metric_configuration(
        self, req: cs_pb.GetMetricConfigurationRequest
    ) -> Iterator[cs_pb.GetMetricConfigurationResponse]:
        uri = f"{self.connection_string}/{req.project_id}/get_metric_configuration"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.GetMetricConfigurationResponse()
        )

    def update_metric_configuration(
        self, req: cs_pb.UpdateMetricConfigurationRequest
    ) -> Iterator[cs_pb.UpdateMetricConfigurationResponse]:
        uri = f"{self.connection_string}/{req.metric_configuration.project_id}/update_metric_configuration"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.UpdateMetricConfigurationResponse()
        )

    def get_classification_threshold_configuration(
        self, req: cs_pb.GetClassificationThresholdConfigurationRequest
    ) -> Iterator[cs_pb.GetClassificationThresholdConfigurationResponse]:
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/get_classification_threshold_configuration"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.GetClassificationThresholdConfigurationResponse()
        )

    def update_classification_threshold_configuration(
        self, req: cs_pb.UpdateClassificationThresholdConfigurationRequest
    ) -> Iterator[cs_pb.UpdateClassificationThresholdConfigurationResponse]:
        uri = f"{self.connection_string}/{req.threshold_config.model_id.project_id}/model/{req.threshold_config.model_id.model_id}/update_classification_threshold_configuration"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp,
            cs_pb.UpdateClassificationThresholdConfigurationResponse()
        )

    def set_base_split(
        self, req: cs_pb.SetBaseSplitRequest
    ) -> Iterator[cs_pb.SetBaseSplitRequestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/split/{req.split_id}/set_base_split"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.SetBaseSplitRequestResponse()
        )

    def get_base_split(
        self, req: cs_pb.GetBaseSplitRequest
    ) -> Iterator[cs_pb.GetBaseSplitRequestResponse]:
        uri = f"{self.connection_string}/{req.project_id}/data_collection/{req.data_collection_id}/get_base_split"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, cs_pb.GetBaseSplitRequestResponse()
        )
