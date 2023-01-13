##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


from .NotebookConfig import create_config
from .Server import Server, mapping
from .Resource import Resource, GpuType
from .Executable import ProgramType
from .Workload import Workload, Progress
from .ContainerRegistry import ContainerRegistry

import optumi_core as optumi

import os, datetime, json
from enum import Enum
from typing import Union


class Container:
    def __init__(self, image: str, registry: ContainerRegistry = None):
        self._image = image
        self._registry = registry

    def __utcnow(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def launch(
        self,
        wait=True,
        progress=Progress.SUMMARY,
        resource=Server(size="Standard_NC4as_T4_v3"),
        notifications=None,
    ):
        # Start with blank config
        nb_config = create_config()

        # Plug in program type
        nb_config["programType"] = ProgramType.DOCKER_CONTAINER.value

        # Register any unsaved container registries with the controller
        # Plug in container registries

        if self._registry:
            nb_config["integrations"] = [
                {
                    "name": self._registry.name,
                    "enabled": True,
                    "integrationType": "generic container registry",
                }
            ]

        # Plug in resource requirements
        if type(resource) is Server:
            nb_config["machineAssortment"] = [
                mapping[resource.provider.value] + ":" + resource.size
            ]
        elif type(resource) is Resource:
            nb_config["machineAssortment"] = []
            if type(resource.gpu) is bool:
                nb_config["graphics"]["cores"] = [1 if resource.gpu else -1, -1, -1]
            elif type(resource.gpu) is GpuType:
                nb_config["graphics"]["cores"] = [1, -1, -1]
                nb_config["graphics"]["boardType"] = resource.gpu.value

        # Plug in requirements
        if notifications != None:
            nb_config["notifications"] = {
                "jobStartedSMSEnabled": notifications.job_started,
                "jobCompletedSMSEnabled": notifications.job_completed,
                "jobFailedSMSEnabled": notifications.job_failed,
                "packageReadySMSEnabled": False,
            }

        container_name = (
            self._registry.url + "/" + self._image if self._registry else self._image
        )

        setup = json.loads(
            optumi.core.setup_notebook(
                container_name,
                self.__utcnow(),
                {"path": container_name, "content": container_name},
                json.dumps(nb_config),
            ).text
        )

        # print(setup)

        # TODO:JJ What do we do about error handling for these calls

        workload_uuid = setup["uuid"]
        run_num = setup["runNum"]

        # this is necessary for the extension
        optumi.core.push_workload_initializing_update(workload_uuid, "Initializing")
        optumi.core.push_workload_initializing_update(workload_uuid, "stop")

        optumi.core.launch_notebook(
            nb_config["upload"]["requirements"],
            [],
            [],
            [],
            [],
            [],
            workload_uuid,
            self.__utcnow(),
        )

        launch_status = optumi.get_launch_status(workload_uuid)

        # print(launch_status)

        module_uuid = launch_status["modules"][0]

        workload = Workload(
            container_name,
            container_name,
            workload_uuid,
            module_uuid,
            nb_config,
            run_num,
        )

        if wait:
            workload.wait(progress)
        return workload

    @property
    def image(self):
        return self._image

    @property
    def registry(self):
        return self._registry

    def __str__(self):
        return self._registry.url + "/" + self._image if self._registry else self._image
