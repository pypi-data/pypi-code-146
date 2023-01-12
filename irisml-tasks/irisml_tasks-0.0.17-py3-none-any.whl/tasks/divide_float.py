import dataclasses
import logging
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Floating point division.

    Inputs:
        float0 (float): The output is (float0 / float1).
        float1 (float):
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        float0: float
        float1: float

    @dataclasses.dataclass
    class Outputs:
        result: float

    def execute(self, inputs):
        result = inputs.float0 / inputs.float1
        logger.debug(f"{inputs.float0} / {inputs.float1} = {result}")
        return self.Outputs(result)

    def dry_run(self, inputs):
        return self.execute(inputs)
