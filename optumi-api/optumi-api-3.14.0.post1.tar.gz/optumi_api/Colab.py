##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .NotebookConfig import create_config
from .Packages import Packages
from .LocalStorage import LocalStorage
from .Server import Server, mapping
from .Resource import Resource, GpuType
from .Executable import ProgramType
from .Workload import Workload, Progress
from .EnvironmentVariables import EnvironmentVariables

import optumi_core as optumi

import os, datetime, json
from enum import Enum
from typing import Union


class Colab:
    def __init__(self):
        self._program_type = ProgramType.PYTHON_NOTEBOOK

    def __utcnow(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def launch(
        self,
        wait=True,
        progress=Progress.SUMMARY,
        packages=Packages(),
        files=LocalStorage(),
        env: Union[EnvironmentVariables, list] = [],
        resource=Server(size="Standard_NC4as_T4_v3"),
        notifications=None,
    ):
        # Start with blank config
        nb_config = create_config()

        # Plug in program type
        nb_config["programType"] = self._program_type.value

        # Plug in packages
        nb_config["upload"]["requirements"] = "\n".join(packages)

        # Plug in files
        expanded = [f.path for f in files]

        # Make sure files are uploaded
        files.upload()
        nb_config["upload"]["files"] = [
            {"path": optumi.utils.replace_home_with_tilde(path), "enabled": True}
            for path in expanded
        ]

        # Plug in environment variables
        if type(env) is EnvironmentVariables:
            nb_config["integrations"] = [
                {
                    "name": env.name,
                    "enabled": True,
                    "integrationType": "environment variable",
                }
            ]
        else:
            nb_config["integrations"] = [
                {
                    "name": e.name,
                    "enabled": True,
                    "integrationType": "environment variable",
                }
                for e in env
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

        from google.colab import _message

        # Load the notebook JSON string.
        notebook = _message.blocking_request("get_ipynb")["ipynb"]

        # Remove the optumi cell
        notebook["cells"] = [
            cell
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
            and not "".join(cell["source"]).startswith("#skip@optumi")
        ]

        program = json.dumps(notebook)

        # Get the notebook name
        import requests

        d = requests.get("http://172.28.0.2:9000/api/sessions").json()[0]
        name = d["name"]

        setup = json.loads(
            optumi.core.setup_notebook(
                name,
                self.__utcnow(),
                {"path": name, "content": program},
                json.dumps(nb_config),
            ).text
        )

        # print(setup)

        workload_uuid = setup["uuid"]
        run_num = setup["runNum"]

        # this is necessary for the extension
        optumi.core.push_workload_initializing_update(workload_uuid, "Initializing")
        optumi.core.push_workload_initializing_update(workload_uuid, "stop")

        hashes = [optumi.utils.hash_file(f) for f in expanded]
        stats = [os.stat(f) if os.path.isfile(f) else None for f in expanded]
        creation_times = [
            datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z"
            if stat != None
            else str(None)
            for stat in stats
        ]
        last_modification_times = [
            datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
            if stat != None
            else str(None)
            for stat in stats
        ]
        sizes = [str(stat.st_size) if stat else str(None) for stat in stats]

        optumi.core.launch_notebook(
            nb_config["upload"]["requirements"],
            hashes,
            [optumi.utils.replace_home_with_tilde(path) for path in expanded],
            creation_times,
            last_modification_times,
            sizes,
            workload_uuid,
            self.__utcnow(),
        )

        launch_status = optumi.get_launch_status(workload_uuid)

        # print(launch_status)

        module_uuid = launch_status["modules"][0]

        workload = Workload(
            name, program, workload_uuid, module_uuid, nb_config, run_num
        )
        if wait:
            workload.wait(progress)
        return workload
