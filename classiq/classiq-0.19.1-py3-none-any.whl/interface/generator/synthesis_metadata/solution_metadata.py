from typing import List, Optional

import pydantic


class SynthesisStepDurations(pydantic.BaseModel):
    preprocessing: Optional[float] = None
    solving: Optional[float] = None
    conversion_to_circuit: Optional[float] = None
    postprocessing: Optional[float] = None

    def total_time(self) -> float:
        return sum(
            time if time is not None else 0
            for time in (
                self.preprocessing,
                self.solving,
                self.conversion_to_circuit,
                self.postprocessing,
            )
        )


class SolutionMetadata(pydantic.BaseModel):
    topological_sort: List[str]
    failure_reason: Optional[str]
    step_durations: Optional[SynthesisStepDurations]
