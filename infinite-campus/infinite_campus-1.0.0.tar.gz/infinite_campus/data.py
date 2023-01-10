from dataclasses import dataclass


@dataclass(init=False, repr=False)
class DataObject:
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        return self.__class__.__name__