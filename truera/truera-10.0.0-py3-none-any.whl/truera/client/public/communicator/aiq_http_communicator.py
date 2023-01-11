import json
import logging
from typing import Iterator, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.aiq_communicator import AiqCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.public.aiq import intelligence_service_pb2 as is_pb
from truera.protobuf.public.artifactrepo_pb2 import \
    PingRequest  # pylint: disable=no-name-in-module
from truera.protobuf.public.artifactrepo_pb2 import \
    PingRequestResponse  # pylint: disable=no-name-in-module


class HttpAiqCommunicator(AiqCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/intelligence/aiq"
        self.http_communicator = HttpCommunicator(
            connection_string=connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def ping(self, req: PingRequest) -> Iterator[PingRequestResponse]:
        uri = f"{self.connection_string}/ping/{req.test_string}"
        json_resp = self.http_communicator.get_request(uri, None)
        return self.http_communicator._json_to_proto(
            json_resp, PingRequestResponse()
        )

    def get_model_predictions(
        self, req: is_pb.ModelPredictionsRequest
    ) -> Iterator[is_pb.ModelPredictionsResponse]:
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/predictions"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp_arr = []
        with self.http_communicator.post_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.iter_lines(decode_unicode=True):
                json_resp_arr.append(body)
        json_resp_arr = "".join(json_resp_arr)
        return self.http_communicator._json_to_proto(
            json_resp_arr, is_pb.ModelPredictionsResponse()
        )

    def get_model_influences(
        self, req: is_pb.ModelInfluencesRequest
    ) -> Iterator[is_pb.ModelInfluencesResponse]:
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/influences"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp_arr = []
        with self.http_communicator.post_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.iter_lines(decode_unicode=True):
                json_resp_arr.append(body)
        json_resp_arr = "".join(json_resp_arr)
        return self.http_communicator._json_to_proto(
            json_resp_arr, is_pb.ModelInfluencesResponse()
        )

    def get_model_data(
        self, req: is_pb.ModelDataRequest
    ) -> Iterator[is_pb.ModelDataResponse]:
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/model_data"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.ModelDataResponse()
        )

    def get_partial_dependence_plot(
        self,
        req: is_pb.PartialDependencePlotRequest,
    ) -> Iterator[is_pb.PartialDependencePlotResponse]:
        # TODO(davidkurokawa): refactor all these streaming ones together.
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/partial_dependence_plot"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp_arr = []
        with self.http_communicator.post_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.iter_lines(decode_unicode=True):
                json_resp_arr.append(body)
        json_resp_arr = "".join(json_resp_arr)
        return self.http_communicator._json_to_proto(
            json_resp_arr, is_pb.PartialDependencePlotResponse()
        )

    def get_split_data(
        self, req: is_pb.SplitDataRequest
    ) -> Iterator[is_pb.SplitDataResponse]:
        uri = f"{self.connection_string}/{req.project_id}/split/{req.input_spec.split_id}/split_data"
        json_req = self.http_communicator._proto_to_json(req)
        with self.http_communicator.post_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.json():
                yield self.http_communicator._json_to_proto(
                    json.dumps(body), is_pb.SplitDataResponse()
                )

    def compute_accuracy(
        self, req: is_pb.AccuracyRequest
    ) -> Iterator[is_pb.AccuracyResponse]:
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/accuracy"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.AccuracyResponse()
        )

    def compute_batched_accuracy(
        self, req: is_pb.BatchAccuracyRequest
    ) -> Iterator[is_pb.BatchAccuracyResponse]:
        uri = f"{self.connection_string}/{req.project_id}/batch_accuracies"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.BatchAccuracyResponse()
        )

    def compute_model_score_instability(
        self, req: is_pb.CompareModelOutputRequest
    ) -> Iterator[is_pb.CompareModelOutputResponse]:
        uri = f"{self.connection_string}/{req.output_spec1.model_id.project_id}/model/{req.output_spec1.model_id.model_id}/compare_model_output_distribution"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.CompareModelOutputResponse()
        )

    def batch_compute_model_score_instability(
        self, req: is_pb.BatchCompareModelOutputRequest
    ) -> Iterator[is_pb.BatchCompareModelOutputResponse]:
        uri = f"{self.connection_string}/{req.project_id}/batch_compare_model_output_distribution"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.BatchCompareModelOutputResponse()
        )

    def get_segmentations(
        self, req: is_pb.GetManualSegmentationRequest
    ) -> Iterator[is_pb.GetManualSegmentationResponse]:
        uri = f"{self.connection_string}/{req.project_id}/manual_segmentation"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.GetManualSegmentationResponse()
        )

    def compute_fairness(
        self, req: is_pb.GetModelBiasRequest
    ) -> Iterator[is_pb.GetModelBiasResponse]:
        uri = f"{self.connection_string}/{req.model_id.project_id}/model/{req.model_id.model_id}/model_bias"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.GetModelBiasResponse()
        )

    def batch_compute_fairness(
        self, req: is_pb.GetBatchModelBiasRequest
    ) -> Iterator[is_pb.GetBatchModelBiasResponse]:
        uri = f"{self.connection_string}/{req.project_id}/batch_model_bias"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.GetBatchModelBiasResponse()
        )

    def compute_feature_drift(
        self, req: is_pb.FeatureDriftRequest
    ) -> Iterator[is_pb.FeatureDriftResponse]:
        # return self.invoke_req(self.stub.GetFeatureDrift, req)
        uri = f"{self.connection_string}/split1/{req.input_spec1.split_id}/split2/{req.input_spec2.split_id}/feature_drift"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.FeatureDriftResponse()
        )

    def update_manual_segmentation(
        self, req: is_pb.UpdateManualSegmentationRequest
    ) -> Iterator[is_pb.UpdateManualSegmentationResponse]:
        uri = f"{self.connection_string}/{req.project_id}/manual_segmentation"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.UpdateManualSegmentationResponse()
        )

    def get_interesting_segments(
        self, req: is_pb.InterestingSegmentsRequest
    ) -> Iterator[is_pb.InterestingSegmentsResponse]:
        uri = f"{self.connection_string}/{req.project_id}/interesting_segments"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, is_pb.InterestingSegmentsResponse()
        )
