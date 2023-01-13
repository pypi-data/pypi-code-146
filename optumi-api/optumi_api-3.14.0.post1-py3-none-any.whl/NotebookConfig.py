##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


def create_config(config={}):
    default = {
        "intent": 0.5,
        "compute": {
            "expertise": "component",
            "required": False,
            "rating": [-1, -1, -1],
            "score": [-1, -1, -1],
            "cores": [-1, -1, -1],
            "frequency": [-1, -1, -1],
        },
        "graphics": {
            "expertise": "simplified",
            "required": False,
            "rating": [-1, -1, -1],
            "score": [-1, -1, -1],
            "cores": [-1, -1, -1],
            "memory": [-1, -1, -1],
            "frequency": [-1, -1, -1],
            "boardType": "U",
        },
        "memory": {
            "expertise": "component",
            "required": False,
            "rating": [-1, -1, -1],
            "size": [-1, -1, -1],
        },
        "storage": {
            "expertise": "component",
            "required": False,
            "rating": [-1, -1, -1],
            "size": [-1, -1, -1],
            "iops": [-1, -1, -1],
            "throughput": [-1, -1, -1],
        },
        "upload": {"files": [], "requirements": ""},
        "integrations": [],
        "machineAssortment": ["Azure:Standard_NC4as_T4_v3"],
        "notifications": {
            "jobStartedSMSEnabled": False,
            "jobCompletedSMSEnabled": False,
            "jobFailedSMSEnabled": False,
            "packageReadySMSEnabled": False,
        },
        "interactive": False,
        "annotation": "",
    }
    default.update(config)
    return default
