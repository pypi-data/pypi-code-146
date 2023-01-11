from __future__ import annotations
from typing import List, Optional
import json
from continual.python.sdk.iterators import Pager

from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.events import EventManager
from continual.python.sdk.metadata import NpEncoder
from continual.rpc.management.v1 import management_pb2, types

CHUNK_SIZE = 117440512  # 112 MB in bytes, chosen arbitrarily


class ResourceChecksManager(Manager):
    """Manages resource check resources."""

    # the name pattern for a resource check depends on the resource it was created for
    name_pattern: str = ""

    def get(self, id: str) -> ResourceCheck:
        """Get resource check.
        Arguments:
            id: ResourceCheck name or id.
        Returns
            A ResourceCheck.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> dc = dataset_version.resource_checks.create(display_name="Check Null Values", group_name="test", outcome="PASSED", summary="No null values", state="PASS")
            >>> dataset_version.resource_checks.get(id=dc.id)
            <ResourceCheck object {'name': 'projects/continual_test_proj/environments/production/datasets/test_dataset/versions/cegaeq25lsrt9r5a8ma0/resourceChecks/cegai425lsrt9r5a8md0',
            'run_name': 'projects/continual_test_proj/environments/production/runs/cegaeq25lsrt9r5a8m80', 'group_name': 'test', 'outcome': 'PASSED',
            'summary': 'No null values', 'create_time': '2022-12-19T18:10:24.774076Z', 'display_name': 'Check Null Values', 'duration': 0.0,
            'errors': [], 'warnings': [], 'infos': [], 'artifact_name': ''}>
        """

        req = management_pb2.GetResourceCheckRequest(name=self.name(id))
        resource_check = self.client._management.GetResourceCheck(req)
        return ResourceCheck.from_proto(resource_check, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        latest: bool = True,
    ) -> List[ResourceCheck]:
        """List resource checks.
        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
        Returns:
            A list of ResourceChecks.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> checks = [dataset_version.resource_checks.create(display_name=f"Test {i}", group_name="test", outcome=f"{('PASSED' if i%2 == 1 else 'FAILED')}", summary=f"Test {i} passed.") for i in range(5)]
            >>> [check.outcome for check in dataset_version.resource_checks.list(page_size=10)]
            [<CheckOutcome.FAILED: 'FAILED'>, <CheckOutcome.PASSED: 'PASSED'>, <CheckOutcome.FAILED: 'FAILED'>, <CheckOutcome.PASSED: 'PASSED'>, <CheckOutcome.FAILED: 'FAILED'>]
            >>> [check.outcome for check in dataset_version.resource_checks.list(page_size=10, order_by='outcome')]
            [<CheckOutcome.FAILED: 'FAILED'>, <CheckOutcome.PASSED: 'PASSED'>]
        """
        req = management_pb2.ListResourceChecksRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            latest=latest,
        )
        resp = self.client._management.ListResourceChecks(req)
        return [
            ResourceCheck.from_proto(x, client=self.client)
            for x in resp.resource_checks
        ]

    def list_all(self) -> Pager[ResourceCheck]:
        """List all resource checks.
        Pages through all resource_checks using an iterator.
        Returns:
            A iterator of all resource_checks.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> checks = [dataset_version.resource_checks.create(display_name=f"Test {i}", group_name="test", outcome='PASSED', summary=f"Test {i} passed.") for i in range(5)]
            >>> [check.summary for check in dataset_version.resource_checks.list_all()]
            ['Test 0 passed.', 'Test 1 passed.', 'Test 2 passed.', 'Test 3 passed.', 'Test 4 passed.']
        """

        def next_page(next_page_token):
            req = management_pb2.ListResourceChecksRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListResourceChecks(req)
            return (
                [
                    ResourceCheck.from_proto(x, client=self.client)
                    for x in resp.resource_checks
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def create(
        self,
        display_name: str,
        outcome: str,
        group_name: str = "",
        duration: float = 0.0,
        data: dict = {},
        errors: List[str] = [],
        warnings: List[str] = [],
        infos: List[str] = [],
        summary: str = "",
        artifact_name: Optional[str] = "",
    ) -> ResourceCheck:
        """Create a ResourceCheck.
        Arguments:
            group_name: Name of the group.
            outcome: whether the check PASSED, FAILED, or was SKIPPED.
            duration: Duration of the resource check.
            data: Dictionary of additional information if desired.
            errors: List of errors.
            warnings: List of warnings.
            infos: List of infos.
            summary: Human readable summary of the resource check result.
            artifact_name: Name of an artifact associated with the resource check.
            display_name: Display name of the resource check.
        Returns:
            ResourceCheck object.
        Examples:
            >>> ... # Assume client, project, environment, and dataset are defined
            >>> dataset_version = dataset.dataset_versions.create()
            >>> dataset_version.resource_checks.create(display_name="Check Null Values", group_name="test", outcome="PASSED"", summary="No null values", state="PASS")
            <ResourceCheck object {'name': 'projects/continual_test_proj/environments/production/datasets/test_dataset/versions/cegaeq25lsrt9r5a8ma0/resourceChecks/cegai425lsrt9r5a8md0',
            'run_name': 'projects/continual_test_proj/environments/production/runs/cegaeq25lsrt9r5a8m80', 'group_name': 'test', 'outcome': 'PASSED',
            'summary': 'No null values', 'create_time': '2022-12-19T18:10:24.774076Z', 'display_name': 'Check Null Values', 'duration': 0.0, 'data': {},
            'errors': [], 'warnings': [], 'infos': [], 'artifact_name': ''}>
        """
        req = management_pb2.CreateResourceCheckRequest(
            parent=self.parent,
            resource_check=ResourceCheck(
                display_name=display_name,
                group_name=group_name,
                outcome=outcome,
                duration=duration,
                data=json.dumps(data, cls=NpEncoder),
                errors=errors,
                warnings=warnings,
                infos=infos,
                summary=summary,
                artifact_name=artifact_name,
                run_name=self.run_name,
            ).to_proto(),
        )
        resp = self.client._management.CreateResourceCheck(req)
        return ResourceCheck.from_proto(resp, client=self.client)


class ResourceCheck(Resource, types.ResourceCheck):
    """ResourceCheck resource."""

    # the name pattern for resource check depends on the resource it was created for
    name_pattern: str = ""
    manager: ResourceChecksManager

    events: EventManager
    """Event manager."""

    def _init(self):
        self.manager = ResourceChecksManager(parent=self.parent, client=self.client)
