"""Endpoint interface.

:author: Julian M. Kleber
"""
import os
from typing import Any, Dict, Tuple, Optional
from abc import ABC, abstractmethod
import http.client

from dotenv import load_dotenv


from bulkhead.endpoint.interface import Endpoint

load_dotenv()


class EndpointWeather(Endpoint, ABC):
    """Interface for Endpoints dedicated to Weather.

    :author: Julian M. Kleber
    """

    def __init__(self) -> None:
        self._key: Optional[str]
        self._url: Optional[str]
        self._field_dict: Dict[str, Tuple[str, str]]

    def get_value(self, **kwargs: int | str) -> Any:
        """The get_cloud_cover function takes in a longitude, latitude, and
        interval. The function then uses the request function to make a REST
        call to a Weather API defined by the EndpointObject through the
        connection string (make_conn_str method). The response is parsed using
        the parse_request function and returned as an integer.

        :param lon:float: Used to pass the longitude value to the function.
        :param lat:float: Used to specify the latitude of the location you want
                           to get weather data for.
        :param interval:int: Used to determine the time interval in which to
                             get the cloud cover data.
        :return: The cloud value.

        :doc-author: Julian M. Kleber
        """
        value_name = str(kwargs["value_name"])
        lon = float(kwargs["lon"])
        lat = float(kwargs["lat"])

        parsing_func = self.get_method(self._field_dict[value_name][1])

        req_value = self.parse_request(
            self.request(lon=lon, lat=lat, value_name=value_name),
            parsing_func=parsing_func,
        )
        if req_value is not None:
            setattr(self, value_name, req_value)
        return req_value

    def request(self, **kwargs: str | float) -> Dict[str, Any]:
        """The request function takes in a value, longitude, latitude and
        interval. It then makes an HTTPS connection to the url provided by the
        user. A conn_str is created using make_conn_str function which takes in
        a value, longitude, latitude and key (which are all passed into this
        function). The conn object then requests GET with the conn_str as its
        path parameter and payload as its body parameter. The response from
        that request is stored in dict format using get_dict response function.

        :param value:str: Used to specify the type of data you want to get from the api.
        :param lon:float: Used to specify the longitude of the location.
        :param lat:float: Used to specify the latitude of the location.
        :param interval:float: Used to Specify the time interval between each request.
        :return: A dictionary.

        :doc-author: Julian M. Kleber
        """

        value_name_api = self._field_dict[str(kwargs[str("value_name")])][0]
        conn: http.client.HTTPSConnection
        conn = http.client.HTTPSConnection(str(self._url))

        conn_str = self.make_conn_str(
            value_name=value_name_api,
            lon=int(kwargs["lon"]),
            lat=int(kwargs["lat"]),
            key=self._key,
        )
        conn.request(
            method="GET",
            url=conn_str,
        )

        dict_response = self.get_dict_response(conn=conn)
        return dict_response

    @abstractmethod
    def parse_request_cc(self, response: Dict[str, Any]) -> int:
        """
        The parse_request_cc function takes in a response from the API and returns an integer.
                The function takes in a dictionary of type Dict[str, Any] as its only argument.
                The function returns an integer.

        :param self: Used to Represent the instance of a class.
        :param response:Dict[str: Used to Pass the response from the request
                                  to a dictionary.
        :param Any]: Used to Specify that the response is a dictionary with any
                     type of key and value.
        :return: The status code of the response.

        :doc-author: Trelent
        """

        pass  # pragma: no cover

    @abstractmethod
    def make_conn_str(
        self, value_name: str, lon: float, lat: float, key: Optional[str]
    ) -> str:
        """
        The make_conn_str function takes a value name, longitude, latitude and key (optional)
        and returns a connection string. The function is used to create the connection string for
        the database that will be queried.

        :param value_name:str: Used to Specify the name of the value that you want to get.
        :param lon:float: Used to Specify the longitude of the location you want to get
        weather data for.
        :param lat:float: Used to Specify the latitude value.
        :param key:Optional[str]: Used to Specify whether the key is optional or not.
        :return: A string.

        :doc-author: Julian M. Kleber
        """

        pass  # pragma: no cover


