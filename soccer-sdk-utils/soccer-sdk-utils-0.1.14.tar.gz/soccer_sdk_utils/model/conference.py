import uuid

from soccer_sdk_utils.model.values import Values
from soccer_sdk_utils.tools import slugify


class Conference:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.division = kwargs.get("division")
        self.ids = kwargs.get("ids")
        self.urls = kwargs.get("urls")

        if self.ids is None:
            self.ids = Values()

        if self.urls is None:
            self.urls = Values()

    @property
    def slug(self) -> str:
        """Returns a slug for the conference"""
        return slugify(self.name)

    def __repr__(self):
        if self.id is None:
            return f"<Conference(name='{self.name}', division='{self.division}', gender='{self.gender.name}')>"
        else:
            return f"<Conference(id={self.id}, name='{self.name}', division='{self.division}', gender='{self.gender.name}')>"

    def generate_id(self):
        """Generates a unique ID for the user in place"""
        self.id = str(uuid.uuid4())
