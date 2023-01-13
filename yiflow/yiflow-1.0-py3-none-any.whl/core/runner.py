from abc import abstractmethod


class Runner(object):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError("`run` method must be implemented!")