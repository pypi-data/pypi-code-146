from abc import ABCMeta, abstractmethod

class SinkSerializer(metaclass=ABCMeta):
    """This class will serialize the data for the sinks
    using the strategy pattern.
    """
    
    def __init__(self, *args, **kwargs):
        return
    
    @abstractmethod
    def serialize(self, element):
        pass