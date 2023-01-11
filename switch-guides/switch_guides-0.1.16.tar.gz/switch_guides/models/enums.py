from enum import IntEnum


class StepResultType(IntEnum):
    StepProgress = 0
    StepCompleted = 1
    StructuredLogs = 2
    StepBaselineResult = 3
    
