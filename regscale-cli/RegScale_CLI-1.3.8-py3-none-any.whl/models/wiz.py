#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from enum import Enum


class AssetType(Enum):
    """Map Wiz assetTypes with RegScale assetCategories


    Args:
        Enum (object): Enum
    """

    SERVICE_USAGE_TECHNOLOGY = "Software"
    SECRET = "Software"
    BUCKET = "Software"
    WEB_SERVICE = "Software"
    DB_SERVER = "Hardware"
    LOAD_BALANCER = "Software"
    CLOUD_ORGANIZATION = "Software"
    SUBNET = "Software"
    VIRTUAL_MACHINE = "Hardware"
    TECHNOLOGY = "Software"
    SECRET_CONTAINER = "Software"
    FILE_SYSTEM_SERVICE = "Software"
    KUBERNETES_CLUSTER = "Software"
    ROUTE_TABLE = "Software"
    COMPUTE_INSTANCE_GROUP = "Software"
    HOSTED_TECHNOLOGY = "Software"
    USER_ACCOUNT = "Software"
    DNS_ZONE = "Software"
    VOLUME = "Software"
    SERVICE_ACCOUNT = "Software"
    RESOURCE_GROUP = "Software"
    ACCESS_ROLE = "Software"
    SUBSCRIPTION = "Software"
    SERVICE_CONFIGURATION = "Software"
    VIRTUAL_NETWORK = "Software"
    VIRTUAL_MACHINE_IMAGE = "Software"
    FIREWALL = "Hardware"
    DATABASE = "Software"
    STORAGE_ACCOUNT = "Software"
