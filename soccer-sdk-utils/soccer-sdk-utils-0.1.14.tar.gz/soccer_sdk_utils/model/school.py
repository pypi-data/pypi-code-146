from soccer_sdk_utils.model.values import Values


class School:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.gender = kwargs.get("gender")
        self.ids = kwargs.get("ids")
        self.urls = kwargs.get("urls")

        if self.ids is None:
            self.ids = Values()

        if self.urls is None:
            self.urls = Values()

    def __repr__(self):
        if self.id is None:
            return f"<School(name='{self.name}', gender='{self.gender}')>"
        else:
            return f"<School(id={self.id}, name='{self.name}', gender='{self.gender}')>"
