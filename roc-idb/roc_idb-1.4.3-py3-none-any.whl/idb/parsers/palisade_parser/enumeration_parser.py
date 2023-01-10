#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from roc.idb.parsers.idb_elements import Enumeration

__all__ = [
    'EnumerationParser',
]


class EnumerationParser:
    """
    Mixin class used to parse enumerations
    """

    def populate_enumerations(self):
        """
        Search in the root node enumeration definitions and populate it with
        information from the IDB.
        """
        # find the node for the definition of the enumeration
        nodes = self._findall(self.root, './/{0}EnumDefinition', '',)

        # loop over nodes and create enumeration
        for node in nodes:
            palisade_id = node.attrib['ID']

            for packet_type in ['TM', 'TC']:
                # get the srdb_id from the palisade_id and the packet type if any
                # if it's an internal enum (with no srdb id), replace the srdb_id by the palisade id
                srdb_id = self.palisade_to_srdb_id[packet_type].get(
                    palisade_id, palisade_id
                )

                if srdb_id is None:
                    continue

                enumeration = Enumeration(srdb_id)

                # get some information from the node
                enumeration.data_type = node.attrib['Type']
                enumeration.values = {
                    value_entry.attrib['ID']: int(
                        value_entry.attrib['NumValue'], 0
                    )
                    for value_entry in self._findall(node, './/{0}Value', '')
                }
                # check for recursive enumeration
                enumeration.values = [
                    Enumeration(
                        self.palisade_to_srdb_id[packet_type].get(
                            enum_entry.attrib['IDRef'],
                            enum_entry.attrib['IDRef'],
                        )
                    )
                    for enum_entry in self._findall(node, './/{0}Enum', '')
                ]
