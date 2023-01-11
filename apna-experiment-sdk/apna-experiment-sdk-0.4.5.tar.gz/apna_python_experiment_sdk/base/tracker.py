from abc import ABCMeta, abstractmethod
from typing import Dict, List
from .configuration import Configuration
from .sink import Sink

class Tracker(metaclass = ABCMeta):
    client = None
    
    @abstractmethod
    def __init__(
        self, experiment_client_name: str, experiment_client_conf: Configuration, sinks: List[Sink]):
        pass
    
    @abstractmethod
    def is_enabled(self, feature_name: str, context: Dict[str, str], track: bool = False) -> bool:
        """This method returns whether a feature is enabled or not for the given context.

        Args:
            feature_name (str): Name of the feature (experiment).
            context (Dict[str, str]): Context to pass in the experimentation client.
            track (bool, optional): This flags determine whether to push to sink or not. Defaults to False.            

        Returns:
            bool: Returns true if the feature is enabled else false.
        """
        
    @abstractmethod
    def get_variant(self, feature_name: str, context: Dict[str, str], track: bool = True) -> bool:
        """This method returns variant associated for the feature for the given context.
        NOTE: Call this method only if the is_enabled has returned true otherwise NotFoundException will
        be raised.

        Args:
            feature_name (str): Name of the feature (experiment).
            context (Dict[str, str]): Context to pass in the experimentation client.
            track (bool, optional): This flags determine whether to push to sink or not. Defaults to True.            

        Returns:
            bool: Returns true if the feature is enabled else false.
        """
        
    def _track(self, data: dict) -> None:
        """This means pushes the data into the sinks.

        Args:
            data (dict): The variant which is recevied from the experiment client.
        """
        for sink in self.sinks:
            sink.push(data)