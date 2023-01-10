from typing import List

from rick_db import Repository
from rick_db.sql import Select, Literal, Delete, Insert

from pokie.contrib.auth.dto import AclRole, AclUserRole, AclResource, AclRoleResource


class AclRoleRepository(Repository):
    def __init__(self, db):
        super().__init__(db, AclRole)

    def find_user_roles(self, id_user: int) -> List[AclRole]:
        key = "__acl__:find_user_roles"
        sql = self._cache_get(key)
        if not sql:
            sql, _ = (
                self.select()
                .join(AclUserRole, AclUserRole.id_role, AclRole, AclRole.id)
                .where(AclUserRole.id_user, "=", id_user)
                .order(AclRole.id)
                .assemble()
            )
            self._cache_set(key, sql)
        with self._db.cursor() as c:
            return c.fetchall(sql, [id_user], cls=AclRole)

    def can_remove(self, id_role: int) -> bool:
        """
        Check if a given role is empty or not in use
        :param id_role:
        :return:
        """
        # check if role references resources
        sql, values = (
            Select(self._dialect)
            .from_(
                AclRoleResource,
                cols={Literal("COUNT(*)"): "total"},
                schema=self._schema,
            )
            .where(AclRoleResource.id_role, "=", id_role)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchone(sql, values)
            if result["total"] != 0:
                return False

        # check if role is referenced by users
        sql, values = (
            Select(self._dialect)
            .from_(
                AclUserRole, cols={Literal("COUNT(*)"): "total"}, schema=self._schema
            )
            .where(AclUserRole.id_role, "=", id_role)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchone(sql, values)
            if result["total"] != 0:
                return False

        return True

    def truncate(self, id_role: int):
        # delete role resources
        sql, values = (
            Delete(self._dialect)
            .from_(AclRoleResource)
            .where(AclRoleResource.id_role, "=", id_role)
            .assemble()
        )
        self.exec(sql, values)

        # delete user associations
        sql, values = (
            Delete(self._dialect)
            .from_(AclUserRole)
            .where(AclUserRole.id_role, "=", id_role)
            .assemble()
        )
        self.exec(sql, values)

        # finally, delete role
        self.delete_pk(id_role)

    def add_role_resource(self, id_role: int, id_resource: int):
        """
        Associates a resource with a role
        :param id_role:
        :param id_resource:
        :return:
        """
        # check if resource is already in role
        sql, values = (
            Select(self._dialect)
            .from_(AclRoleResource, schema=self._schema)
            .where(AclRoleResource.id_role, "=", id_role)
            .where(AclRoleResource.id_resource, "=", id_resource)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchall(sql, values)
            if len(result) > 0:
                return

        sql, values = (
            Insert(self._dialect)
            .into(AclRoleResource(id_role=id_role, id_resource=id_resource))
            .assemble()
        )
        self.exec(sql, values)

    def remove_role_resource(self, id_role: int, id_resource: int):
        """
        Removes an association between a resource and a role
        :param id_role:
        :param id_resource:
        :return:
        """
        # check if resource is already in role
        sql, values = (
            Select(self._dialect)
            .from_(AclRoleResource, schema=self._schema)
            .where(AclRoleResource.id_role, "=", id_role)
            .where(AclRoleResource.id_resource, "=", id_resource)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchall(sql, values)
            if len(result) == 0:
                return

        # delete resource from role association
        sql, values = (
            Delete(self._dialect)
            .from_(AclRoleResource)
            .where(AclRoleResource.id_role, "=", id_role)
            .where(AclRoleResource.id_resource, "=", id_resource)
            .assemble()
        )
        self.exec(sql, values)

    def remove_user_role(self, id_user: int, id_role: int):
        """
        Removes an association between a user and a role
        :param id_user:
        :param id_role:
        :return:
        """
        # check if role is associated with user
        sql, values = (
            Select(self._dialect)
            .from_(AclUserRole, schema=self._schema)
            .where(AclUserRole.id_role, "=", id_role)
            .where(AclUserRole.id_user, "=", id_user)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchall(sql, values)
            if len(result) == 0:
                return

        # delete role from user
        sql, values = (
            Delete(self._dialect)
            .from_(AclUserRole)
            .where(AclUserRole.id_role, "=", id_role)
            .where(AclUserRole.id_user, "=", id_user)
            .assemble()
        )
        self.exec(sql, values)

    def add_user_role(self, id_user, id_role):
        """
        Associates a user with a role
        :param id_user:
        :param id_role:
        :return:
        """
        # check if role is associated with user
        sql, values = (
            Select(self._dialect)
            .from_(AclUserRole, schema=self._schema)
            .where(AclUserRole.id_role, "=", id_role)
            .where(AclUserRole.id_user, "=", id_user)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchall(sql, values)
            if len(result) > 0:
                return

        # insert association record
        sql, values = (
            Insert(self._dialect)
            .into(AclUserRole(id_role=id_role, id_user=id_user))
            .assemble()
        )
        self.exec(sql, values)


class AclResourceRepository(Repository):
    def __init__(self, db):
        super().__init__(db, AclResource)

    def find_user_resources(self, id_user: int) -> List[AclResource]:
        key = "__acl__:find_user_resources"
        sql = self._cache_get(key)
        if not sql:
            sql, _ = (
                self.select()
                .join(
                    AclRoleResource,
                    AclRoleResource.id_resource,
                    AclResource,
                    AclResource.id,
                )
                .join(
                    AclUserRole,
                    AclUserRole.id_role,
                    AclRoleResource,
                    AclRoleResource.id_role,
                )
                .where(AclUserRole.id_user, "=", id_user)
                .assemble()
            )
            self._cache_set(key, sql)

        with self._db.cursor() as c:
            return c.fetchall(sql, [id_user], cls=AclResource)

    def find_by_role(self, id_role: int) -> List[AclResource]:
        """
        List resources for a given role
        :param id_role:
        :return:
        """
        key = "__acl__:find_by_role"
        sql = self._cache_get(key)
        if not sql:
            sql, _ = (
                self.select()
                .join(
                    AclRoleResource,
                    AclRoleResource.id_resource,
                    AclResource,
                    AclResource.id,
                )
                .where(AclRoleResource.id_role, "=", id_role)
                .order(AclResource.id)
                .assemble()
            )
            self._cache_set(key, sql)

        with self._db.cursor() as c:
            return c.fetchall(sql, [id_role], cls=AclResource)

    def can_remove(self, id_resource: int):
        """
        Check if a given resource can be removed
        :param id_resource:
        :return:
        """
        # check if role references resources
        sql, values = (
            Select(self._dialect)
            .from_(
                AclRoleResource,
                cols={Literal("COUNT(*)"): "total"},
                schema=self._schema,
            )
            .where(AclRoleResource.id_resource, "=", id_resource)
            .assemble()
        )

        with self._db.cursor() as c:
            result = c.fetchone(sql, values)
            return result["total"] == 0
