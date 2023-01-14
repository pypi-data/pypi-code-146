##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import json

from .Machine import Machine, Status


class Machines:
    @classmethod
    def list(cls, status: Status = None):
        machines = []

        response = json.loads(optumi.core.get_machines().text)

        for machine in response["machines"]:
            machine = Machine(*Machine.reconstruct(machine))
            if machine.is_visible():
                machines.append(machine)

        return machines
