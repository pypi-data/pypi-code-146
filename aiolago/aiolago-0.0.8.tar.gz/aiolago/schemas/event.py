import time
import uuid
from typing import Optional, Type, List
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty, Field

__all__ = [
    'BillableMetric',
    'BillableMetricResponse',
    'BillableMetricRoute',
]

def transaction_id():
    return str(uuid.uuid4())

class Event(BaseResource):
    transaction_id: str = Field(default_factory = transaction_id)
    external_customer_id: Optional[str]
    external_subscription_id: Optional[str]
    code: str
    timestamp: Optional[int] = Field(default_factory = time.time)
    properties: Optional[dict]


class BatchEvent(BaseResource):
    transaction_id: str = Field(default_factory = transaction_id)
    external_customer_id: Optional[str]
    external_subscription_ids: List[str]
    code: str
    timestamp: Optional[int]
    properties: Optional[dict]


class EventResponse(BaseResource):
    lago_id: str
    transaction_id: str
    external_customer_id: Optional[str]
    lago_customer_id: Optional[str]
    lago_subscription_id: Optional[str]
    external_subscription_id: Optional[str]
    code: str
    timestamp: str
    properties: Optional[dict]
    created_at: str


class EventRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Event
    response_model: Optional[Type[BaseResource]] = EventResponse
    usage_model: Optional[Type[BaseResource]] = None
    
    @lazyproperty
    def api_resource(self):
        return 'events'
    
    @lazyproperty
    def root_name(self):
        return 'event'
    
    def batch_create(
        self, 
        input_object: BatchEvent,
        return_response: bool = False,
        **kwargs
    ):
        """
        Batch Create Resources

        :param input_object: Input Object to Create
        :param return_response: Return the Response Object
        """
        return super().batch_create(
            input_object=input_object,
            return_response=return_response,
            **kwargs
        )
    
    async def async_batch_create(
        self, 
        input_object: BatchEvent,
        return_response: bool = False,
        **kwargs
    ):
        """
        Batch Create Resources

        :param input_object: Input Object to Create
        :param return_response: Return the Response Object
        """
        return await super().async_batch_create(
            input_object=input_object,
            return_response=return_response,
            **kwargs
        )

