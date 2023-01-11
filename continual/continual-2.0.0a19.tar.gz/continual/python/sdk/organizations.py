from __future__ import annotations
from typing import List, Optional
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.projects import ProjectManager
from google.protobuf import field_mask_pb2


class OrganizationManager(Manager):
    """Manages user resources."""

    name_pattern: str = "organizations/{user}"

    def create(self, display_name: str) -> Organization:
        """Create an organization.

        Arguments:
            display_name: Display name.

        Returns:
            A new organization.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> client.organizations.create(display_name="example-org")
            <Organization object {'name': 'organizations/ced8rci5lsrrfj0t5f30', 'display_name': 'example-org',
            'update_time': '2022-12-15T03:00:02.419421Z', 'create_time': '2022-12-15T03:00:02.419421Z',
            'status': 'EXPIRED', 'trial_credits': '0', 'trial_credits_used': '0', 'show_plan': False,
            'sso_enabled': False, 'requires_sso': False, 'sso_domains': [], 'allow_external_users': False,
            'sso_configured': False, 'directory_sync_configured': False}>
        """
        req = management_pb2.CreateOrganizationRequest(
            organization=types.Organization(display_name=display_name).to_proto()
        )
        resp = self.client._management.CreateOrganization(req)
        return Organization.from_proto(resp, client=self.client)

    def get(self, id: str) -> Organization:
        """Get organization.

        Arguments:
            id: Organization name or id.

        Returns
            An organization.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> client.organizations.get(id=org.name)
            <Organization object {'name': 'organizations/ced8rci5lsrrfj0t5f30', 'display_name': 'example-org',
            'update_time': '2022-12-15T03:00:02.419421Z', 'create_time': '2022-12-15T03:00:02.419421Z',
            'status': 'EXPIRED', 'trial_credits': '0', 'trial_credits_used': '0', 'show_plan': False,
            'sso_enabled': False, 'requires_sso': False, 'sso_domains': [], 'allow_external_users': False,
            'sso_configured': False, 'directory_sync_configured': False}>
        """
        req = management_pb2.GetOrganizationRequest(name=self.name(id))
        resp = self.client._management.GetOrganization(req)
        return Organization.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        latest: bool = True,
    ) -> List[Organization]:
        """List organizations.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of Organizations.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> orgs = [client.organizations.create(display_name=f"example-org-{i}") for i in range(10)]
            >>> [org.display_name for org in client.organizations.list(page_size=10)] # Orders by 'create_time' by default
            ['example-org-0', 'example-org-1', 'example-org-2', 'example-org-3', 'example-org-4', 'example-org-5',
            'example-org-6', 'example-org-7', 'example-org-8', 'example-org-9']
            >>> [org.display_name for org in client.organizations.list(page_size=10, latest=False)] # Ascending order of create_time
            ['test2@continual.ai', 'test@continual.ai']
        """
        req = management_pb2.ListOrganizationsRequest(
            page_size=page_size, order_by=order_by, latest=latest
        )
        resp = self.client._management.ListOrganizations(req)
        return [
            Organization.from_proto(u, client=self.client) for u in resp.organizations
        ]

    def list_all(self) -> Pager[Organization]:
        """List all organizations.

        Pages through all organization using an iterator.

        Returns:
            A iterator of all organizations.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> orgs = [client.organizations.create(display_name=f"example-org-{i}") for i in range(10)]
            >>> [org.display_name for org in client.organizations.list_all()] # Orders by 'create_time' by default
            ['example-org-0', 'example-org-1', 'example-org-2', 'example-org-3', 'example-org-4', 'example-org-5',
            'example-org-6', 'example-org-7', 'example-org-8', 'example-org-9']
        """

        def next_page(next_page_token):
            req = management_pb2.ListOrganizationsRequest(page_token=next_page_token)
            resp = self.client._management.ListOrganizations(req)
            return (
                [
                    Organization.from_proto(u, client=self.client)
                    for u in resp.organizations
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def delete(self, id: str) -> None:
        """Delete an organization.

        Arguments:
            id: Organization name or id.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> orgs = [client.organizations.create(display_name=f"example-org-{i}") for i in range(10)]
            >>> [client.organizations.delete(id=org.id)  for org in client.organizations.list_all()]
            [None, None, None, None, None, None, None, None, None, None]
            >>> len([org  for org in client.organizations.list_all()])
            0
        """
        req = management_pb2.DeleteOrganizationRequest(name=self.name(id))
        self.client._management.DeleteOrganization(req)

    def update(
        self,
        id: str,
        display_name: Optional[str] = None,
    ) -> Organization:
        """Update organization.

        Arguments:
            id: The organization's id
            display_name:  Display name.

        Returns:
            Updated organization.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="name_wiht_typo")
            >>> client.organizations.update(id=org.name, display_name="name_without_typo").display_name
            'name_without_typo'
        """
        paths = []
        if display_name is not None:
            paths.append("display_name")
        req = management_pb2.UpdateOrganizationRequest(
            update_mask=field_mask_pb2.FieldMask(paths=paths),
            organization=Organization(
                name=self.name(id),
                display_name=display_name,
            ).to_proto(),
        )
        resp = self.client._management.UpdateOrganization(req)
        return Organization.from_proto(resp, client=self.client)


class Organization(Resource, types.Organization):
    """Organization resource."""

    name_pattern = "organizations/{users}"

    _manager: OrganizationManager

    _projects: ProjectManager

    def _init(self):
        self._manager = OrganizationManager(parent=self.parent, client=self.client)
        self._projects = ProjectManager(parent=self.name, client=self.client)

    @property
    def projects(self) -> ProjectManager:
        """Organization's Project Manager."""
        return self._projects

    def delete(self) -> None:
        """Delete organization.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> org.delete()
            >>> len([org for org in client.organizations.list_all()])
            0
        """
        self._manager.delete(self.name)

    def update(
        self,
        display_name: Optional[str] = None,
    ) -> Organization:
        """Update organization.

        Arguments:
            display_name:  Display name.

        Returns:
            Updated organization.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="name_wiht_typo")
            >>> org = org.update(display_name="name_without_typo")
            >>> org.display_name
            'name_without_typo'
        """
        return self._manager.update(
            self.name,
            display_name=display_name,
        )

    def _create_user_role(self, user_name: str, role: str) -> None:
        """Create an organization role for a user

        Arguments:
            user_name: the name of the user
            role: the name of the role
        """

        req = management_pb2.CreateAccessPolicyRequest(
            parent=self.name,
            access_policy=types.AccessPolicy(
                resource=self.name, subject=user_name, role=role
            ).to_proto(),
        )
        self._manager.client._management.CreateAccessPolicy(req)
