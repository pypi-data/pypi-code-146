##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import (
    OptumiException,
)

from .Workload import Status, Workload

import json, os

from enum import Enum


class Workloads:
    @classmethod
    def list(cls, status: Status = None):
        user_information = json.loads(optumi.core.get_user_information(True).text)

        workloads = []

        # Add apps from user information if they don't already exist
        if "jobs" in user_information:
            for app_map in user_information["jobs"]:
                workloads.append(Workload(*Workload.reconstruct(app_map)))
        return workloads

    @classmethod
    def current(cls):
        if not os.environ["OPTUMI_MOD"]:
            raise OptumiException(
                "Workloads.current() only supported on Optumi dynamic machines."
            )

        user_information = json.loads(optumi.core.get_user_information(True).text)

        workloads = []

        # Add apps from user information if they don't already exist
        if "jobs" in user_information:
            for app_map in user_information["jobs"]:
                for module in app_map["modules"]:
                    if module["uuid"] == os.environ["OPTUMI_MOD"]:
                        return Workload(*Workload.reconstruct(app_map))
