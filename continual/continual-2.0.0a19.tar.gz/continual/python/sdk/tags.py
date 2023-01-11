from __future__ import annotations
from typing import List, Optional

from continual.python.sdk.iterators import Pager
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.rpc.management.v1 import (
    management_pb2,
    types as management_types_py,
)


class TagsManager(Manager):
    """Manages tag resources."""

    # the name pattern for tags depends on the resource it was created for
    name_pattern: str = ""

    def create(
        self,
        key: str,
        value: str,
    ) -> Tag:
        """Create tag.

        Arguments:
            key: the tag key
            value: the tag value

        Returns
            A tag.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> run = env.runs.create('run0')
            >>> model_version = run.models.create("example-model").model_versions.create()
            >>> model_version.tags.create(key="test_1", value="test_val")
            <Tag object {'name': 'projects/test_project_1/environments/test_env/models/test_model/versions/cegl9qq5lsrkc0osu0ug/tags/cegm5mq5lsrkc0osu130',
            'key': 'test_1', 'value': 'test_val', 'create_time': '2022-12-20T07:23:07.982232Z', 'update_time': '2022-12-20T07:23:07.982232Z'}>
            >>> model_version.tags.create(key="test_2", value=10)
            <Tag object {'name': 'projects/test_project_1/environments/test_env/models/test_model/versions/cegl9qq5lsrkc0osu0ug/tags/cegm5vq5lsrkc0osu13g',
            'key': 'test_2', 'value': '10', 'create_time': '2022-12-20T07:23:43.273380Z', 'update_time': '2022-12-20T07:23:43.273380Z'}>
            >>> model_version.tags.create(key="test_3", value=0.8)
            <Tag object {'name': 'projects/test_project_1/environments/test_env/models/test_model/versions/cegl9qq5lsrkc0osu0ug/tags/cegm67i5lsrkc0osu140',
            'key': 'test_3', 'value': '0.8', 'create_time': '2022-12-20T07:24:14.532739Z', 'update_time': '2022-12-20T07:24:14.532739Z'}>
        """
        req = management_pb2.CreateTagRequest(
            parent=self.parent,
            key=str(key),
            value=str(value),
        )
        resp = self.client._management.CreateTag(req)
        return Tag.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        latest: bool = True,
        order_by: Optional[str] = None,
    ) -> List[Tag]:
        """List tags.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of tags.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> run = env.runs.create('run0')
            >>> model_version = run.models.create("example-model").model_versions.create()
            >>> tags = [model_version.tags.create(key=f"test_{i}", value="test_val") for i in range(3)]
            >>> [t.key for t in model_version.tags.list(page_size=10)]
            ['test_2', 'test_1', 'test_0']
            >>> [t.key for t in model_version.tags.list(page_size=10, latest=False)]
            ['test_0', 'test_1', 'test_2']
            >>> [t.key for t in model_version.tags.list(page_size=10, order_by="key")]
            ['test_0', 'test_1', 'test_2']
        """
        if not self.client:
            print(f"Cannot list tags without client")
            return

        req = management_pb2.ListTagsRequest(
            parent=self.parent,
            page_size=page_size,
            latest=latest,
            order_by=order_by,
        )
        resp = self.client._management.ListTags(req)
        return [Tag.from_proto(x, client=self.client) for x in resp.tags]

    def list_all(self) -> Pager[Tag]:
        """List all tags.

        Pages through all tags using an iterator.

        Returns:
            A iterator of all tag.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> run = env.runs.create('run0')
            >>> model_version = run.models.create("example-model").model_versions.create()
            >>> tags = [model_version.tags.create(key=f"test_{i}", value="test_val") for i in range(3)]
            >>> [t.key for t in model_version.tags.list_all()]
            ['test_0', 'test_1', 'test_2']
        """

        def next_page(next_page_token):
            req = management_pb2.ListTagsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListTags(req)
            return (
                [Tag.from_proto(x, client=self.client) for x in resp.tags],
                resp.next_page_token,
            )

        return Pager(next_page)

    def get(self, key: str) -> Tag:
        """Get tag.

        Arguments:
            key: The key associated with the tag

        Return
            A Tag

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> run = env.runs.create('run0')
            >>> model_version = run.models.create("example-model").model_versions.create()
            >>> tag = model_version.tags.create(key="test_1", value="test_val")
            >>> model_version.tags.get(key="test_1")
            <Tag object {'name': 'projects/test_project_1/environments/test_env/models/test_model/versions/cegl9qq5lsrkc0osu0ug/tags/cegm5mq5lsrkc0osu130',
            'key': 'test_1', 'value': 'test_val', 'create_time': '2022-12-20T07:23:07.982232Z', 'update_time': '2022-12-20T07:23:07.982232Z'}>
        """

        if not self.client:
            print(f"Cannot fetch tag without client")
            return

        req = management_pb2.GetTagRequest(parent=self.parent, key=key)
        res = self.client._management.GetTag(req)
        return res

    def delete(self, name: str):
        """Delete tag.

        Arguments:
            name: The fully qualified name of the tag

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> run = env.runs.create('run0')
            >>> model_version = run.models.create("example-model").model_versions.create()
            >>> tag = model_version.tags.create(key="test_1", value="test_val")
            >>> len(list(model_version.tags.list_all()))
            1
            >>> model_version.tags.delete(name=tag.name)
            >>> len(list(model_version.tags.list_all()))
            0
        """
        if not self.client:
            print(f"Cannot delete tag without client")
            return

        req = management_pb2.DeleteTagRequest(name=name)
        self.client._management.DeleteTag(req)


class Tag(Resource, management_types_py.Tag):
    """Tag resource."""

    # the name pattern for tags depends on the resource it was created for
    name_pattern: str = ""
    _manager: TagsManager
    """Tags manager."""

    def _init(self):
        self._manager = TagsManager(parent=self.parent, client=self.client)
