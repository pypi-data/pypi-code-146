# Player properties.
#
# Copyright 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.lib.xmlutil import bool_attrib, str_attrib
import orpg.version
from .roles import *

class Player:
    def __init__(self, name):
        self.id = "0"
        self.name = name
        self.status = ""
        self.typing = False
        self.role = ROLE_LURKER
        self._version = orpg.version.VERSION
        self._protocol_version = orpg.version.PROTOCOL_VERSION
        self._client_string = orpg.version.CLIENT_STRING

    @classmethod
    def from_xml(self, xml_dom=None):
        player = Player("")
        player.update_from_xml(xml_dom)
        return player

    def update_from_xml(self, xml_dom):
        self.id = str_attrib(xml_dom, "id", "0")
        self.name = str_attrib(xml_dom, "name", "")
        self.status = str_attrib(xml_dom, "status", "")
        self.typing = bool_attrib(xml_dom, "typing", False)
        self._version = str_attrib(xml_dom, "version", "(unknown)")
        self._protocol_version = str_attrib(xml_dom, "protocol_version", "(unknown)")
        self._client_string = str_attrib(xml_dom, "client_string", "(unknown)")

    @property
    def version(self):
        return self._version
    
    @property
    def protocol_version(self):
        return self._protocol_version

    @property
    def client_string(self):
        return self._client_string
