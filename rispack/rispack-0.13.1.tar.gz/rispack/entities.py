from importlib import import_module

from rispack.schemas import BaseSchema


class BaseEntity(BaseSchema):
    _instances = {}

    @classmethod
    def store(cls):
        store = cls.__name__ + "Store"

        if store in BaseEntity._instances:
            return BaseEntity._instances[store]

        module = import_module("repositories.stores")
        instance = getattr(module, store)()

        BaseEntity._instances[store] = instance

        return instance
