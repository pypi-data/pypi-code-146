from pydantic import BaseModel, Extra
from typing import Sequence
from .metadata import Metadata
from .step import Steps
import logging

from ..dataschema_4_2 import DataSchema as NewDataSchema

logger = logging.getLogger(__name__)


class DataSchema(BaseModel, extra=Extra.forbid):
    metadata: Metadata
    steps: Sequence[Steps]

    def update(self):
        logger.info("Updating from DataSchema-4.1 to DataSchema-4.2")

        nsch = {"metadata": {}, "steps": []}
        nsch["metadata"] = {
            "version": "4.2",
            "timezone": self.metadata.timezone,
            "provenance": self.metadata.provenance.dict(exclude_none=True),
        }
        if "metadata" not in nsch["metadata"]["provenance"]:
            nsch["metadata"]["provenance"]["metadata"] = {
                "updated-using": "dgbowl-schemas",
                "from": self.metadata.version,
            }
        for step in self.steps:
            nstep = {
                "parser": step.parser,
                "tag": step.tag,
                "input": step.input.dict(exclude_none=True),
            }
            if step.externaldate is not None:
                nstep["externaldate"] = step.externaldate.dict(exclude_none=True)
            if step.parameters is not None:
                nstep["parameters"] = step.parameters.dict(exclude_none=True)

            nsch["steps"].append(nstep)

        return NewDataSchema(**nsch)
