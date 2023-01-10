from abc import ABC, abstractmethod
from .exceptions import UnknownSymbolError


class RegistryMixin(ABC):
    _registry = None

    def lookup(self, name):
        """Lookup a symbol based on its name.
        """
        symbol = self._registry.get(name, name) if self._registry else name
        if isinstance(symbol, str):
            raise UnknownSymbolError(name)
        return symbol

    @property
    def registry(self):
        """Get the name registry.
        """
        return self._registry

    @registry.setter
    def registry(self, value):
        """Set the name registry.
        """
        if value != self._registry:
            self._registry = value
            self.set_registry(value)

    @abstractmethod
    def set_registry(self, value):
        pass
