from typing import Dict, Type

from aiohttp import ClientSession
from uplink import AiohttpClient, Consumer

from aiotraxx.controllers import Sensors



class TraxxClient:
    """Declaritive interface for an HTTP inSight client."""
    consumers: Dict[str, Consumer] = {}

    def __init__(self, session: ClientSession) -> None:
        self.session = session

    @property
    def sensors(self) -> Sensors:
        return self._get_consumer_instance(Sensors)
    
    def _get_consumer_instance(self, consumer: Type[Consumer]) -> Consumer:
        """Get an instance of the consumer for the a controller.
        
        This caches the consumer instance in the class for reuse.
        """
        name = consumer.__name__
        if name in self.consumers:
            return self.consumers[name]
        instance = consumer(client=AiohttpClient(session=self.session))
        self.consumers[name] = instance
        return instance