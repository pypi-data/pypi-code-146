from threading import Thread
from typing import Any, Callable, Dict, Optional

import yaml

from servicefoundry.auto_gen.models import Port, Resources
from servicefoundry.function_service.app import build_and_run_app_in_background_thread
from servicefoundry.function_service.build import BuildConfig
from servicefoundry.function_service.remote import RemoteClass
from servicefoundry.function_service.route import RouteGroups
from servicefoundry.v2.lib import Build, LocalSource, Service


class FunctionService:
    def __init__(
        self,
        name: str,
        build_config: Optional[BuildConfig] = None,
        resources: Optional[Resources] = None,
        replicas: int = 1,
        port: int = 8000,
        env: Optional[Dict[str, str]] = None,
    ):
        self._name = name
        self._build_config = build_config or BuildConfig()
        self._resources = resources or Resources()
        self._replicas = replicas
        self._port = port
        self._env = env or {}

        self._route_groups: RouteGroups = RouteGroups()

    @property
    def route_groups(self) -> RouteGroups:
        return self._route_groups

    def __repr__(self):
        return yaml.dump(
            dict(
                name=self._name,
                build_config=self._build_config.dict(),
                resources=self._resources.dict(),
                routes=self._route_groups.dict(),
                replicas=self._replicas,
                port=self._port,
                env=self._env,
            ),
            indent=2,
        )

    def register_function(
        self,
        func: Callable,
        *,
        path: Optional[str] = None,
    ):
        self._route_groups.register_function(func=func, path=path)

    def register_class(
        self,
        class_,
        *,
        init_kwargs: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
    ):
        remote_class = RemoteClass(class_, init_kwargs=init_kwargs, name=name)
        # TODO: I need to rethink this `RemoteClass`.
        # I am mixing up multiple responsibilities here.
        # for now, I am removing the burden of using `remote` from the user when deploying
        # an instance of a class.
        self._route_groups.register_class(remote_class=remote_class)

    def run(self) -> Thread:
        return build_and_run_app_in_background_thread(
            route_groups=self._route_groups, port=self._port
        )

    def get_deployment_definition(self) -> Service:
        # Keeping this function right now so that later,
        # the constructor of the application call this function
        # to get the component spec, if an object of this class
        # is directly passed as an component
        tfy_python_build_config = self._build_config.to_tfy_python_build_config(
            port=self._port, route_groups=self._route_groups
        )
        service = Service(
            name=self._name,
            image=Build(build_source=LocalSource(), build_spec=tfy_python_build_config),
            resources=self._resources,
            replicas=self._replicas,
            ports=[Port(port=self._port, expose=True)],
            env=self._env,
        )
        return service

    def deploy(self, workspace_fqn: str, wait: bool = True):
        service = self.get_deployment_definition()
        service.deploy(workspace_fqn=workspace_fqn, wait=wait)
