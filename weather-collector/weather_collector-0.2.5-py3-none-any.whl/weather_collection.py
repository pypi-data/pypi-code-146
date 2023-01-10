"""
Define the collector function for the API collection 

:author: Julian M. Kleber
"""
from typing import Type

from bulkhead.endpoint_collection.endpoint_collection import EndpointCollection

from weather_collector.weather_endpoints import (
    EndpointOpenWeatherMap,
    EndpointTomorrowIO,
    EndpointWeatherAPI,
)


class WeatherEndpointCollection(EndpointCollection):
    """Interface for orchestration of different weather endpoints.

    :author: Julian M. Kleber
    """


def get_collection() -> Type[WeatherEndpointCollection]:
    """
    The get_collection function takes in a longitude, latitude, and value_name.
    It then creates an endpoint collection with two endpoints: OpenWeatherMap and TomorrowIO.
    The function returns the endpoint collection.

    :param lon:float: Used to Specify the longitude of a location.
    :param lat:float: Used to Specify the latitude of the location.
    :param value_name:str: Used to Specify the value to be returned.
    :return: A weatherendpointcollection object.

    :doc-author: Julian M. Kleber
    """

    owp_endpoint = EndpointOpenWeatherMap()
    tmio_endpoint = EndpointTomorrowIO()
    weather_api_endpoint = EndpointWeatherAPI()
    endpoint_list = [owp_endpoint, tmio_endpoint, weather_api_endpoint]
    endpoint_coll = WeatherEndpointCollection(endpoint_list)

    return endpoint_coll
