import itertools
import json
import logging
from typing import Generator, Iterator, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.artifactrepo_communicator import \
    ArtifactRepoCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.public import artifactrepo_pb2 as ar_pb
from truera.protobuf.public.data_service import data_service_pb2 as ds_pb

_MAX_SIZE_TO_POST = 16 * 1024


class HttpArtifactRepoCommunicator(ArtifactRepoCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/artifacts/artifactrepo"
        self.http_communicator = HttpCommunicator(
            connection_string=connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def ping(self, req: ar_pb.PingRequest) -> ar_pb.PingRequestResponse:
        uri = "{conn}/Ping/{text}".format(
            conn=self.connection_string, text=req.test_string
        )
        json_resp = self.http_communicator.get_request(uri, None)
        try:
            json.loads(json_resp)
        except:
            raise ConnectionError(
                f"Failed to connect! Provided connection string: {uri}"
            )
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.PingRequestResponse()
        )

    def put_resource(
        self,
        req_gen: Generator[ar_pb.PutRequest, None, None],
        stream=False
    ) -> ar_pb.PutRequestResponse:
        peeker, reqs = itertools.tee(req_gen)
        # peek at the first element without pulling it out of the requests to be sent.
        r = next(peeker)
        if not r:
            raise ValueError("At least one element expected.")
        uri = f"{self.connection_string}/Resource"

        def data_generator(protos):
            first = True
            for proto in protos:
                encoded = b''
                if first:
                    encoded += "[".encode()
                    first = False
                encoded += self.http_communicator._proto_to_json(proto).encode()
                encoded += ",".encode()
                for i in range(0, len(encoded), _MAX_SIZE_TO_POST):
                    yield encoded[i:(i + _MAX_SIZE_TO_POST)]
            yield "]".encode()

        if stream:
            json_resp = []
            with self.http_communicator.post_request(
                uri, json_data_or_generator=data_generator(reqs), stream=True
            ) as response:
                self.http_communicator._handle_response(response)
                response.encoding = "UTF-8"
                for body in response.iter_lines(decode_unicode=True):
                    json_resp.append(body)
            json_resp = "".join(json_resp)
        else:
            json_resp = self.http_communicator.post_request(
                uri, json_data_or_generator=data_generator(reqs), stream=False
            )
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.PutRequestResponse()
        )

    def put_metadata(
        self, req: ar_pb.PutMetadataRequest
    ) -> ar_pb.PutMetadataRequestResponse:
        uri = f"{self.connection_string}/Metadata"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(
            uri, json_data_or_generator=json_req
        )
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.PutMetadataRequestResponse()
        )

    def resource_exists(
        self, req: ar_pb.ExistsRequest
    ) -> ar_pb.ExistsRequestResponse:
        uri = f"{self.connection_string}/Resource/{req.project_id}/{ar_pb.ArtifactType.Name(req.artifact_type)}/{req.artifact_id}:exists"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.ExistsRequestResponse()
        )

    def get_resource(
        self, req: ar_pb.GetRequest
    ) -> Iterator[ar_pb.GetRequestResponse]:
        uri = f"{self.connection_string}/Resource/{req.project_id}/{ar_pb.ArtifactType.Name(req.artifact_type)}/{req.artifact_id}"
        json_req = self.http_communicator._proto_to_json(req)
        with self.http_communicator.get_request(
            uri, json_data_or_generator=json_req, stream=True
        ) as response:
            self.http_communicator._handle_response(response)
            response.encoding = "UTF-8"
            for body in response.json():
                yield self.http_communicator._json_to_proto(
                    json.dumps(body), ar_pb.GetRequestResponse()
                )

    def get_metadata_for_entity(
        self, req: ar_pb.GetMetadataForEntityRequest
    ) -> ar_pb.GetMetadataForEntityRequestResponse:
        uri = f"{self.connection_string}/Metadata/{req.project_id}/{ar_pb.ArtifactType.Name(req.artifact_type)}"
        if req.entity_name:
            uri = f"{uri}/name/{req.entity_name}"
        elif req.entity_id:
            uri = f"{uri}/id/{req.entity_id}"
        else:
            raise ValueError(
                "TruEra internal error: Expected at least one of entity name or id"
            )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.GetMetadataForEntityRequestResponse()
        )

    def get_all_metadata_for_resource(
        self, req: ar_pb.GetAllMetadataRequest
    ) -> ar_pb.GetAllMetadataRequestResponse:
        uri = f"{self.connection_string}/Metadata/{req.project_id}/{ar_pb.ArtifactType.Name(req.artifact_type)}"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.GetAllMetadataRequestResponse()
        )

    def delete_resource(self, req: ar_pb.DeleteRequest) -> None:
        uri = f"{self.connection_string}/Resource/{req.project_id}/{ar_pb.ArtifactType.Name(req.artifact_type)}/{req.artifact_id}"
        json_req = self.http_communicator._proto_to_json(req)
        self.http_communicator.delete_request(uri, json_req)

    def delete_metadata(
        self, req: ar_pb.DeleteMetadataRequest
    ) -> ar_pb.DeleteMetadataRequestResponse:
        uri = f"{self.connection_string}/Metadata/{req.project_id}/{ar_pb.ArtifactType.Name(req.artifact_type)}"
        if req.entity_name:
            uri = f"{uri}/name/{req.entity_name}"
        elif req.entity_id:
            uri = f"{uri}/id/{req.entity_id}"
        else:
            raise ValueError(
                "TruEra internal error: Expected at least one of entity name or id"
            )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.DeleteMetadataRequestResponse()
        )

    def get_models(
        self, req: ar_pb.GetModelsRequest
    ) -> ar_pb.GetModelsResponse:
        uri = f"{self.connection_string}/Resource/{req.project_id}/model"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.GetModelsResponse()
        )

    def get_splits(
        self, req: ar_pb.GetSplitsRequest
    ) -> ar_pb.GetSplitsResponse:
        uri = f"{self.connection_string}/Resource/{req.project_id}/split"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ar_pb.GetSplitsResponse()
        )

    def close(self):
        self.http_communicator.close()
