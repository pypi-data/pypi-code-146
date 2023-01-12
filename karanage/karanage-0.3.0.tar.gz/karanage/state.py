#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
import enum
import requests
import json
from typing import Dict, Optional
from .connection import KaranageConnection
from .exception import KaranageException

class StateSystem(enum.Enum):
    OK = "OK"
    FAIL = "FAIL"
    DOWN = "DOWN"

## Generic karanage sending system.
class KaranageState:
    def __init__(self, connection: KaranageConnection) -> None:
        """ 
        @brief Initialize the communication class.
        @param[in] connection Connection interface.
        """
        self.connection = connection
    
    def get_url(self, service: str, topic: Optional[str] = None):
        if topic is None:
            return self.connection.get_url(service)
        return f"{self.connection.get_url(service)}/{topic}"
    
    def send(self, topic: str, data: Optional[Dict], state: StateSystem = StateSystem.OK) -> None:
        """
        @brief Send a message to the server.
        @param[in] topic Topic where to publish the data.
        @param[in] data: Data to send to the server
        @param[in] state: State of the current system
        """
        if data is None:
            data = {}
        param = {}
        if state is not None:
            param["state"] = state
        header = self.connection.get_header()
        try:
            ret = requests.post(self.get_url("state", topic), json=data, headers=header, params=param)
        except requests.exceptions.ConnectionError as ex:
            raise KaranageException(f"Fail connect server: {self.get_url('state', topic)}", 0, str(ex))
        if 200 <= ret.status_code <= 299:
            pass
        else:
            raise KaranageException(f"Fail send message: {self.get_url('state', topic)}", ret.status_code, ret.content.decode("utf-8"))
    

    def gets(self, topic: Optional[str] = None, since: Optional[str] = None) -> Dict:
        """
        @brief Get all the topic fom the server.
        @param since ISO1866 time value.
        @return A dictionnary with the requested data.
        """
        param = { }
        header = self.connection.get_header()
        if since is not None:
            param["since"] = since
        ret = requests.get(self.get_url("state", topic), headers=header, params=param)
        #print(ret.content.decode('utf-8'))
        if 200 == ret.status_code:
            return json.loads(ret.content.decode('utf-8'))
        raise KaranageException(f"Fail get data: {self.get_url('state', topic)}", ret.status_code, ret.content.decode("utf-8"))

    def get_history(self, topic: Optional[str] = None, since: Optional[str] = None, since_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """
        @brief Get all the topic fom the server.
        @param since ISO1866 time value.
        @param since_id remote BDD index of tje fielf.
        @param limit Number of value we want to get
        @return A dictionnary with the requested data.
        """
        param = { }
        header = self.connection.get_header()
        if since is not None:
            param["since"] = since
        if since_id is not None:
            param["sinceId"] = since_id
        if limit is not None:
            param["limit"] = limit
        ret = requests.get(self.get_url("state_history", topic), headers=header, params=param)
        #print(ret.content.decode('utf-8'))
        if 200 == ret.status_code:
            return json.loads(ret.content.decode('utf-8'))
        raise KaranageException(f"Fail get data: {self.get_url('state_history', topic)}", ret.status_code, ret.content.decode("utf-8"))

