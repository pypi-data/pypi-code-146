from pydantic import BaseModel, Extra
from typing import Sequence
from .metadata import Metadata
from .step import Steps
import logging

from ..dataschema_5_0 import DataSchema as NewDataSchema

logger = logging.getLogger(__name__)


class DataSchema(BaseModel, extra=Extra.forbid):
    metadata: Metadata
    """Metadata information for yadg."""

    steps: Sequence[Steps]
    """A sequence of parser steps."""

    def update(self):
        logger.info("Updating from DataSchema-4.2 to DataSchema-5.0")

        nsch = {"metadata": {}, "steps": []}
        nsch["metadata"] = {
            "version": "5.0",
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
            else:
                nstep["parameters"] = {}

            if "filetype" in nstep["parameters"]:
                nstep["filetype"] = nstep["parameters"].pop("filetype")

            for k in {
                "sigma",
                "calfile",
                "convert",
                "species",
                "detectors",
                "method",
                "height",
                "distance",
                "cutoff",
                "threshold",
            }:
                if k in nstep["parameters"]:
                    logger.warning(
                        "Parameter '%s' of parser '%s' is not "
                        "supported in DataSchema-5.0.",
                        k,
                        nstep["parser"],
                    )
                    del nstep["parameters"][k]

            if nstep["parameters"] == {}:
                del nstep["parameters"]

            nsch["steps"].append(nstep)

        return NewDataSchema(**nsch)
