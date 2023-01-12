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

## Generic karanage sending system.
class KaranageLog:
    def __init__(self, connection: KaranageConnection, system: Optional[str] = None) -> None:
        """ 
        @brief Initialize the communication class.
        @param[in] connection Connection interface.
        """
        self.connection = connection
        self.system = system
        self.service = "log"
    
    def get_url(self):
        if self.system is None:
            return self.connection.get_url(self.service)
        return f"{self.connection.get_url(self.service)}/{self.system}"
    
    def send(self, system: str, data: Dict, id: int = None) -> None:
        """
        @brief Send a message to the server.
        @param[in] system system where to publish the data.
        @param[in] data: Data to send to the server
        @param[in] id: Local internal ID
        """
        param = {}
        if id is not None:
            param["id"] = id
        header = self.connection.get_header()
        try:
            ret = requests.post(self.get_url(), json=data, headers=header, params=param)
        except requests.exceptions.ConnectionError as ex:
            raise KaranageException(f"Fail connect server: {self.get_url('state', system)}", 0, str(ex))
        if 200 <= ret.status_code <= 299:
            pass
        else:
            raise KaranageException(f"Fail send message: {self.get_url('state', system)}", ret.status_code, ret.content.decode("utf-8"))
    