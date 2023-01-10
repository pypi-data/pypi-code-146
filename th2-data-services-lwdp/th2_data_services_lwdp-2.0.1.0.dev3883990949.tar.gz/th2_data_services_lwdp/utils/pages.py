from typing import Dict


class Page:
    def __init__(self, data: Dict):  # noqa
        """Page Constructor.

        Args:
            data (Dict): Page Data
        """
        id_ = data.pop("id")
        data["book"] = id_["book"]
        data["name"] = id_["name"]
        self.data = data
        self.book = data["book"]
        self.name = data["name"]
        self.comment = data["comment"]
        self.start_timestamp = data["started"]
        self.end_timestamp = data["ended"]
        self.updated = data["updated"]
        self.removed = data["removed"]

    def __str__(self):  # noqa
        return str(self.data)

    def __repr__(self):  # noqa
        return self.__str__()
