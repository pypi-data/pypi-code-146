from ..Phase import Phase
from ..util.Optionizable import Optionizable


class Decorator(Optionizable):
    """
    This is an abstract class to implement custom phase decorators.
    A phase decorator that can overwrite methods that should be run before or/and
    after the execution of a specified phase

    Args:
        Optionizable (dict): config options that can be used within the methods
    """

    def filter(self, phase: Phase) -> bool:
        """this method can returns if the decorator should be used for the given phase

        Args:
            phase (Phase): the phase that should be checked

        Returns:
            bool: return True if the decorator should be executed
        """
        return True

    def before(self, phase: Phase):
        """this method is executed right before the phase is executed

        Args:
            phase (Phase): the phase that will be runned after this method
        """
        pass

    def after(self, phase: Phase):
        """this method is executed right after the phase is executed

        Args:
            phase (Phase): the phase that was just executed
        """
        pass
