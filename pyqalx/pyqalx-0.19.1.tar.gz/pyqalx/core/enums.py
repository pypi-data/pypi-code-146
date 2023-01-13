from enum import Enum


class ValidStates(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    STOPPED = "stopped"
    TERMINATED = "terminated"
