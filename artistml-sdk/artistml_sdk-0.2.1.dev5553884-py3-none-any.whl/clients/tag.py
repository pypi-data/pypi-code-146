from ..apis.common.v1.types_pb2 import CommonOption
from ..apis.tag.v1.tag_pb2 import Tag
from ..apis.tag.v1.tag_pb2 import TagOptionFilter
from ..apis.tag.v1.tag_service_pb2 import CreateTagRequest
from ..apis.tag.v1.tag_service_pb2 import CreateTagResponse
from ..apis.tag.v1.tag_service_pb2 import DeleteTagRequest
from ..apis.tag.v1.tag_service_pb2 import DeleteTagResponse
from ..apis.tag.v1.tag_service_pb2 import GetTagRequest
from ..apis.tag.v1.tag_service_pb2 import GetTagResponse
from ..apis.tag.v1.tag_service_pb2 import ListTagsRequest
from ..apis.tag.v1.tag_service_pb2 import ListTagsResponse
from ..gateway import tag_client
from ..gateway import try_request_grpc


class TagClient:

    @staticmethod
    def tag():
        return "hello!"

    @property
    def _stub(self):
        """
        The function returns the vela client object
        :return: The vela client object
        """
        return tag_client

    @try_request_grpc
    def create_tag(
        self,
        name: str,
        icon: str,
        fontColor: str,
        inheritFrom: int,
    ) -> CreateTagResponse:
        return self._stub.tag.CreateTag(
            CreateTagRequest(tag=Tag(name=name,
                                     icon=icon,
                                     font_color=fontColor,
                                     inherit_from=inheritFrom), ), )

    @try_request_grpc
    def get_tag(
        self,
        id: int,
    ) -> GetTagResponse:
        return self._stub.tag.GetTag(GetTagRequest(id=id), )

    @try_request_grpc
    def list_tag(
        self,
        page: int = 1,
        size: int = 10,
        name: str = None,
        inheritFrom: int = None,
    ) -> ListTagsResponse:
        return self._stub.tag.ListTags(
            ListTagsRequest(
                common_option=CommonOption(page=page, size=size, query=name),
                option_filter=TagOptionFilter(inherit_from=inheritFrom)), )

    @try_request_grpc
    def delete_tag(
        self,
        id: int,
    ) -> DeleteTagResponse:
        return self._stub.tag.DeleteTag(DeleteTagRequest(id=id), )
