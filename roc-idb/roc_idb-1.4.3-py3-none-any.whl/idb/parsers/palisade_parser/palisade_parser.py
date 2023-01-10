#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .enumeration_parser import EnumerationParser
from .packet_parser import PacketParser
from .parameter_parser import ParameterParser
from .tf_parser import TFParser
from .base_palisade_parser import BasePALISADEParser

__all__ = [
    'PALISADEParser',
]


class PALISADEParser(
    BasePALISADEParser,
    ParameterParser,
    EnumerationParser,
    PacketParser,
    TFParser,
):
    """
    Class used for the parsing of the XML of the IDB (PALISADE) to get information on the
    IDB and SRDB.
    """

    def parse(self):
        """
        Call all methods to the necessary information from the IDB and SRDB
        mapping in XML files specified in arguments.
        """

        # create the mapping for packets
        self.get_structures()

        # populate enumerations
        self.populate_enumerations()

        # populate information of parameters
        self.populate_parameters()

        # create packets
        self.create_packets_idb()

        # create TF packets
        self.create_tf()
