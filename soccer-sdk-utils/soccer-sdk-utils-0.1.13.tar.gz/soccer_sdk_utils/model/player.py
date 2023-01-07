from soccer_sdk_utils.gender import Gender
from soccer_sdk_utils.model.meta import MetaProperty


class Player:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.gender = kwargs.get("gender")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.club = kwargs.get("club")
        self.state = kwargs.get("state")
        self.position = kwargs.get("position")

        self.meta = kwargs.get("meta", [])

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @name.setter
    def name(self, value: str):
        if value is not None:
            parts = value.split(" ")

            if len(parts) == 2:
                self.first_name = parts[0]
                self.last_name = parts[1]
            elif len(parts) == 3:
                self.first_name = parts[0]
                self.last_name = f"{parts[1]} {parts[2]}"
            else:
                self.first_name = value
                self.last_name = None

    @property
    def year(self) -> str | None:
        result = self.get_property("grad_year")
        if result is None:
            result = self.get_property("graduation_year")

        return result

    @property
    def commitment(self) -> str | None:
        result = self.get_property("commitment")

        if result is None:
            result = self.get_property("college_team")

            if result is not None:
                if result.endswith(" Women"):
                    return result[:-6].strip()
                elif result.endswith(" Men"):
                    return result[:-4].strip()

        return result

    @property
    def is_committed(self) -> bool:
        commitment = self.commitment
        return commitment is not None and commitment != ""

    def __repr__(self):
        avps = []

        if self.id is not None:
            avps.append(f"id='{self.id}'")

        avps.append(f"name='{self.name}'")

        if self.year is not None:
            avps.append(f"year='{self.year}'")

        gender_type = type(self.gender)
        if gender_type == Gender:
            avps.append(f"gender='{self.gender.name}'")
        elif gender_type == str:
            avps.append(f"gender='{self.gender}'")

        if self.state is not None:
            avps.append(f"state='{self.state}'")

        avps.append(f"position='{self.position}'")

        if self.club is not None:
            avps.append(f"club='{self.club}'")

        if self.is_committed:
            avps.append(f"commitment='{self.commitment}'")

        return f"<Player({', '.join(avps)})>"

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
