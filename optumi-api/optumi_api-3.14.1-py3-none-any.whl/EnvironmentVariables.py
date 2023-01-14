##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import json


class EnvironmentVariables:
    def __init__(self, name: str = "", environ: dict = None):
        self._name = name

        if environ is None:
            # Retrieve the environment variables
            # This is not the best way to do this...
            integrations = json.loads(optumi.core.get_integrations().text)[
                "integrations"
            ]
            for integration in integrations:
                if integration["name"] == name:
                    self._name = integration["name"]
                    self._environ = EnvironmentVariables.__format_environ(
                        integration["keys"]
                    )
                    return
            raise OptumiException(
                "Unable to find environment variable named '" + name + "'"
            )
        else:
            # Store the environment variables
            info = {
                "integrationType": "environment variable",
                "name": name,
                "variables": environ,
            }
            res = optumi.core.add_integration(name, json.dumps(info), False).text
            try:
                integration = json.loads(res)
                self._name = integration["name"]
                self._environ = self.__format_environ(integration["keys"])
            except json.decoder.JSONDecodeError:
                raise OptumiException(res)

    def rename(self, newName):
        optumi.core.rename_integration(self._name, newName)
        self._name = newName

    def remove(self):
        EnvironmentVariables.purge(self._name)

    @property
    def name(self):
        return self._name

    @property
    def environ(self):
        return dict(zip(self._environ, ["**hidden**" for _ in self._environ]))

    @classmethod
    def __format_environ(cls, keys):
        return dict(zip(keys, ["**hidden**" for _ in keys]))

    @classmethod
    def purge(cls, name: str):
        optumi.core.remove_integration(name)

    def __str__(self):
        return str(self.environ)
