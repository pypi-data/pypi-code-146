from .targets import Targets
from .crud import KeycloakCRUD


class BaseRoleCRUD(KeycloakCRUD):
    _rest_params_read = {"briefRepresentation": False}

    """
    For RH SSO 7.4 (KC 9.0), role with attributes cannot be created.
    We need to first create role, then update it to add attributes.

    This will not be needed any more in RH SSO 7.5.
    """
    def create(self, payload):
        # "composites" are setup via separated API
        # payload.pop("composites", None)

        ret = super().create(payload)
        if "attributes" in payload:
            role = self.findFirstByKV("name", payload["name"])
            self.update(role["id"], payload).isOk()
        return ret


class RealmRoleCRUD(BaseRoleCRUD):
    pass


# The Keycloak guys decided to use another resource DELETE /roles-by-id, instead of sticking to DELETE /roles.
def RolesURLBuilder(url):
    targets = Targets.makeWithURL(url)
    targets.targets['delete'].replaceResource('roles', 'roles-by-id')
    targets.targets['update'].replaceResource('roles', 'roles-by-id')
    return targets