"""Common types & data used by other modules within the jetto_tools package"""

import dataclasses


@dataclasses.dataclass()
class TimeConfig:
    """Time configuration for a JETTO run"""
    start_time: float
    end_time: float
    n_esco_times: int
    n_output_profile_times: int
