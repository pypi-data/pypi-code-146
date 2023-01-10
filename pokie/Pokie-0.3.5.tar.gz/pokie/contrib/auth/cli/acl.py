from argparse import ArgumentParser
from rick.form import RequestRecord, field

from pokie.contrib.auth.constants import SVC_USER, SVC_ACL
from pokie.constants import DI_SERVICES
from pokie.contrib.auth.service import UserService, AclService
from pokie.core import CliCommand


class DescriptionRequest(RequestRecord):
    fields = {
        "description": field(
            validators="required|minlen:1|maxlen:200", error="invalid description"
        )
    }


class IdDescriptionRequest(RequestRecord):
    fields = {
        "id_resource": field(
            validators="required|minlen:1|maxlen:200", error="invalid resource id"
        ),
        "description": field(
            validators="required|minlen:1|maxlen:200", error="invalid description"
        ),
    }


class UserRoleRequest(RequestRecord):
    fields = {
        "username": field(
            validators="required|pk:user,username", error="invalid username"
        ),
        "id_role": field(
            validators="required|numeric|pk:acl_role", error="invalid role id"
        ),
    }


class RoleResourceRequest(RequestRecord):
    fields = {
        "id_role": field(
            validators="required|numeric|pk:acl_role", error="invalid role id"
        ),
        "id_resource": field(
            validators="required|pk:acl_resource", error="invalid resource id"
        ),
    }


class AclCommand(CliCommand):
    @property
    def svc_user(self) -> UserService:
        return self.get_di().get(DI_SERVICES).get(SVC_USER)

    @property
    def svc_acl(self) -> AclService:
        return self.get_di().get(DI_SERVICES).get(SVC_ACL)


class AclRoleListCmd(AclCommand):
    description = "list acl roles"

    def run(self, args) -> bool:
        for record in self.svc_acl.list_roles():
            self.tty.write("{:<8}: {}".format(str(record.id), record.description))
        return True


class AclRoleCreateCmd(AclCommand):
    description = "create acl role"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "description", type=str, help="Role description for new role"
        )

    def run(self, args) -> bool:
        req = DescriptionRequest()
        if not req.is_valid({"description": args.description}):
            for k, v in req.get_errors().items():
                self.tty.write(
                    self.tty.colorizer.red("Error in {}: {}".format(k, v["*"]))
                )
            return False

        lower = args.description.lower()
        for record in self.svc_acl.list_roles():
            if record.description.lower() == lower:
                self.tty.write(
                    self.tty.colorizer.red(
                        "Error: role with same description already exists"
                    )
                )
                return False

        id = self.svc_acl.add_role(args.description)
        self.tty.write(
            "Created role #{} with description '{}'".format(str(id), args.description)
        )

        return True


class AclRoleRemoveCmd(AclCommand):
    description = "remove acl role"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("id_role", type=int, help="Role id to remove")
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Force removal even if role is in use",
        )

    def run(self, args) -> bool:
        id = int(args.id_role)
        record = self.svc_acl.get_role(id)
        if record is None:
            self.tty.write(
                self.tty.colorizer.red(
                    "Error: role id #{} not found".format(str(args.id_role))
                )
            )
            return False

        if not self.svc_acl.can_remove_role(id) and args.force is False:
            self.tty.write(
                self.tty.colorizer.red(
                    "Error: role is in use; use -f to truncate records"
                )
            )
            return False

        self.svc_acl.truncate_role(id)
        self.tty.write("Role #{} removed successfully".format(id))
        return True


class AclRoleInfoCmd(AclCommand):
    description = "list resources for acl role"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("id_role", type=int, help="Role id to list")

    def run(self, args) -> bool:
        id_role = int(args.id_role)
        record = self.svc_acl.get_role(id_role)
        if record is None:
            self.tty.write(
                self.tty.colorizer.red(
                    "Error: role id #{} not found".format(str(args.id_role))
                )
            )
            return False

        for resource in self.svc_acl.list_role_resources(id_role):
            self.tty.write("{:<12}: {}".format(resource.id, resource.description))
        return True


class AclResourceListCmd(AclCommand):
    description = "list acl resources"

    def run(self, args) -> bool:
        for record in self.svc_acl.list_resources():
            self.tty.write("{:<8}: {}".format(str(record.id), record.description))
        return True


