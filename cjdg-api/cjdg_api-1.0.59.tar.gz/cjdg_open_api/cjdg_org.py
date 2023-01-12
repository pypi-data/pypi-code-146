import requests
from .base import base


class cjdgOrg(base):

    def __init__(self, token, app_secret):
        super().__init__(token, app_secret)

    def create(self, data):
        api_name = "org/create"
        return self.request(api_name, data)

    def create_one(self, data):
        api_name = "org/create"
        return self.request(api_name, data)

    def list(self, data):
        api_name = "org/query"
        return self.request(api_name, data)

    def update(self, data):
        api_name = "org/modifi"
        return self.request(api_name, data)

    def delete(self, data):
        api_name = "org/delete"
        return self.request(api_name, data)

    def install(self):
        api_name = "org/install"
        return self.request(api_name)
