"""BEMServer API client resources

/about/ endpoint
"""
from .base import BaseResources


class AboutResources(BaseResources):
    endpoint_base_uri = "/about/"
    disabled_endpoints = ["getone", "create", "update", "delete"]