class AclResourceCreateCmd(AclCommand):
    description = "create acl resource"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("id", type=str, help="Id for new resource")
        parser.add_argument("description", type=str, help="Description of new resource")

    def run(self, args) -> bool:
        req = IdDescriptionRequest()
        if not req.is_valid({"id": args.id, "description": args.description}):
            for k, v in req.get_errors().items():
                self.tty.write(
                    self.tty.colorizer.red("Error in {}: {}".format(k, v["*"]))
                )
            return False

        id_lower = args.id.lower()
        lower = args.description.lower()
        for record in self.svc_acl.list_resources():
            if record.id.lower() == id_lower:
                self.tty.write(
                    self.tty.colorizer.red(
                        "Error: resource with specified id already exists"
                    )
                )
                return False
            if record.description.lower() == lower:
                self.tty.write(
                    self.tty.colorizer.red(
                        "Error: resource with specified description already exists"
                    )
                )
                return False

        id = self.svc_acl.add_resource(args.id, args.description)
        self.tty.write(
            "Created resource '{}' with description '{}'".format(
                str(id), args.description
            )
        )

        return True


class AclResourceLinkCmd(AclCommand):
    description = "associate an acl resource with an acl role"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("id_role", type=int, help="Numeric id of existing role")
        parser.add_argument("id_resource", type=str, help="Id of existing resource")

    def run(self, args) -> bool:
        req = RoleResourceRequest()
        if not req.is_valid({"id_role": args.id_role, "id_resource": args.id_resource}):
            for k, v in req.get_errors().items():
                self.tty.write(
                    self.tty.colorizer.red("Error in {}: {}".format(k, v["*"]))
                )
            return False

        id_role = int(args.id_role)
        self.svc_acl.add_role_resource(id_role, args.id_resource)
        self.tty.write(
            "Associated resource '{}' with role #{}".format(args.id_resource, id_role)
        )

        return True


class AclResourceUnlinkCmd(AclCommand):
    description = "removes the association between an acl role and an acl resource"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("id_role", type=int, help="Numeric id of existing role")
        parser.add_argument("id_resource", type=str, help="Id of existing resource")

    def run(self, args) -> bool:
        req = RoleResourceRequest()
        if not req.is_valid({"id_role": args.id_role, "id_resource": args.id_resource}):
            for k, v in req.get_errors().items():
                self.tty.write(
                    self.tty.colorizer.red("Error in {}: {}".format(k, v["*"]))
                )
            return False

        id_role = int(args.id_role)
        self.svc_acl.remove_role_resource(id_role, args.id_resource)
        self.tty.write(
            "Removed association of resource '{}' with role #{}".format(
                args.id_resource, id_role
            )
        )

        return True


class AclRoleLinkCmd(AclCommand):
    description = "associate an user with an acl role"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("username", type=str, help="Existing username")
        parser.add_argument("id_role", type=int, help="Numeric id of existing role")

    def run(self, args) -> bool:
        req = UserRoleRequest()
        if not req.is_valid({"username": args.username, "id_role": args.id_role}):
            for k, v in req.get_errors().items():
                self.tty.write(
                    self.tty.colorizer.red("Error in {}: {}".format(k, v["*"]))
                )
            return False

        user = self.svc_user.get_by_username(args.username)
        if user is None:
            self.tty.write(
                self.tty.colorizer.red(
                    "Error: username '{}' not found".format(args.username)
                )
            )
            return False

        id_role = int(args.id_role)
        self.svc_acl.add_user_role(user.id, id_role)
        self.tty.write(
            "Associated user '{}' with role #{}".format(user.username, id_role)
        )

        return True


class AclRoleUnlinkCmd(AclCommand):
    description = "removes user association with a role"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("username", type=str, help="Existing username")
        parser.add_argument("id_role", type=int, help="Numeric id of existing role")

    def run(self, args) -> bool:
        req = UserRoleRequest()
        if not req.is_valid({"username": args.username, "id_role": args.id_role}):
            for k, v in req.get_errors().items():
                self.tty.write(
                    self.tty.colorizer.red("Error in {}: {}".format(k, v["*"]))
                )
            return False

        user = self.svc_user.get_by_username(args.username)
        if user is None:
            self.tty.write(
                self.tty.colorizer.red(
                    "Error: username '{}' not found".format(args.username)
                )
            )
            return False

        id_role = int(args.id_role)
        self.svc_acl.remove_user_role(user.id, id_role)
        self.tty.write(
            "Removed association of user '{}' with role #{}".format(
                user.username, id_role
            )
        )

        return True


class AclUserRoleCmd(AclCommand):
    description = "list roles associated with a given username"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("username", type=str, help="Existing username")

    def run(self, args) -> bool:

        user = self.svc_user.get_by_username(args.username)
        if user is None:
            self.tty.write(
                self.tty.colorizer.red(
                    "Error: username '{}' not found".format(args.username)
                )
            )
            return False

        for role in self.svc_acl.get_user_roles(user.id):
            self.tty.write("{:<12}: {}".format(role.id, role.description))

        return True
