import dataclasses
import time
import irisml.core


class Task(irisml.core.TaskBase):
    """Get the current time in seconds since the epoch"""
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Outputs:
        time: float

    def execute(self, inputs):
        return self.Outputs(time.time())

    def dry_run(self, inputs):
        return self.execute(inputs)
