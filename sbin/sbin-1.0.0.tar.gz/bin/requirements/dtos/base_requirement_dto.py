import abc

from bin.requirements.requirement import Requirement


class BaseRequirementDto(abc.ABC):
    @abc.abstractmethod
    def to_requirement(self) -> Requirement:
        pass
