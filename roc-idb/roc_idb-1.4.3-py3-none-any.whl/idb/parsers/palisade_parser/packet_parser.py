#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.logger import logger
from roc.idb.parsers.idb_elements import Packet, ParameterDefinition, Parameter

__all__ = [
    'PacketParser',
]


class PacketParser:
    """
    Mixin class used to parse packets
    """

    def create_packets_idb(self):
        """
        Create all packets defined in the IDB.
        """
        self.create_packets(self.root)

    def create_packets(self, node):
        """
        Create packets from the packet definitions encountered in the given
        node.
        """
        # prepare the enumeration table

        enumeration_table = dict()

        for enumeration_entry in self._findall(
            self.root, './/{0}EnumDefinition', ''
        ):

            # get the enumeration id
            enumeration_id = enumeration_entry.attrib['ID']

            for value_entry in self._findall(
                enumeration_entry, './/{0}Value', ''
            ):

                table_key = enumeration_id + '/' + value_entry.attrib['ID']

                # Check if the ID is already used. If not create a new
                # dictionary to store parent IDs otherwise, add a new key to
                # the dictionary
                if enumeration_table.get(value_entry.attrib['ID']) is None:
                    enumeration_table[value_entry.attrib['ID']] = dict(
                        [
                            (
                                enumeration_id,
                                int(value_entry.attrib['NumValue'], 0),
                            )
                        ]
                    )
                else:
                    enumeration_table[value_entry.attrib['ID']][
                        enumeration_id
                    ] = int(value_entry.attrib['NumValue'], 0)

                # NumValue can be both decimal and hex values but with the 0x
                # prefix, Python can distinguish hex and decimal automatically
                # We must specify 0 as the base in order to invoke this
                # prefix-guessing behavior

        # prepare the dict of structured that may be included in packets

        structure_nodes = {
            structure_node.attrib['ID']: structure_node
            for structure_node in self._findall(
                self.root, './/{0}StructDefinition', ''
            )
        }

        struct_param_id_ref_map = {
            param_node.attrib['StructParamIDRef']: param_node.attrib['Value']
            for param_node in self._findall(
                self.root, './/{0}Param[@StructParamIDRef]', ''
            )
        }

        # search for packets in the given node
        for packet_node in self._findall(node, './/{0}PacketDefinition', '',):
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
            packet_type = self._find(
                packet_node,
                ".//{0}Param[@StructParamIDRef='PACKET_TYPE']",
                '',
            )
            if packet_type is None:
                # the packet doesn't have a type, so don't analyze it
                logger.warning(
                    (
                        "Packet {0} doesn't have a type. Surely an internal "
                        + 'command of the DPU.'
                    ).format(palisade_id)
                )
                continue
            else:
                pack_type = packet_type.attrib['Value'][:2]

            # create the object of the packet
            packet = Packet(
                palisade_id, info['SRDBID'], packet_node, type=pack_type,
            )

            packet.spid = info['SPID'] if 'SPID' in info else None

            # get the engineering values for the category, type, subtype, sid
            # and pid

            # get the packet category
            packet.category_eng = self._find(
                packet_node,
                ".//{0}Param[@StructParamIDRef='PACKET_CATEGORY']",
                '',
            ).attrib['Value']

            # get the packet service_type
            packet.service_type_eng = self._find(
                packet_node,
                ".//{0}Param[@StructParamIDRef='SERVICE_TYPE']",
                '',
            ).attrib['Value']

            # get the packet service_subtype
            packet.service_subtype_eng = self._find(
                packet_node,
                ".//{0}Param[@StructParamIDRef='SERVICE_SUBTYPE']",
                '',
            ).attrib['Value']

            # get the packet pid
            pid_node = self._find(
                packet_node, ".//{0}Param[@StructParamIDRef='PROCESS_ID']", ''
            )

            packet.pid_eng = (
                pid_node.attrib['Value'] if pid_node is not None else None
            )

            # now get the raw values using the enumeration mapping table

            # extract the key, value tuple from the mapping table and manage
            # cases where there are 0 or more than 1 elements for the given
            # key.

            # Packet category can't be NULL

            ((_, packet.category),) = enumeration_table[
                packet.category_eng
            ].items()

            if packet.pid_eng is not None:
                ((_, packet.pid),) = enumeration_table[packet.pid_eng].items()
            else:
                packet.pid = None

            if packet.service_type_eng is not None:
                ((_, packet.service_type),) = enumeration_table[
                    packet.service_type_eng
                ].items()
            else:
                packet.service_type = None

            if packet.service_subtype_eng is not None:
                if len(enumeration_table[packet.service_subtype_eng]) == 1:
                    ((_, packet.service_subtype),) = enumeration_table[
                        packet.service_subtype_eng
                    ].items()
                else:
                    packet.service_subtype = enumeration_table[
                        packet.service_subtype_eng
                    ]['SERVICE_SUBTYPE_' + packet.service_type_eng]
            else:
                packet.service_subtype = None

            # get the description of the packet
            packet.description = self._find(
                packet_node, '{0}Description', ''
            ).text

            # get the palisade category
            palisade_category = self.get_palisade_category(packet_node)

            # compute the long srdb id
            srdb_id = self.compute_packet_srdbid(pack_type, info['SRDBID'])

            # store the palisade id and the palisade category indexed by the srdb id
            self.palisade_metadata_map[srdb_id] = {
                'palisade_id': palisade_id,
                'palisade_category': palisade_category,
            }

            # create parameters in relation with the packet
            packet.parameters = self.create_parameters_from_packet(packet)

        return enumeration_table

    def _get_sid_from_structure(self, current_node, parameter):
        param_node = self._find(
            current_node,
            ".//{0}Parameter[@IDRef='%s']" % parameter.definition.palisade_id,
            '',
        )

        if param_node is None:
            param_node = self._find(
                current_node,
                ".//{0}Param[@StructParamIDRef='%s']"
                % parameter.definition.palisade_id,
                '',
            )

        if parameter.alias is not None and param_node is None:
            param_node = self._find(
                current_node,
                ".//{0}Param[@StructParamIDRef='%s']" % parameter.alias,
                '',
            )
        sid_eng = None

        if param_node is None:
            for child in current_node:
                # if the child is a structure
                if child.tag == self.struct_tag:
                    struct_sid = self._get_sid_from_structure(
                        self.structures[child.attrib['IDRef']], parameter
                    )
                else:
                    struct_sid = self._get_sid_from_structure(child, parameter)
                if struct_sid is not None:
                    sid_eng = struct_sid
        else:
            sid_eng = param_node.attrib.get('ForceValue')
            if sid_eng is None:
                sid_eng = param_node.attrib.get('Value')
        return sid_eng

    def _get_packet_sid(self, packet, parameter):
        """
        Get the packet sid from the sid parameter
        """
        param_node = self._find(
            packet.node,
            ".//{0}Parameter[@IDRef='%s']" % parameter.definition.palisade_id,
            '',
        )

        # if None check for struct tag
        sid_eng = None

        if param_node is None:
            sid_eng = self._get_sid_from_structure(
                self._find(
                    packet.node, ".//{0}Field[@Name='SOURCE_DATA']", ''
                ),
                parameter,
            )

        else:
            sid_eng = param_node.attrib.get('ForceValue')
        try:
            return sid_eng, parameter.definition.data_type.values[sid_eng]
        except KeyError as e:
            logger.error(
                'SID tag found but no value found for the packet '
                + repr(packet)
            )
            return None, None

    def create_parameters_from_packet(self, packet):
        """
        Create parameters associated to a packet with all necessary
        information extracted from the IDB and mapping with SRDB.
        """
        # initialize some parameters for tracking of information
        self.bit_cursor = 0

        # get the parameters from the XML file by recursively parsing nodes
        parameters, _, _ = self._parameters_from_node(
            packet.node, packet.type,
        )

        sid_parameters = [
            parameter for parameter in parameters if parameter.is_sid
        ]

        sid_list_len = len(sid_parameters)

        if sid_list_len == 0:
            logger.debug('No SID for the packet %s' % packet)
        elif sid_list_len == 1:
            logger.debug('SID parameter for the packet %s' % packet)
            packet.sid_eng, packet.sid = self._get_packet_sid(
                packet, sid_parameters[0]
            )
        else:
            raise RuntimeError(
                'Multiple SID detected for the packet %s' % packet
            )

        # store the information of the packet size in bytes. This necessary
        # because parameters are not sufficient for this, since sometimes
        # packets have a spare at the end of the packet, and verifying the size
        # of the packet with the last parameter is not sufficient
        if self.bit_cursor % 8 != 0:
            # in case the size is not a multiple of a byte, we have a problem
            # and inform the user
            logger.error(
                (
                    'The length of {0} packet is not a byte multiple. '
                    + 'Problem in parsing the IDB.'.format(packet.name)
                )
            )
        packet.byte_size = self.bit_cursor // 8

        # return parameters
        return parameters

    def _parameters_from_node(self, node, packet_type):
        """
        Given a node, search recursively for parameters in structure node if
        present and in the node itself.
        """
        # an empty set of parameters
        parameters = list()

        # block size of parameters and spare inside the node
        block_size = 0

        # store the value of the sid and sid_eng if it exists
        packet_sid = None

        # loop over child nodes
        for child in node:
            sid_value = None
            # if the child is a structure
            if child.tag == self.struct_tag:
                # get the structures definition node
                struct_node = self.structures[child.attrib['IDRef']]

                # get the parameters from this node
                params, bsize, sid_value = self._parameters_from_node(
                    struct_node, packet_type,
                )
                parameters += params
                block_size += bsize

            # if we have a spare, the bit cursor needs to be moved of the value
            # specified in the spare tag
            elif child.tag == self.spare_tag:
                # get the unit
                unit = child.attrib['Size']
                # in bit units
                if unit == 'Bit':
                    bits = int(child.attrib['Count'])
                    self.bit_cursor += bits
                    block_size += bits
                elif unit == 'Byte':
                    bits = int(child.attrib['Count']) * 8
                    self.bit_cursor += bits
                    block_size += bits

            # if the tag is a loop, this is the case of parameters inside a
            # block and we need to loop on the packet to get the wanted
            # information
            elif child.tag == self.loop_tag:
                # get parameters inside the loop tag
                params, bsize, sid_value = self._parameters_from_node(
                    child, packet_type
                )
                block_size += bsize

                # set the group size to the number of parameters
                group_size = len(params)

                # set the counter value if not a parameter name
                count = child.attrib['Count']
                if not count.startswith('PARAM:'):
                    counter = int(child.attrib['Count'])
                else:
                    counter = 0

                # loop over parameters for setting the group size
                for param in params:
                    param.group_size = group_size
                    param.block_size = bsize // 8  # in bytes
                    param.group_counter = counter

                # add parameters
                parameters += params

            # if the child is a parameter
            elif child.tag == self.param_tag:
                # get the name of the parameter
                palisade_id = child.attrib['IDRef']
                srdb_id = self.palisade_to_srdb_id[packet_type][palisade_id]

                # get info on the packet from the IDB
                definition = ParameterDefinition.manager[srdb_id]

                # create a parameter for storing information
                parameter = Parameter(definition, packet_type)

                # store the byte position and bit position inside the byte
                parameter.byte_position = self.bit_cursor // 8
                parameter.bit_position = self.bit_cursor % 8

                # increment the byte position with the size of the parameter
                # and store it
                self.bit_cursor += definition.data_type.bit_length
                block_size += definition.data_type.bit_length

                # add the parameter to the set
                parameters.append(parameter)

            # if something else, search in it to see if a parameter is present
            else:
                params, bsize, sid_value = self._parameters_from_node(
                    child, packet_type,
                )
                if child.attrib.get('TAG') == 'SID':
                    if len(params) == 1:
                        params[0].is_sid = True
                        params[0].alias = child.attrib.get(
                            'OptionalStructParamID'
                        )
                    else:
                        raise RuntimeError(
                            'SID parameters are supposed to'
                            + ' be alone in the structure tag'
                        )
                parameters += params
                block_size += bsize

            if sid_value is not None:
                packet_sid = sid_value

        # return parameters
        return parameters, block_size, packet_sid
