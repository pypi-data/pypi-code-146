from ..apis.assoc.v1.assoc_service_pb2 import Assoc
from ..apis.assoc.v1.assoc_service_pb2 import AssocOptionFilter
from ..apis.assoc.v1.assoc_service_pb2 import AssocType
from ..apis.assoc.v1.assoc_service_pb2 import CountAssocsRequest
from ..apis.assoc.v1.assoc_service_pb2 import CountAssocsResponse
from ..apis.assoc.v1.assoc_service_pb2 import CreateAssocRequest
from ..apis.assoc.v1.assoc_service_pb2 import CreateAssocResponse
from ..apis.assoc.v1.assoc_service_pb2 import DeleteAssocRequest
from ..apis.assoc.v1.assoc_service_pb2 import DeleteAssocResponse
from ..apis.assoc.v1.assoc_service_pb2 import GetAssocRequest
from ..apis.assoc.v1.assoc_service_pb2 import GetAssocResponse
from ..apis.assoc.v1.assoc_service_pb2 import ListAssocsRequest
from ..apis.assoc.v1.assoc_service_pb2 import ListAssocsResponse
from ..apis.assoc.v1.assoc_service_pb2 import UpdateAssocRequest
from ..apis.common.v1.types_pb2 import CommonFilter
from ..apis.common.v1.types_pb2 import CommonOption
from ..gateway import assoc_client
from ..gateway import try_request_grpc


class AssocClient:

    @staticmethod
    def assoc():
        return "hello!"

    @property
    def _stub(self):
        return assoc_client

    @try_request_grpc
    def create_assoc(
        self,
        from_id: int,
        to_id: int,
        a_type: AssocType,
    ) -> CreateAssocResponse:
        return self._stub.assoc.CreateAssoc(
            CreateAssocRequest(assoc=Assoc(
                from_id=from_id,
                to_id=to_id,
                a_type=a_type,
            ), ), )

    @try_request_grpc
    def update_assoc(
        self,
        from_id: int,
        to_id: int,
        a_type: AssocType,
        assoc: Assoc,
    ) -> CreateAssocResponse:
        return self._stub.assoc.UpdateAssoc(
            UpdateAssocRequest(
                from_id=from_id,
                to_id=to_id,
                a_type=a_type,
                assoc=assoc,
            ), )

    @try_request_grpc
    def list_assoc(
        self,
        common_option: CommonOption = None,
        common_filter: CommonFilter = None,
        option_filter: AssocOptionFilter = None,
    ) -> ListAssocsResponse:
        return self._stub.assoc.ListAssocs(
            ListAssocsRequest(
                common_filter=common_filter,
                common_option=common_option,
                option_filter=option_filter,
            ), )

    @try_request_grpc
    def delete_assoc(
        self,
        from_id: int,
        to_id: int,
        a_type: AssocType,
    ) -> DeleteAssocResponse:
        return self._stub.assoc.DeleteAssoc(
            DeleteAssocRequest(
                from_id=from_id,
                to_id=to_id,
                a_type=a_type,
            ), )

    @try_request_grpc
    def get_assoc(
        self,
        from_id: int,
        to_id: int,
        a_type: AssocType,
    ) -> GetAssocResponse:
        return self._stub.assoc.GetAssoc(
            GetAssocRequest(
                from_id=from_id,
                to_id=to_id,
                a_type=a_type,
            ), )

    @try_request_grpc
    def count_assoc(
        self,
        from_id: int,
        a_type: AssocType,
    ) -> CountAssocsResponse:
        return self._stub.assoc.CountAssocs(
            CountAssocsRequest(
                from_id=from_id,
                a_type=a_type,
            ), )
