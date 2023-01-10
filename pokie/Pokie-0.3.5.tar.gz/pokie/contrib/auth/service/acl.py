from typing import List, Optional

from rick.mixin.injectable import Injectable

from pokie.contrib.auth.dto import AclRole, AclResource
from pokie.contrib.auth.repository.acl import AclRoleRepository, AclResourceRepository
from pokie.constants import DI_DB


class AclService(Injectable):
    def get_user_acl_info(self, id_user: int) -> dict:
        return {
            "roles": self.list_user_role_id(id_user),
            "resources": self.list_user_resource_id(id_user),
        }

    def get_user_roles(self, id_user: int) -> List[AclRole]:
        return self.role_repository.find_user_roles(id_user)

    def list_user_resource_id(self, id_user: int) -> List[str]:
        result = []
        for record in self.resource_repository.find_user_resources(id_user):
            result.append(record.id)
        return result

    def list_user_role_id(self, id_user: int) -> List[str]:
        result = []
        for record in self.role_repository.find_user_roles(id_user):
            result.append(record.id)
        return result

    def list_roles(self) -> List[AclRole]:
        return self.role_repository.fetch_all_ordered(AclRole.id)

    def list_resources(self) -> List[AclResource]:
        return self.resource_repository.fetch_all_ordered(AclResource.id)

    def list_role_resources(self, id_role: int) -> List[AclResource]:
        return self.resource_repository.find_by_role(id_role)

    def get_role(self, id_role: int) -> Optional[AclRole]:
        return self.role_repository.fetch_pk(id_role)

    def get_resource(self, id_resource: str) -> Optional[AclResource]:
        return self.resource_repository.fetch_pk(id_resource)

    def add_role(self, description: str) -> int:
        return self.role_repository.insert_pk(AclRole(description=description))

    def add_resource(self, id_resource: str, description: str) -> int:
        return self.resource_repository.insert_pk(
            AclResource(id=id_resource, description=description)
        )

    def add_role_resource(self, id_role: int, id_resource: int):
        return self.role_repository.add_role_resource(id_role, id_resource)

    def add_user_role(self, id_user: int, id_role: int):
        self.role_repository.add_user_role(id_user, id_role)

    def remove_user_role(self, id_user: int, id_role: int):
        self.role_repository.remove_user_role(id_user, id_role)

    def remove_role(self, id_role: int):
        return self.role_repository.delete_pk(id_role)

    def remove_resource(self, id_resource: int):
        return self.resource_repository.delete_pk(id_resource)

    def can_remove_role(self, id_role: int) -> bool:
        return self.role_repository.can_remove(id_role)

    def truncate_role(self, id_role: int):
        return self.role_repository.truncate(id_role)

    def can_remove_resource(self, id_resource: int) -> bool:
        return self.resource_repository.can_remove(id_resource)

    def truncate_resource(self, id_resource: int):
        return self.resource_repository.truncate(id_resource)

    def remove_role_resource(self, id_role: int, id_resource: int):
        return self.role_repository.remove_role_resource(id_role, id_resource)

    @property
    def role_repository(self):
        return AclRoleRepository(self.get_di().get(DI_DB))

    @property
    def resource_repository(self):
        return AclResourceRepository(self.get_di().get(DI_DB))
