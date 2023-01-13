##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    ServiceException,
    OptumiException,
)


import json


class ContainerRegistry:
    def __init__(self, name: str, url: str, username: str = None, password: str = None):
        got_username = username != None and len(username) > 0
        got_password = password != None
        if (got_username and not got_password) or (not got_username and got_password):
            raise OptumiException("Inconsistent username/password combination")

        self._name = name
        self._url = url
        self._username = username
        self._password = password

        info = {
            "integrationType": "container registry",
            "name": name,
            "registryService": "generic container registry",
            "url": self._url,
            "username": self._username,
            "password": self._password,
        }
        integration = json.loads(
            optumi.core.add_integration(name, json.dumps(info), False).text
        )
        self._name = integration["name"]

    def remove(self):
        ContainerRegistry.remove(self._name)

    @classmethod
    def remove(cls, name: str):
        optumi.core.remove_integration(name)

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @classmethod
    def load(cls, name: str):
        # This is not the best way to do this...
        integrations = json.loads(optumi.core.get_integrations().text)["integrations"]
        for integration in integrations:
            if integration["name"] == name:
                con = ContainerRegistry(integration["url"])
                con._name = integration["name"]
                return env

    @classmethod
    def purge(cls, name: str):
        optumi.core.remove_integration(name)

    def __str__(self):
        return str(self._url) + " " + str(self._username)
