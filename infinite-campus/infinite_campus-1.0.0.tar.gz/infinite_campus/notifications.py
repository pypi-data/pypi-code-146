from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=False, repr=False)
class Notification:
    """Notifcation class for student notifications."""

    notificationID: int
    userID: int
    creationTimestamp: str
    notificationTypeID: int
    read: bool
    notificationText: str
    notificationTypeText: str
    displayedDate: str
    finalText: str
    finalUrl: str

    def __init__(self, **kwargs) -> None:
        for kwarg in kwargs.keys():
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "{}: {}.".format(self.displayedDate, self.notificationText)
