#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from poppy.core.generic.metaclasses import Singleton
except:
    print('POPPy framework is not installed!')

__all__ = ['PacketCache']


class PacketCache(metaclass=Singleton):

    def __init__(self):
        # Cache for IDB
        self.idb = {}

        # Cache for packet max_sid values
        self.max_sid = {}

        # Cache for packet_id values
        self.packet_ids = {}

        # Cache for PALISADE metadata query result
        self.palisade_metadata_query = {}

        # Cache for PALISADE metadata dictionary
        self.palisade_metadata_dict = {}

        # Cache for latest PALISADE IDB version
        self.latest_palisade_version = None

        # Cache for transfer function
        self.transfer_function = {}
