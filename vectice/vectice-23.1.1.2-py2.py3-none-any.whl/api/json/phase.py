from __future__ import annotations

from enum import Enum


class PhaseStatus(Enum):
    """
    Indicates the Documentation Page Status.
    """

    NotStarted = "NotStarted"
    """
    """
    InProgress = "Draft"
    """
    """
    Completed = "Completed"
    """
    """
    InReview = "InReview"


class PhaseInput(dict):
    pass


class PhaseOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def index(self) -> int:
        return int(self["index"])

    @property
    def status(self) -> PhaseStatus:
        return PhaseStatus(self["status"])
