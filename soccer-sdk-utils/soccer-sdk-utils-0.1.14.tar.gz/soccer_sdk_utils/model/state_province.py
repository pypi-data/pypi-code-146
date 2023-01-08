import uuid


class StateProvince:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.code = kwargs.get("code")
        self.country = kwargs.get("country")

        if self.id is None:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"<StateProvince(name='{self.name}' code='{self.code}', id='{self.id}', country='{self.country}')>"
