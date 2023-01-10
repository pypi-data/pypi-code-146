from copy import deepcopy

from .crud import KeycloakCRUD
from .roles import BaseRoleCRUD


class Role():
    def __init__(self, kc, role):
        self.value = role

        # Note: Composites() kc param must be top-level API URL
        # deepcopy is needed, otherwise we end with corrupted parent client_api (the shallow
        # copied URLs would get patched to be suitable for client role)
        kc_top_level = deepcopy(kc)
        for rest_method in kc_top_level.targets.targets:
            custom_url = kc_top_level.targets.targets[rest_method].copy()
            assert custom_url.resources[-1] == 'clients'
            custom_url.removeLast()
            kc_top_level.targets.targets[rest_method] = custom_url

        self.kc = kc_top_level

    def composite(self):
        return Composites(self.kc, self.value['id'])


class ClientRoleCRUD(BaseRoleCRUD):
    pass


class Composites:
    def __init__(self, kc, roleID):
        # Note: kc must be top-level API URL
        self.kc = kc
        self.id = roleID

        # It just adds few extra resource to the url: /id/composites
        roles_by_id_api = KeycloakCRUD.get_child(kc, None, "roles-by-id")
        self.post = lambda payload: KeycloakCRUD.get_child(roles_by_id_api, self.id, 'composites').create(payload)
        self.remove = lambda payload: KeycloakCRUD.get_child(roles_by_id_api, self.id, 'composites').remove(_id=None, payload=payload)
        # It just adds few extra resource to the url: /id/composites/realm
        # Hm. This assumes composite client role will contain only realm roles (not other client roles).
        # Is this always true, does this cover all usecases?
        self.get = lambda: KeycloakCRUD.get_child(roles_by_id_api, self.id, 'composites/realm').findAll()
        self.get_role_by_name = lambda name='': KeycloakCRUD.get_child(kc, None, 'roles').findFirstByKV(key='name', value=name)

    def link(self, roleName):
        role = self.get_role_by_name(roleName)

        if not role:
            raise("Error the role "+roleName+" not found!")

        return self.post([role])

    def unlink(self, roleName):
        role = self.get_role_by_name(roleName)

        if not role:
            raise ("Error the role " + roleName + " not found!")

        # Whole role representation needed in DELETE payload
        # See https://www.keycloak.org/docs-api/20.0.1/rest-api/index.html#_roles_by_id_resource
        return self.remove([role])

    def findAll(self):
        return self.get()


def new_child(kc, query, child_resource):
    client_id = kc.findFirst(query)['id']
    return KeycloakCRUD.get_child(kc, client_id, child_resource)


class Clients(KeycloakCRUD):

    def secrets(self, client_query):
        obj = super().findFirst(client_query)
        child = KeycloakCRUD.get_child(self, obj['id'], 'client-secret')
        return child

    def get_roles(self, client_query):
        # TODO maybe move briefRepresentation=False into the RestURL class?
        # So we always get same object returned.
        roles = self.roles(client_query).findAll(dict(briefRepresentation=False)).resp().json()

        assert str(self.targets.targets["read"]).endswith("/clients")
        ret = [Role(self, role) for role in roles]
        assert str(self.targets.targets["read"]).endswith("/clients")

        return ret

    def roles(self, client_query):
        client_id = super().findFirst(client_query)['id']
        client_roles_api = ClientRoleCRUD.get_child(self, client_id, 'roles')
        client_roles_api = self.__hack_rest_roles_remove_and_update_endpoint(client_roles_api)
        return client_roles_api

    def __hack_rest_roles_remove_and_update_endpoint(self, client_roles_api):
        custom_delete = self.targets.targets['delete'].copy()
        custom_delete.replaceResource('clients', 'roles-by-id')
        client_roles_api.targets.targets['delete'] = custom_delete

        custom_update = self.targets.targets['update'].copy()
        custom_update.replaceResource('clients', 'roles-by-id')
        client_roles_api.targets.targets['update'] = custom_update

        return client_roles_api
