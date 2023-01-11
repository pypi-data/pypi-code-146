from abc import ABCMeta, abstractmethod
from typing import List
from .configuration import Configuration
from .sink_serializer import SinkSerializer

class Sink(metaclass = ABCMeta):
    client = None    
    buffer = []
    
    @abstractmethod
    def __init__(self, configuration: Configuration, serializer: SinkSerializer):
        self.configuration = configuration
        self.serializer = serializer
    
    @abstractmethod
    def push(self, element: dict) -> bool:
        """This method serializes the element and pushes to the sink buffer.
        It also calls 'trigger' when the 'trigger_condition' is met.

        Args:
            element (dict): Element of type dict.
        """
        pass
    
    @abstractmethod
    def bulk_push(self, serialized_elements: List[dict]) -> bool:
        """This method pushes the elements into the Sink's client.
        This method is called via 'trigger' function.

        Args:
            serialized_elements (List[dict]): List of serialized elements.

        Returns:
            bool: Returns True if successfull.
        """
        pass
    
    @abstractmethod
    def trigger_condition(self) -> bool:
        """This method returns True if the trigger condition is met otherwise false.

        Returns:
            bool: Returns True if the trigger condition is met otherwise false.
        """
        pass

        
    @abstractmethod
    def trigger(self):
        """This method is used to trigger the 'bulk_push' method of the sink.
        NOTE: This should only be called if the trigger_condition is met.
        """
        pass