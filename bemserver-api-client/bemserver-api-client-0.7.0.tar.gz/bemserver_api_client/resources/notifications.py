"""BEMServer API client resources

/notifications/ endpoints
"""
from .base import BaseResources


class NotificationResources(BaseResources):
    endpoint_base_uri = "/notifications/"
