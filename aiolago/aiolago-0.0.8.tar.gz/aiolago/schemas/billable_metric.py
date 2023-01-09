from typing import Optional, Type, List, Dict, Any, Union
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'BillableMetric',
    'BillableMetricResponse',
    'BillableMetricRoute',
]


class BillableMetricGroupValue(BaseResource):
    name: Optional[str]
    key: Optional[str]
    values: Optional[List[str]]


class BillableMetricGroup(BaseResource):
    key: Optional[str]
    values: List[BillableMetricGroupValue]


class BillableMetric(BaseResource):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]
    group: Optional[Union[BillableMetricGroup, Dict]]


class BillableMetricResponse(BaseResource):
    lago_id: str
    name: str
    code: str
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]
    created_at: str
    group: Optional[Union[BillableMetricGroup, Dict]]


class MetricGroup(BaseResource):
    lago_id: Optional[str]
    key: Optional[str]
    value: Optional[str]

class MetricGroupResponse(BaseResource):
    groups: Optional[List[MetricGroup]]

class BillableMetricRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = BillableMetric
    response_model: Optional[Type[BaseResource]] = BillableMetricResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'billable_metrics'

    @lazyproperty
    def root_name(self):
        return 'billable_metric'
    
    def get_groups(
        self, 
        resource_id: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Type[MetricGroupResponse]:
        """
        Fetch all the groups for a given metric
        
        :param resource_id:
        :param params:
        :param kwargs:
        :return:
        """
        api_resource = f'{self.api_resource}/{resource_id}/groups'
        api_response = self._send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = self.headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data, response_object = MetricGroupResponse)
    

    async def async_get_groups(
        self, 
        resource_id: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Type[MetricGroupResponse]:
        """
        Fetch all the groups for a given metric
        
        :param resource_id:
        :param params:
        :param kwargs:
        :return:
        """
        api_resource = f'{self.api_resource}/{resource_id}/groups'
        api_response = await self._async_send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = self.headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data, response_object = MetricGroupResponse)
    


