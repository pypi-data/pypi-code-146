from soccer_sdk_utils.model.values import Values


class Commitment:
    def __init__(self, **kwargs):
        self.school = kwargs.get("school")
        self.urls = kwargs.get("urls")

    @property
    def school(self) -> str | None:
        return self._school

    @school.setter
    def school(self, value: str | None):
        self._school = value

    @property
    def urls(self) -> Values:
        return self._urls

    @urls.setter
    def urls(self, value: Values):
        self._urls = value
