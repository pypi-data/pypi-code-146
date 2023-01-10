from rick_db import fieldmapper


@fieldmapper(tablename="acl_role", pk="id_acl_role")
class AclRole:
    id = "id_acl_role"
    description = "description"


@fieldmapper(tablename="acl_resource", pk="id_acl_resource")
class AclResource:
    id = "id_acl_resource"
    description = "description"


@fieldmapper(tablename="acl_role_resource", pk="id_acl_role_resource")
class AclRoleResource:
    id = "id_acl_role_resource"
    id_role = "fk_acl_role"
    id_resource = "fk_acl_resource"


@fieldmapper(tablename="acl_user_role", pk="id_acl_user_role")
class AclUserRole:
    id = "id_acl_user_role"
    id_role = "fk_acl_role"
    id_user = "fk_user"
