from soccer_sdk_utils.model.meta import MetaProperty


class Club:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.city = kwargs.get("city")
        self.state = kwargs.get("state")
        self.meta = kwargs.get("meta", [])

    @property
    def league(self):
        return self.get_property("league")

    def __repr__(self):
        return f"<Club(id={self.id}, name='{self.name}', location='{self.city}, {self.state}')>"

    def has_property(self, name: str):
        for meta in self.meta:
            if meta.name == name:
                return True

        return False

    def get_property(self, name: str):
        for meta in self.meta:
            if meta.name == name:
                return meta.value

        return None

    def add_property(self, name: str, value: str):
        self.meta.append(MetaProperty(name=name, value=value))


class ClubCommitmentStats:
    def __init__(self, **kwargs):
        self.club = kwargs.get("club")
        self.di = kwargs.get("di")
        self.dii = kwargs.get("dii")
        self.diii = kwargs.get("diii")
        self.naia = kwargs.get("naia")
        self.total = kwargs.get("total")

    def __repr__(self):
        buffer = "<ClubCommitmentStats("
        buffer += f"club={self.club}, "
        buffer += f"di={self.di}, "
        buffer += f"dii={self.dii}, "
        buffer += f"diii={self.diii}, "
        buffer += f"naia={self.naia}, "
        buffer += f"total={self.total})>"

        return buffer