class EndpointOpenWeatherMap(EndpointWeather):
    """Class implementing the OpenWeatherMap API endpoint dedicated for
    extracting cloud cover.

    :author: Julian M. Kleber
    """

    def __init__(
        self,
    ) -> None:  # Redundant constructor ensures you don't forget to define the neccessary values

        super().__init__()

        if os.getenv("OpenWeatherMapKey") is not None:
            self._key = os.getenv("OpenWeatherMapKey")
        else:
            self._key = "No Key"
        if os.getenv("OpenWeatherMapURL") is not None:
            self._url = os.getenv("OpenWeatherMapURL")
        else:
            self._url = "No url"
        self._field_dict = {
            "cloud_cover": ("weather", "parse_request_cc"),
            "solar_radiation": ("solar_radiation", "parse_request_sr"),
        }

    def parse_request_cc(self, response: Dict[str, Any]) -> int:
        return int(response["clouds"]["all"])

    def make_conn_str(
        self, value_name: str, lon: float, lat: float, key: Optional[str]
    ) -> str:
        conn_str = f"/data/2.5/{value_name}?&lat={lat}&lon={lon}&APPID={key}"
        return conn_str


class EndpointTomorrowIO(EndpointWeather):
    """Class implementing the OpenWeatherMap API endpoint dedicated for
    extracting cloud cover.

    :author: Julian M. Kleber
    """

    def __init__(
        self,
    ) -> None:  # Redundant constructor ensures you don't forget to define the neccessary values
        super().__init__()
        self._key = os.getenv("TomorrowIOKey")
        self._url = os.getenv("TomorrowIOURL")
        self._field_dict = {
            "cloud_cover": ("cloudCover", "parse_request_cc"),
            "solar_radiation": ("solarRadiation", "parse_request_sr"),
        }

    def parse_request_cc(self, response: Dict[str, Any]) -> int:
        return int(
            response["data"]["timelines"][0]["intervals"][0]["values"]["cloudCover"]
        )

    def make_conn_str(
        self, value_name: str, lon: float, lat: float, key: Optional[str]
    ) -> str:

        # lon lat reversed to OWM
        conn_str = f"/v4/timelines?location={lat}%2C{lon}&fields={value_name}&timesteps=current&units=metric&apikey={key}"
        return conn_str


class EndpointWeatherAPI(EndpointWeather):
    """
    Class implementing the WeatherCom Endpoint

    :author: Julian M. Kleber
    """

    def __init__(
        self,
    ) -> None:  # Redundant constructor ensures you don't forget to define the neccessary values
        super().__init__()
        self._key = os.getenv("WeatherComKey")
        self._url = os.getenv("WeatherComURL")
        self._field_dict = {
            "cloud_cover": ("cloudCover", "parse_request_cc"),
        }

    def parse_request_cc(self, response: Dict[str, Any]) -> int:
        """
        The parse_request_cc function takes in a response from the WeatherAPI API and
        returns an integer value for cloud cover.


        :param self: Used to Refer to the class instance.
        :param response:Dict[str: Used to Specify the type of data that is being passed in.
        :param Any]: Used to Specify that the function can take any data type as a parameter.
        :return: The cloud cover value from the first interval in the first timeline.

        :doc-author: Trelent
        """
        return int(response["current"]["cloud"])

    def make_conn_str(self, lon: float, lat: float, key: str, value_name: str) -> str:
        """
        The make_conn_str function takes in a longitude, latitude, and API key.
        It then returns a string that can be used to make an HTTPS request to the WeatherAPI API.

        :param lon:float: Used to Get the longitude of a location.
        :param lat:float: Used to Specify the latitude of the location.
        :param key:str: Used to Pass in the api key.
        :return: A string that can be used to connect to the api.

        :doc-author: Julian M. Kleber
        """

        # please note that the order of lon lat is different to other endpoints
        conn_str = f"/v1/current.json?key={key}&q={lat},{lon}&aqi=no"
        return conn_str
