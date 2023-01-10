import abc
from abc import abstractmethod

from pypattyrn.structural.composite import Composite

from local_environment.dependencies.base_dependency import BaseEnvironmentComponent


class BaseComposite(Composite, metaclass=abc.ABCMeta):
    def __init__(self):
        super(BaseComposite, self).__init__(BaseEnvironmentComponent)
        self.compose()

    @abstractmethod
    def compose(self):
        raise NotImplementedError()
