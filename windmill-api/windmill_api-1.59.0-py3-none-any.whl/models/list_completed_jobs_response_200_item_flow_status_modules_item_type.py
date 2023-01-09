from enum import Enum


class ListCompletedJobsResponse200ItemFlowStatusModulesItemType(str, Enum):
    WAITINGFORPRIORSTEPS = "WaitingForPriorSteps"
    WAITINGFOREVENTS = "WaitingForEvents"
    WAITINGFOREXECUTOR = "WaitingForExecutor"
    INPROGRESS = "InProgress"
    SUCCESS = "Success"
    FAILURE = "Failure"

    def __str__(self) -> str:
        return str(self.value)
