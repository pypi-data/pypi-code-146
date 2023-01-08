from datetime import datetime


class Suggestion:
    def __init__(
        self,
        _id: str = None,
        description: str = None,
        author: str = None,
        state: str = None,
        opened_on: str = None,
        closed_on: str = None,
    ):
        self.id = _id
        self.description = description
        self.author = author
        self.state = state
        self.opened_on = opened_on
        self.closed_on = closed_on

    def __repr__(self):
        buffer = "<Suggestion("
        buffer += f"id={self.id}, "
        buffer += f"description={self.description}, "
        buffer += f"author={self.author}, "
        buffer += f"state={self.state}, "
        buffer += f"opened_on={self.opened_on}, "
        buffer += f"closed_on={self.closed_on})>"

        return buffer

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value: str):
        self._author = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: str):
        self._state = value

    @property
    def opened_on(self):
        return self._opened_on

    @opened_on.setter
    def opened_on(self, value: datetime):
        self._opened_on = value

    @property
    def closed_on(self) -> datetime:
        return self._closed_on

    @closed_on.setter
    def closed_on(self, value: datetime):
        self._closed_on = value
