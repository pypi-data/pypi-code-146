from soccer_sdk_utils.model.meta import MetaProperty


class Team:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.abbreviation = kwargs.get("abbreviation")

        self.meta = kwargs.get("meta", [])

    def __repr__(self):
        avps = []

        if self.id is not None:
            avps.append(f"id='{self.id}'")

        avps.append(f"title='{self.title}'")


        return f"<Team({', '.join(avps)})>"

    def has_property(self, name: str) -> bool:
        for item in self.meta:
            if item.name == name:
                return item.value is not None and item.value != ""

        return False

    def get_property(self, name: str) -> str | None:
        for item in self.meta:
            if item.name == name:
                return item.value

        return None

    def update_property(self, name: str, value: str | None):
        for item in self.meta:
            if item.name == name:
                item.value = value

    def add_property(self, name: str, value: str | None):
        if value is not None:

            if type(value) == str:
                value = value.strip()

                if len(value) == 0:
                    value = None

        if self.has_property(name):
            self.update_property(name, value)
        else:
            self.meta.append(MetaProperty(name=name, value=value))
