import uuid


class City:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.spid = kwargs.get("spid")

        if self.id is None:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"<City(name='{self.name}' id='{self.id}', spid='{self.spid}')>"
