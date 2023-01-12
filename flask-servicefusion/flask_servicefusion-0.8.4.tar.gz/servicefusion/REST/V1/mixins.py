from servicefusion.REST import BaseService

class BaseServiceMixin(BaseService):
    primary_key = "id"
    update_verb = "PUT"

class CreateMixin(BaseServiceMixin):
    def create(self, **kwargs):
        return self._post(f"{self.api_url}", data=kwargs)


class DeleteMixin(BaseServiceMixin):
    def delete(self, id: int, params: dict = None):
        return self._delete(f"{self.api_url}/{id}", params=params)