import abc
from abc import abstractmethod
import copy


class BaseNoSQLStorage(abc.ABC):
    def __init__(self):
        self._data = {}

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def dump(self):
        raise NotImplementedError

    def __getattribute__(self, item):
        if item == "_data":
            return AttributeError(
                "Direct access to data is restricted for consistency, use get_data(*keys) method instead"
            )
        else:
            object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        if key == "_data":
            return AttributeError(
                "Direct data assignment is restricted for consistency, use set_data(**kwargs) method instead"
            )
        else:
            object.__setattr__(self, key, value)

    def set_data(self, **kwargs):
        updated = False
        for key, value in kwargs.items():
            if key not in self._data.keys() or self._data[key] != value:
                self._data[key] = copy.deepcopy(value)
                updated = True
        if updated:
            self.dump()

    def delete_data(self, *keys):
        for key in keys:
            if key in self._data.keys():
                del self._data[key]
            else:
                raise KeyError(key)
        self.dump()

    def reset_data(self):
        self._data = {}
        self.dump()

    def get_data(self, *keys) -> tuple:
        result = []
        for key in keys:
            if key in self._data.keys():
                result.append(self._data[key])
            else:
                raise KeyError(key)
        return tuple(result)
