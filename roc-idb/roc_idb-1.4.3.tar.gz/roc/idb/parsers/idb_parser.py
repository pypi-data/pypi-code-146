#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import os.path as osp
import xml.etree.ElementTree as ET

from poppy.core.logger import logger

from .idb_elements import Time, SimpleType

__all__ = [
    'IDBParser',
]


class XMLParser(object):
    """
    Base class for XML parsers.
    """

    @staticmethod
    def parse_and_get_ns(filename):
        events = 'start', 'start-ns'
        root = None
        ns = {}
        for event, elem in ET.iterparse(filename, events):
            if event == 'start-ns':
                if elem[0] in ns and ns[elem[0]] != elem[1]:
                    # NOTE: It is perfectly valid to have the same prefix refer
                    #     to different URI namespaces in different parts of the
                    #     document. This exception serves as a reminder that this
                    #     solution is not robust.    Use at your own peril.
                    raise KeyError(
                        'Duplicate prefix with different URI found.'
                    )
                ns[elem[0]] = '{%s}' % elem[1]
            elif event == 'start':
                if root is None:
                    root = elem
        return ET.ElementTree(root), ns


class IDBParser(XMLParser):
    """
    Base class for IDB parsers.
    """

    def __init__(self, mapping_file_path):
        """
        Store the xml mapping file path and create the mapping dict.
        """
        # mapping file path
        self.mapping_file_path = mapping_file_path

        # mapping tables to link srdb and palisade IDs
        self.srdb_to_palisade_id = {'TM': dict(), 'TC': dict()}
        self.palisade_to_srdb_id = {'TM': dict(), 'TC': dict()}

        logger.debug('Create mapping from the xml file ...')
        self.create_mapping()
        logger.debug('Create mapping from the xml file ... Done')

        # initialize the mib version (First row of the vdf.dat table including tabs)
        self.mib_version = None

    def source(self):
        """
        Return the source of the IDB
        """
        return self._source

    def store_mapping_tree(self):
        """
        Get nodes for the mapping.
        """
        # check that the file exist
        if self.mapping_file_path is None or not osp.isfile(
            self.mapping_file_path
        ):
            logger.error(
                "Mapping {0} doesn't exist".format(self.mapping_file_path)
            )
            raise SystemExit(-1)

        # get the tree and namespace
        self.mapping_tree, self._mapping_ns = self.parse_and_get_ns(
            self.mapping_file_path
        )

        # get the root element
        self.mapping_root = self.mapping_tree.getroot()

    def create_mapping(self):
        """
        From the file of the mapping between SRDB and IDB, create parameters
        and packets ((TM,TC,TF) with the good categories.
        """

        self.store_mapping_tree()

        # -- mapping for packets --

        # init the mapping for packets
        self.packets_mapping = {}

        for packet in self.mapping_root.findall('.//Packets//Map'):
            palisade_id = packet.attrib['PALISADEID']
            # ignore packets which do not start with TM or TC
            packet_type = palisade_id[:2]
            if packet_type not in ['TM', 'TC']:
                logger.warning('Skipping packet %s' % palisade_id)
                continue

            short_srdb_id = packet.attrib['SRDBID']
            srdb_id = self.compute_packet_srdbid(packet_type, short_srdb_id)
            # store the correspondence between srdb and palisade
            self.srdb_to_palisade_id[packet_type][srdb_id] = palisade_id

            # store the other information
            self.packets_mapping[palisade_id] = copy.copy(packet.attrib)

        # -- mapping for parameters --
        parameters = self.mapping_root.find('.//Parameters')

        # init the mapping for parameters
        self.parameters_mapping = {}
        self.parameters_mapping['TM'] = {}
        self.parameters_mapping['TC'] = {}

        # loop of TM and TC parameters
        types = ['TM', 'TC']
        for parameter_type in types:
            # get the node
            node = parameters.find(parameter_type)

            # search normal, global and detailed parameters
            for parameter in node.findall('Normal/Map'):
                palisade_id = parameter.attrib['PALISADEID']
                short_srdb_id = parameter.attrib['SRDBID']
                srdb_id = self.compute_parameter_srdbid(
                    parameter_type, short_srdb_id, 'normal'
                )
                self.srdb_to_palisade_id[parameter_type][srdb_id] = palisade_id

                self.parameters_mapping[parameter_type][palisade_id] = {
                    'SRDBID': short_srdb_id,
                    'kind': 'normal',
                }

            for parameter in node.findall('Global/Map'):
                palisade_id = parameter.attrib['PALISADEID']
                short_srdb_id = parameter.attrib['SRDBID']
                srdb_id = self.compute_parameter_srdbid(
                    parameter_type, short_srdb_id, 'global'
                )
                self.srdb_to_palisade_id[parameter_type][srdb_id] = palisade_id

                self.parameters_mapping[parameter_type][palisade_id] = {
                    'SRDBID': short_srdb_id,
                    'kind': 'global',
                }

            for parameter in node.findall('Detailed/Map'):
                palisade_id = parameter.attrib['PALISADEID']
                short_srdb_id = parameter.attrib['SRDBID']
                srdb_id = self.compute_parameter_srdbid(
                    parameter_type, short_srdb_id, 'detailed'
                )
                self.srdb_to_palisade_id[parameter_type][srdb_id] = palisade_id

                self.parameters_mapping[parameter_type][palisade_id] = {
                    'SRDBID': short_srdb_id,
                    'kind': 'detailed',
                }

        # init mapping for enumerations
        self.enumerations_mapping = {}
        self.enumerations_mapping['TM'] = {}
        self.enumerations_mapping['TC'] = {}

        # node for enumerations
        enumerations = self.mapping_root.find('.//Enumerations')

        # loop for TM and TC enumerations
        for enum_type in types:
            # get the node
            node = enumerations.find(enum_type)

            # search normal, global and detailed enumerations
            for enumeration in node.findall('Map'):
                palisade_id = enumeration.attrib['PALISADEID']
                short_srdb_id = enumeration.attrib['SRDBID']
                srdb_id = self.compute_enumeration_srdbid(
                    enum_type, short_srdb_id,
                )
                self.enumerations_mapping[enum_type][
                    palisade_id
                ] = short_srdb_id

                self.srdb_to_palisade_id[enum_type][srdb_id] = palisade_id

        # -- mapping for TF --
        logger.debug('ENTER TF MAPPING')
        tfs = self.mapping_root.find('.//Calibrations')

        # init the mapping for parameters
        # self.tf_mapping = {}
        # self.tf_mapping["TM"] = {}
        # self.tf_mapping["TC"] = {}

        # loop of TM and TC parameters
        types = ['TM', 'TC']
        for tf_type in types:
            # get the node
            node = tfs.find(tf_type)

            # build the dictionnary srdb : palisade
            for tf in node.findall('Tabulate/Map'):
                palisade_id = tf.attrib['PALISADEID']
                short_srdb_id = tf.attrib['SRDBID']

                srdb_id = self.compute_tf_srdbid(tf_type, short_srdb_id,)

                self.srdb_to_palisade_id[tf_type][srdb_id] = palisade_id

        logger.debug('CREATE MAPPING TABLE FINISHED SRDB ID --> PALISADE ID')

        # compute the reverse map

        # loop on TM/TC
        for packet_type in types:

            # loop over each srdb_id
            for srdb_id, palisade_id in self.srdb_to_palisade_id[
                packet_type
            ].items():
                # check for duplicates palisade_id
                if palisade_id in self.palisade_to_srdb_id[packet_type]:
                    if isinstance(
                        self.palisade_to_srdb_id[packet_type][palisade_id],
                        list,
                    ):
                        self.palisade_to_srdb_id[packet_type][
                            palisade_id
                        ].append(srdb_id)
                    else:
                        self.palisade_to_srdb_id[packet_type][palisade_id] = [
                            self.palisade_to_srdb_id[packet_type][palisade_id],
                            srdb_id,
                        ]
                else:
                    self.palisade_to_srdb_id[packet_type][
                        palisade_id
                    ] = srdb_id

        # remove separation between TM and TC in the srdb_to_palisade_id dict
        # Note: this is not possible in the reverse dictionary as the palisade
        # ID are not really unique
        self.srdb_to_palisade_id = {
            **self.srdb_to_palisade_id['TM'],
            **self.srdb_to_palisade_id['TC'],
        }

        logger.debug('CREATE MAPPING TABLE FINISHED PALISADE ID --> SRDB ID')

    @property
    def mapping_namespace(self):
        return self._mapping_ns

    @staticmethod
    def compute_apid(process_id, packet_category):
        """
        Compute the APID using the process_id and the packet_category
        APID = |0000000|0000|
            process_id | packet_category
        """

        return (process_id << 4) + packet_category  # 4 bits shift

    @staticmethod
    def split_apid(apid):
        """
        Compute the APID using the process_id and the packet_category
        APID = |0000000|0000|
            process_id | packet_category
        """
        # force the type of the apid
        process_id = int(apid) >> 4  # 4 bits shift
        packet_category = int(apid) & 15  # keep only the last 4 bits
        return process_id, packet_category

    @staticmethod
    def split_parameter_SRDBID(srdbid):
        """
        Return the type, the kind and the short srdbid of the parameter using
        the SRDB rules.
        """
        parameter_type = {'NIW': 'TM', 'PIW': 'TC'}
        kind = {'G': 'global', 'D': 'detailed'}

        if srdbid[3] in ['D', 'G']:
            start_srdbid = 4
        else:
            start_srdbid = 3

        return (
            parameter_type[srdbid[:3]],  # type (TM/TC)
            kind.get(srdbid[3], 'normal'),  # kind
            int(srdbid[start_srdbid:]),
        )  # short srdbid

    @staticmethod
    def compute_packet_srdbid(packet_type, short_srdbid):
        """
        Return the srdb id according to the short srdb id and the type
        given in argument.
        """
        if packet_type == 'TM':
            prefix = 'YIW'
        elif packet_type == 'TC':
            prefix = 'ZIW'
        else:
            raise TypeError('Unknown packet type %s' % packet_type)
        return prefix + '{0}'.format(short_srdbid.zfill(5))

    @staticmethod
    def compute_parameter_srdbid(parameter_type, short_srdbid, kind):
        """
        Return the srdb id according to the short srdb id and the type
        given in argument.
        """
        if kind == 'normal':
            letter = ''
            size = 5
        elif kind == 'global':
            letter = 'G'
            size = 4
        elif kind == 'detailed':
            letter = 'D'
            size = 4

        if parameter_type == 'TM':
            prefix = 'NIW'
        elif parameter_type == 'TC':
            prefix = 'PIW'
        else:
            raise TypeError('Unknown parameter type %s' % parameter_type)
        return prefix + letter + '{0}'.format(short_srdbid.zfill(size))

    @staticmethod
    def compute_tf_srdbid(tf_type, short_srdbid):
        """
        Return the srdb id according to the short srdb id and the type
        given in argument.
        """
        if tf_type == 'TM':
            prefix = 'CIWP'
            suffix = 'TM'
            return prefix + '{0}'.format(short_srdbid.zfill(4)) + suffix
        elif tf_type == 'TC':
            prefix = 'CIWP'
            suffix = 'TC'
            return prefix + '{0}'.format(short_srdbid.zfill(4)) + suffix
        else:
            raise TypeError('Unknown TF type %s' % tf_type)

    @staticmethod
    def compute_enumeration_srdbid(enum_type, short_srdbid):
        """
        Return the srdb id according to the short srdb id and the type
        given in argument.
        """
        return 'CIWT' + short_srdbid.zfill(4) + enum_type

    @staticmethod
    def srdb_to_palisade_type(ptc, pfc):
        """
        Mapping between srdb and palisade type
        """

        def not_defined(ptc, pfc):
            raise TypeError(
                'Unsupported srdb type (ptc: %i, pfc: %i)' % (ptc, pfc)
            )

        def unsigned_integer_data_type(ptc, pfc):
            if ptc == 2:
                datatype = 'bU%i' % pfc
                if datatype == 'bU16':
                    datatype = 'UShort'
                return SimpleType(datatype)
            elif ptc == 3:
                if pfc < 12:
                    return SimpleType('bU%i' % (pfc + 4))
                elif pfc == 12:
                    return SimpleType('UShort')
                elif pfc == 14:
                    return SimpleType('UInt')
                elif pfc == 16:
                    return SimpleType('UInt64')

            return not_defined(ptc, pfc)

        def boolean_data_type(ptc, pfc):
            return SimpleType('b1Bool')

        def signed_integer_data_type(ptc, pfc):
            if pfc < 12:
                return SimpleType('b%i' % (pfc + 4))
            elif pfc == 12:
                return SimpleType('Short')
            elif pfc == 14:
                return SimpleType('Int')
            elif pfc == 16:
                return SimpleType('Int64')
            return not_defined(ptc, pfc)

        def float_data_type(ptc, pfc):
            if pfc == 1:
                return SimpleType('Float')
            elif pfc == 2:
                return SimpleType('Double')
            return not_defined(ptc, pfc)

        def bit_string_data_type(ptc, pfc):
            return not_defined(ptc, pfc)

        def octet_string_data_type(ptc, pfc):
            return not_defined(ptc, pfc)

        def ascii_string_data_type(ptc, pfc):
            return not_defined(ptc, pfc)

        def absolute_time_data_type(ptc, pfc):
            if pfc == 17:
                # 4 bytes coarse time
                # 2 bytes fine time
                return Time('CUC', 4, 2)

            return not_defined(ptc, pfc)

        def relative_time_data_type(ptc, pfc):
            return not_defined(ptc, pfc)

        ptc_mapping = {
            1: boolean_data_type,
            2: unsigned_integer_data_type,
            3: unsigned_integer_data_type,
            4: signed_integer_data_type,
            5: float_data_type,
            6: bit_string_data_type,
            7: octet_string_data_type,
            8: ascii_string_data_type,
            9: absolute_time_data_type,
            10: relative_time_data_type,
        }

        return ptc_mapping.get(ptc, not_defined)(ptc, pfc)

    @staticmethod
    def split_packet_SRDBID(srdbid):
        """
        Return the name of the parameter in the SRDB rules.
        """
        packet_type = {'YIW': 'TM', 'ZIW': 'TC'}

        return (
            packet_type[srdbid[:3]],  # type (TM/TC)
            'normal',  # kind
            srdbid[3:],
        )  # short srdbid
