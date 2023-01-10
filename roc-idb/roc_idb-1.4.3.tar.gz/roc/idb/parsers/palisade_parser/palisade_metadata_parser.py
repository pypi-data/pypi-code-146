#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.logger import logger
from .base_palisade_parser import BasePALISADEParser

__all__ = [
    'PALISADEMetadataParser',
]


class PALISADEMetadataParser(BasePALISADEParser):
    """
    Class used for the parsing of the XML of the IDB (PALISADE) to get only the PALISADE metadata
    """

    def parse(self):
        """
        Call the load palisade method
        """

        self.load_palisade_metadata()

    def load_palisade_metadata(self):
        """
        Load the palisade metadata map

        :return:
        """

        # search for packets in the given node
        for packet_node in self._findall(
            self.root, './/{0}PacketDefinition', '',
        ):
            # get the name of the packet
            palisade_id = packet_node.attrib['Name']

            # search for the SRDB id of the packet
            if palisade_id[:2] not in ['TM', 'TC']:
                logger.warning('Skipping packet %s' % palisade_id)
                continue
            elif palisade_id in self.palisade_to_srdb_id[palisade_id[:2]]:
                # keep reference to mapping
                info = self.packets_mapping[palisade_id]

            else:
                logger.error(
                    (
                        'Packet {0} not found in PALISADE. Maybe an internal DPU'
                        + ' command ?'
                    ).format(palisade_id)
                )
                continue

            # get the type of the packet
            packet_type_node = self._find(
                packet_node,
                ".//{0}Param[@StructParamIDRef='PACKET_TYPE']",
                '',
            )
            if packet_type_node is None:
                # the packet doesn't have a type, so don't analyze it
                logger.warning(
                    (
                        "Packet {0} doesn't have a type. Surely an internal "
                        + 'command of the DPU.'
                    ).format(palisade_id)
                )
                continue
            else:
                packet_type = packet_type_node.attrib['Value'][:2]

            # get the palisade category
            palisade_category = self.get_palisade_category(packet_node)

            # compute the long srdb id
            srdb_id = self.compute_packet_srdbid(packet_type, info['SRDBID'])

            # store the palisade id and the palisade category indexed by the srdb id
            self.palisade_metadata_map[srdb_id] = {
                'palisade_id': palisade_id,
                'palisade_category': palisade_category,
            }
