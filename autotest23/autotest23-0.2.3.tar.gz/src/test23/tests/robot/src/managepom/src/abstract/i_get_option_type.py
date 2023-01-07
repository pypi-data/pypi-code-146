from abc import ABC, abstractmethod


class IGetOptionType(ABC):
    
    @abstractmethod
    def get_option_name_by_number(self, option_number: int) -> str:
        """This method will take option number of DYNAMIC_COMPONENTS dictionary as parameter
        and return the option type as string. © BS23"""