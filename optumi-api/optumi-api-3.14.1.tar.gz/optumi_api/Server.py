##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from enum import Enum


class Provider(Enum):
    AZ = "AZ"
    AWS = "AWS"
    GCP = "GCP"


mapping = {
    "AZ": "Azure",
    "AWS": "aws?",
    "GCP": "gcp?",
}

reverse_mapping = {v: k for k, v in mapping.items()}

# Support embedding the provider in the machine string, have no default provider argument
class Server:
    def __init__(
        self, size: str = "Standard_NC4as_T4_v3", provider: Provider = Provider.AZ
    ):
        if ":" in size:
            s = size.split(":")
            self._provider = Provider(s[0])
            self._size = s[1]
        else:
            self._provider = provider
            self._size = size

    @property
    def provider(self):
        return self._provider

    @property
    def size(self):
        return self._size

    def __str__(self):
        return str(self.provider) + ":" + str(self.size)
