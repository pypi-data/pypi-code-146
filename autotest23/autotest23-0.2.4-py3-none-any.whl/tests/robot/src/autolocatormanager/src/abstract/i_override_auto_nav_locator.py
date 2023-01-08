from abc import ABC, abstractmethod


class IOverrideNavLocator(ABC):
    """
    This an abstract class which is responsible for maintain `Nav locator` source code properly.
    © BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
    """
    @abstractmethod
    def code_body_str_to_list(self, _code_body: str) -> list:
        """
        This method responsible for making updated code body to an array for further operation.
        """
        pass

    @abstractmethod
    def update_old_code_body_data(self, _var: str, _old_body: list) -> str:
        """
        This method responsible for checking and update old source code with updated value.
        """
        pass
