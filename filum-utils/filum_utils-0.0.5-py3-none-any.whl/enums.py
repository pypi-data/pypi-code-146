from typing import TypedDict


class BaseEnum:
    @classmethod
    def get_list(cls):
        return [getattr(cls, attr) for attr in dir(cls) if attr.isupper()]


class ParentType(BaseEnum):
    INSTALLED_SOURCE = "installed_source"
    AUTOMATED_ACTION = "automated_action"
    CAMPAIGN = "campaign"


class Organization(TypedDict):
    id: str
    slug: str
