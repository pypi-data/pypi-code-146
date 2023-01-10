from sqlalchemy import and_
from viggocore.subsystem.application.resource import Application
from typing import List
from viggocore.common import exception
from viggocore.common.input import RouteResource, InputResource, \
    InputResourceUtils
from viggocore.common.subsystem import operation, manager
from viggocore.subsystem.capability.resource import Capability
from viggocore.subsystem.policy.resource import Policy
from viggocore.subsystem.role.resource import Role
from viggocore.subsystem.route.resource import Route


class Create(operation.Create):

    def pre(self, session, **kwargs) -> bool:
        self.exceptions = kwargs.pop('exceptions', [])

        return super().pre(session, **kwargs)

    def do(self, session, **kwargs):
        super().do(session)
        self.manager.create_user_capabilities_and_policies(id=self.entity.id,
                                                           session=session)
        if self.entity.name != Application.DEFAULT:
            self.manager.create_admin_capabilities_and_policies(
                id=self.entity.id, session=session, exceptions=self.exceptions)
        return self.entity


class CreateUserCapabilitiesAndPolicies(operation.Operation):

    def pre(self, session, id, **kwargs) -> bool:
        self.application_id = id
        self.user_resources = self.manager.bootstrap_resources.USER
        self.role_id = self.manager.api.roles().\
            get_role_by_name(role_name=Role.USER).id

        return True

    def do(self, session, **kwargs):
        self.resources = {'resources': self.user_resources}
        self.manager.api.capabilities().create_capabilities(
            id=self.application_id, **self.resources)

        self.resources['application_id'] = self.application_id
        self.manager.api.roles().create_policies(id=self.role_id,
                                                 **self.resources)


class CreateAdminCapabilitiesAndPolicies(operation.Operation):

    def _map_routes(self, routes: List[Route]) -> List[RouteResource]:
        resources = [(route.url, route.method) for route in routes]
        return resources

    def _filter_resources(self, all_resources: List[RouteResource],
                          exceptions_resources: List[RouteResource],
                          sysadmin_exclusive_resources: List[RouteResource],
                          user_resources: List[RouteResource]) \
            -> List[RouteResource]:
        resources = InputResourceUtils.diff_resources(
            all_resources, sysadmin_exclusive_resources, user_resources,
            exceptions_resources)
        return resources

    def pre(self, session, id, exceptions: List[InputResource] = [], **kwargs):
        self.application_id = id
        exceptions_resources = InputResourceUtils.parse_resources(exceptions)

        routes = self.manager.api.routes().list(active=True)
        routes_resources = self._map_routes(routes)

        self.admin_role_id = self.manager.api.roles().\
            get_role_by_name(role_name=Role.ADMIN).id

        self.admin_resources = self._filter_resources(
            routes_resources, exceptions_resources,
            self.manager.bootstrap_resources.SYSADMIN_EXCLUSIVE,
            self.manager.bootstrap_resources.USER)
        return True

    def do(self, session, **kwargs):
        self.resources = {'resources': self.admin_resources}
        self.manager.api.capabilities().create_capabilities(
            id=self.application_id, **self.resources)

        self.resources['application_id'] = self.application_id
        self.manager.api.roles().create_policies(id=self.admin_role_id,
                                                 **self.resources)


class CreateCapabilitiesWithExceptions(operation.Operation):

    def _filter_resources(self, routes: List[Route],
                          exceptions: List[RouteResource],
                          sysadmin_exclusive_resources: List[RouteResource],
                          user_resources: List[RouteResource]) \
            -> List[RouteResource]:
        all_resources = [(route.url, route.method) for route in routes]
        resources = InputResourceUtils.diff_resources(
            all_resources, sysadmin_exclusive_resources, user_resources,
            exceptions)
        return resources

    def pre(self, session, id: str, **kwargs):
        self.application_id = id
        exceptions = kwargs.get('exceptions', None)

        if not self.application_id or exceptions is None:
            raise exception.BadRequest()

        routes = self.manager.api.routes().list(active=True)
        exceptions_resources = InputResourceUtils.parse_resources(exceptions)
        self.resources = self.\
            _filter_resources(routes,
                              exceptions_resources,
                              self.manager.bootstrap_resoures.
                              SYSADMIN_EXCLUSIVE,
                              self.manager.bootstrap_resources.USER)

        return self.driver.get(id, session=session) is not None

    def do(self, session, **kwargs):
        data = {'resources', self.resources}
        self.manager.api.capabilities().\
            create_capabilities(id=self.application_id, **data)


class GetRoles(operation.Operation):

    def pre(self, session, id, **kwargs):
        self.application_id = id
        return self.driver.get(id, session=session) is not None

    def do(self, session, **kwargs):
        roles = session.query(Role). \
            join(Policy). \
            join(Capability). \
            filter(and_(Capability.application_id == self.application_id,
                        Role.name != Role.USER)). \
            distinct()
        return roles


class UpdateSettings(operation.Update):

    def pre(self, session, id: str, **kwargs) -> bool:
        self.settings = kwargs
        if self.settings is None or not self.settings:
            raise exception.BadRequest("Erro! There is not a setting")
        return super().pre(session=session, id=id)

    def do(self, session, **kwargs):
        result = {}
        for key, value in self.settings.items():
            new_value = self.entity.update_setting(key, value)
            result[key] = new_value
        super().do(session)

        return result


class RemoveSettings(operation.Update):

    def pre(self, session, id: str, **kwargs) -> bool:
        self.keys = kwargs.get('keys', [])
        if not self.keys:
            raise exception.BadRequest('Erro! keys are empty')
        super().pre(session, id=id)

        return self.entity.is_stable()

    def do(self, session, **kwargs):
        result = {}
        for key in self.keys:
            value = self.entity.remove_setting(key)
            result[key] = value
        super().do(session=session)

        return result


class GetApplicationSettingsByKeys(operation.Get):

    def pre(self, session, id, **kwargs):
        self.keys = kwargs.get('keys', [])
        if not self.keys:
            raise exception.BadRequest('Erro! keys are empty')
        return super().pre(session, id=id)

    def do(self, session, **kwargs):
        entity = super().do(session=session)
        settings = {}
        for key in self.keys:
            value = entity.settings.get(key, None)
            if value is not None:
                settings[key] = value
        return settings


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
        self.create_user_capabilities_and_policies = \
            CreateUserCapabilitiesAndPolicies(self)
        self.create_admin_capabilities_and_policies = \
            CreateAdminCapabilitiesAndPolicies(self)
        self.get_roles = GetRoles(self)
        self.update_settings = UpdateSettings(self)
        self.remove_settings = RemoveSettings(self)
        self.get_application_settings_by_keys = \
            GetApplicationSettingsByKeys(self)
