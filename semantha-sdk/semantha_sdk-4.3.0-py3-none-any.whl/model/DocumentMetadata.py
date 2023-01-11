from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.Utils import check_key


@dataclass(frozen=True)
class DocumentMetadata(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict
        check_key(self.data, "fileName", str)
        check_key(self.data, "documentType", str)
