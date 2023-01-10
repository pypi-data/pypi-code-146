from typing import List

from classiq.interface.helpers.versioned_model import VersionedModel


class AnglesResult(VersionedModel):
    initial_point: List[float]


class PyomoObjectResult(VersionedModel):
    details: str
