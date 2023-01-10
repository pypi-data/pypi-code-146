#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import re

import numpy

from poppy.core.logger import logger
from roc.idb.parsers.idb_elements import (Enumeration, Packet, Parameter,
                                          ParameterDefinition, drop_numpy_type)
from roc.idb.parsers.idb_parser import IDBParser

from . import dtypes

__all__ = ['SRDBParser']


def vectorial_match(data, regex=''):
    r = re.compile(regex)

    @numpy.vectorize
    def vmatch(data):
        return bool(r.match(str(data)))

    return vmatch(data)


class SRDBParser(IDBParser):
    """
    Class used for the parsing of the .dat files of the IDB to get information on the
    IDB and SRDB.
    """

    @staticmethod
    def filter_table(table, regex_dict={'SQNAME': 'AIWF\d{3}[A-Z]'}):
        """
        Filter tables to keep only specified values
        """
        match = numpy.logical_and.reduce(
            [
                vectorial_match(table[key], regex=value)
                for key, value in regex_dict.items()
            ]
        )

        return table[match]

    @classmethod
    def from_table(cls, filepath, dtype, regex_dict={}):
        """
        Load IDB info from the given csv file.

        :param filepath: Path to the csv file
        :param dtype: Numpy dtype of the table
        :param regex_dict: Dictionary use to filter the table, example: regex_dict={"SQNAME": "AIWF\d{3}[A-Z]"}
        :return:
        """

        # create a generic dtype to avoid parsing errors with empty values
        obj_dtype = numpy.dtype(
            [(key, object) for key, _ in dtype.fields.items()]
        )

        with open(filepath, newline='') as csv_file:
            csv_table_reader = csv.reader(csv_file, delimiter='\t')
            table = numpy.array(
                [tuple(row)[: len(dtype)] for row in csv_table_reader],
                dtype=obj_dtype,
            )
            if regex_dict:
                table = cls.filter_table(table, regex_dict=regex_dict)

            # force the dtype of the returned table
            return table.astype(dtype)

    def setup_source_dir(self, dir_path):
        self._source = 'SRDB'

        # IDB files path
        self.dir_path = os.path.join(dir_path, self._source, 'Dat')

    def __init__(self, dir_path, mapping_file_path):
        """
        Store the dir path of the .dat files containing the IDB.
        """

        self.setup_source_dir(dir_path)

        super().__init__(mapping_file_path)

        # Packet indexing using TPSD id (variable one)
        self.tpsd_mapping = dict()
        # packet indexing using spid (static one)
        self.spid_mapping = dict()

        # list of detailed parameter for each global one
        self.global_parameters = dict()

        # min and max value indexed by srdbid
        self.min_max_dict = dict()

    def version(self):
        """
        Return the version of the IDB defined in the dat file.
        """

        vdf_table = self.from_table(
            os.path.join(self.dir_path, 'vdf.dat'), dtype=dtypes.vdf_dtype
        )
        # read the version information from the srdb (the version is included
        # in a long comment)
        vdf_version = vdf_table['COMMENT'].item().split(' ')
        # use the word "Version" as a tag to find the usefull information
        version_index = vdf_version.index('Version') + 1
        # store the version and remove the trailing quote
        srdb_version = vdf_version[version_index].strip("'")
        return srdb_version

    def enumeration_srdb(self, enumeration, kind):
        """
        Return the name of the enumeration in the SRDB according to the type
        given in argument.

        For the moment, for the SRDB parser, the enumeration name is the
        SRDBID whereas for PALISADE parser, it's the PALISADE ID
        """
        return enumeration.name

    def get_palisade_id(self, srdb_id):
        """
        Return the corresponding palisade ID.
        """
        return self.srdb_to_palisade_id[srdb_id]

    def add_packet(
        self,
        name,
        srdbid,
        kind=None,
        packet_type=None,
        pid=None,
        spid=None,  # SCOS Packet ID
        sid=None,
        packet_category=None,
        description=None,
        bit_size=0,
        service_type=None,
        service_subtype=None,
    ):

        packet = Packet(
            name, srdbid, kind=kind, type=packet_type, bit_size=bit_size
        )

        packet.pid = pid
        packet.pid_eng = str(pid)
        packet.spid = spid
        packet.sid = sid
        packet.sid_eng = str(sid)
        packet.service_type = service_type
        packet.service_type_eng = str(service_type)
        packet.service_subtype = service_subtype
        packet.service_subtype_eng = str(service_subtype)

        # get the packet category
        packet.category = packet_category
        packet.category_eng = str(packet_category)

        # get the description of the packet
        packet.description = description

        # create empty list of parameters
        packet.parameters = []

        return packet

    def create_mapping(self):
        # xml mapping
        super().create_mapping()

        # mapping between srdbid, short palisade ID and param/packet description

        sw_para_file_path = os.path.join(self.dir_path, 'sw_para.dat')

        if not os.path.isfile(sw_para_file_path):
            sw_para_file_path = os.path.join(self.dir_path, 'ASW_sw_para.dat')

        sw_para = self.from_table(
            sw_para_file_path, dtype=dtypes.sw_para_dtype
        )

        self.sw_para_mapping = {
            row['SCOS_NAME']: (row['SW_NAME'], row['SW_DESCR'])
            for row in sw_para
        }

    def add_palisade_prefix(self, short_palisade_id, srdb_id):
        """
        Save the correspondence between the palisade and the (long) srdb ID
        """
        if srdb_id in self.srdb_to_palisade_id:
            logger.debug(
                f'Comparing reconstructed palisade IDs ({self.srdb_to_palisade_id[srdb_id]}, '
                f'{short_palisade_id}) associated with this srdb ID ({srdb_id})'
            )
            if (
                self.srdb_to_palisade_id[srdb_id][3:].strip()
                != short_palisade_id.strip()
            ):
                logger.error(
                    f'The short palisade ID is not compatible with the long one '
                    f'({self.srdb_to_palisade_id[srdb_id]} != {short_palisade_id}) associated with '
                    f'this srdb ID ({srdb_id})'
                )

            return self.srdb_to_palisade_id[srdb_id]

    def create_parameter(
        self,
        palisade_id,
        srdb_id,
        ptc,
        pfc,
        parameter_type,
        kind,
        unit=None,
        enumeration=None,
        min_max_values=(None, None),
        transfer_function=None,
    ):

        _, description = self.sw_para_mapping[srdb_id]

        definition_dict = {
            'description': description,
            'palisade_id': palisade_id,
            'default': None,
            'is_editable': None,
            'transfer_function': transfer_function,
            'minimum': None,
            'maximum': None,
            'unit': unit,
        }

        if enumeration is not None:
            enumeration.data_type = repr(self.srdb_to_palisade_type(ptc, pfc))
            definition_dict['data_type'] = enumeration
        else:
            definition_dict['data_type'] = self.srdb_to_palisade_type(ptc, pfc)
            (
                definition_dict['minimum'],
                definition_dict['maximum'],
            ) = min_max_values

        definition = ParameterDefinition(srdb_id, **definition_dict)

        parameter = Parameter(definition, parameter_type)

        return parameter

    def convert_to_palisade(self, srdb_id):
        """ Convert SRDB ID into PALISADE ID using mapping table"""
        if srdb_id in self.srdb_to_palisade_id:
            return self.srdb_to_palisade_id[srdb_id]
        else:
            logger.error('No PALISADE ID associated to SRDB ID : %s', srdb_id)

    def load_min_max_values(self):
        """
        Load min and max parameters value from ccs SRDB data
        """

        ccs_cap_dtype = numpy.dtype(
            [('NUMBR', 'U10'), ('XVALS', 'U17'), ('YVALS', 'U17')]  # srdbid
        )

        prv_dtype = numpy.dtype(
            [('NUMBR', 'U10'), ('MINVAL', 'U64'), ('MAXVAL', 'U64')]
        )

        prf_dtype = numpy.dtype(
            [
                ('NUMBR', 'U10'),
                ('DESCR', 'U24'),
                ('INTER', 'U1'),
                ('DSPFMT', 'U1'),
                ('RADIX', 'U1'),
            ]
        )

        ccs_table = self.from_table(
            os.path.join(self.dir_path, 'ccs.dat'),
            dtype=ccs_cap_dtype,
            regex_dict={'NUMBR': '^CIW.*'},
        )

        cap_table = self.from_table(
            os.path.join(self.dir_path, 'cap.dat'),
            dtype=ccs_cap_dtype,
            regex_dict={'NUMBR': '^CIW.*'},
        )

        prv_table = self.from_table(
            os.path.join(self.dir_path, 'prv.dat'),
            dtype=prv_dtype,
            regex_dict={'NUMBR': '^VIW.*'},
        )

        prf_table = self.from_table(
            os.path.join(self.dir_path, 'prf.dat'),
            dtype=prf_dtype,
            regex_dict={'NUMBR': '^VIW.*'},
        )

        for row in ccs_table:
            if self.min_max_dict.get(row['NUMBR']) is None:
                self.min_max_dict[row['NUMBR']] = (row['XVALS'], row['XVALS'])
            else:
                min_value, max_value = self.min_max_dict[row['NUMBR']]
                self.min_max_dict[row['NUMBR']] = (
                    min(min_value, row['XVALS'], key=float),
                    max(max_value, row['XVALS'], key=float),
                )

        for row in cap_table:
            if self.min_max_dict.get(row['NUMBR']) is None:
                self.min_max_dict[row['NUMBR']] = (row['XVALS'], row['XVALS'])
            else:
                min_value, max_value = self.min_max_dict[row['NUMBR']]
                self.min_max_dict[row['NUMBR']] = (
                    min(min_value, row['XVALS'], key=float),
                    max(max_value, row['XVALS'], key=float),
                )


        # get the default min/max representation from the prf table
        #
        # 'D' – Decimal
        # 'H' – Hexadecimal
        # 'O' – Octal

        min_max_repr = {}

        for row in prf_table:
            min_max_repr[row['NUMBR']] = row['RADIX']


        for row in prv_table:
            # convert each min/max value into Dec
            if min_max_repr[row['NUMBR']] == 'H':
                min_value = str(int(row['MINVAL'], 16))
                max_value = str(int(row['MAXVAL'], 16))
            elif min_max_repr[row['NUMBR']] == 'O':
                min_value = str(int(row['MINVAL'], 8))
                max_value = str(int(row['MAXVAL'], 8))
            else:
                min_value = row['MINVAL']
                max_value = row['MAXVAL']

            self.min_max_dict[row['NUMBR']] = (min_value, max_value)


    def add_tc_packet(self):
        """
        TC packet loading from ccf SRDB data
        """

        ccf_table = self.from_table(
            os.path.join(self.dir_path, 'ccf.dat'),
            dtype=dtypes.ccf_dtype,
            regex_dict={'CNAME': '^ZIW.*'},
        )

        for row in ccf_table:
            # create the object of the packet
            short_name = row['DESCR']
            logger.debug('Reading TC packet: %s' % short_name)

            packet_type, kind, srdbid = self.split_packet_SRDBID(row['CNAME'])
            process_id, packet_category = self.split_apid(row['APID'])

            name = self.add_palisade_prefix(short_name, row['CNAME'])
            service_type = row['TYPE']
            service_subtype = row['STYPE']

            self.add_packet(
                name,
                srdbid,
                kind=kind,
                packet_type=packet_type,
                pid=process_id,
                spid=None,
                sid=None,
                packet_category=packet_category,
                description=row['DESCR2'],
                service_type=service_type,
                service_subtype=service_subtype,
            )

    def add_tm_packet(self):
        """
        TM packet loading from pid SRDB data
        """

        pid_table = self.from_table(
            os.path.join(self.dir_path, 'pid.dat'), dtype=dtypes.pid_dtype
        )

        tpcf_table = self.from_table(
            os.path.join(self.dir_path, 'tpcf.dat'),
            dtype=numpy.dtype(
                [('SPID', object), ('NAME', 'U12'), ('SIZE', object)]
            ),
            regex_dict={'NAME': '^YIW.*'},
        )

        spid_srdb_id_mapping = {}

        for tpcf_row in tpcf_table:
            spid_srdb_id_mapping[tpcf_row['SPID']] = (
                tpcf_row['NAME'],
                tpcf_row['SIZE'],
            )

        for pid_row in pid_table:
            if pid_row['SPID'] not in spid_srdb_id_mapping:
                # skip non RPW packets
                continue

            srdb_id, size = spid_srdb_id_mapping[pid_row['SPID']]

            # create the object of the packet
            short_name, description = self.sw_para_mapping[srdb_id]
            logger.debug('Reading TM packet: %s' % short_name)
            packet_type, kind, srdbid = self.split_packet_SRDBID(srdb_id)
            process_id, packet_category = self.split_apid(pid_row['APID'])

            name = self.add_palisade_prefix(short_name, srdb_id)
            service_type = pid_row['TYPE']
            service_subtype = pid_row['STYPE']

            # save packet size if it's not a variable structure (else set to 0
            # and fill it later)
            header_byte_size = 16
            byte_size = int(size) - header_byte_size if size != '' else 0
            packet = self.add_packet(
                name,
                srdbid,
                kind=kind,
                packet_type=packet_type,
                pid=process_id,
                spid=pid_row['SPID'],
                sid=pid_row['PI1_VAL'],
                packet_category=packet_category,
                description=description,
                bit_size=byte_size * 8,
                service_type=service_type,
                service_subtype=service_subtype,
            )
            # if Telemetry Packet Structure Definition (TPSD) exist, use it to
            # index packets
            if pid_row['TPSD'] > -1:
                self.tpsd_mapping[pid_row['TPSD']] = packet
            # else it's a static and use spid to index the packet
            else:
                self.spid_mapping[pid_row['SPID']] = packet

    def add_tc_parameter(self):
        """
        TC parameter loading from cpc SRDB data
        """

        cpc_table = self.from_table(
            os.path.join(self.dir_path, 'cpc.dat'),
            dtype=dtypes.cpc_dtype,
            regex_dict={'PNAME': '^PIW.*'},
        )
        for row in cpc_table:
            srdb_id = row['PNAME']
            parameter_type, kind, short_srdb_id = self.split_parameter_SRDBID(
                srdb_id
            )
            short_name = row['DESCR']
            logger.debug('Reading TC parameter: %s' % short_name)

            palisade_id = self.add_palisade_prefix(short_name, row['PNAME'])
            enumeration = None
            min_max_values = (None, None)
            tf_srdb_id = None

            if row['PRFREF'] != '':
                min_max_values = self.min_max_dict[row['PRFREF']]
            elif row['PAFREF'] != '':
                # if not a transfer function
                if row['PAFREF'][3] == 'T':
                    enumeration = Enumeration.manager[row['PAFREF']]
                else:
                    min_max_values = self.min_max_dict[row['PAFREF']]
                tf_srdb_id = row['PAFREF']
            elif row['CCAREF'] != '':
                # if not a transfer function
                if row['CCAREF'][3] == 'T':
                    enumeration = Enumeration.manager[row['CCAREF']]
                else:
                    min_max_values = self.min_max_dict[row['CCAREF']]
                tf_srdb_id = row['CCAREF']

            self.create_parameter(
                palisade_id,
                srdb_id,
                row['PTC'],
                row['PFC'],
                parameter_type,
                kind,
                unit=row['UNIT'],
                enumeration=enumeration,
                min_max_values=min_max_values,
                transfer_function=tf_srdb_id,
            )

    def add_tm_parameter(self):
        """
        TM parameter loading from pcf SRDB data
        """

        pcf_table = self.from_table(
            os.path.join(self.dir_path, 'pcf.dat'),
            dtype=dtypes.pcf_dtype,
            regex_dict={'NAME': '^NIW.*'},
        )

        for row in pcf_table:
            srdb_id = row['NAME']
            parameter_type, kind, short_srdb_id = self.split_parameter_SRDBID(
                srdb_id
            )
            short_name = row['DESCR']
            logger.debug('Reading TM paramater: %s' % short_name)

            palisade_id = self.add_palisade_prefix(short_name, srdb_id)
            enumeration = None
            tf_srdb_id = None
            min_max_values = (None, None)
            if row['CURTX'] != '':
                # if not a transfer function
                if row['CURTX'][3] == 'T':
                    enumeration = Enumeration.manager[row['CURTX']]
                else:
                    min_max_values = self.min_max_dict[row['CURTX']]
                tf_srdb_id = row['CURTX']

            self.create_parameter(
                palisade_id,
                srdb_id,
                row['PTC'],
                row['PFC'],
                parameter_type,
                kind,
                unit=row['UNIT'],
                enumeration=enumeration,
                min_max_values=min_max_values,
                transfer_function=tf_srdb_id,
            )

    def add_tc_packetsubelement(self):
        """
        TC packet structure loading from cdf SRDB data
        """

        cdf_table = self.from_table(
            os.path.join(self.dir_path, 'cdf.dat'),
            dtype=dtypes.cdf_dtype,
            regex_dict={'CNAME': '^ZIW.*'},
        )

        # size of and position in the group of parameters
        group_size = 0
        group_position = 0
        spare_size = 0

        for row in cdf_table:
            srdb_long_id = row['CNAME']
            packet_type, kind, srdbid = self.split_packet_SRDBID(srdb_long_id)
            name = self.get_palisade_id(srdb_long_id)
            packet = Packet.manager[name]

            # if no parameter name check if it's a spare
            if row['PNAME'] == '':
                if row['DESCR'] == 'SPARE':
                    packet.add_to_size(row['ELLEN'])
                    if group_size != 0:
                        # add the bit size of the spare to the total
                        spare_size += row['ELLEN']
                        # decrement the group size counter since spares 0x0 do
                        # not count in palisade
                        group_size -= 1
                    continue

                else:
                    logger.error(
                        'Unknown object uncounter during SRDB parsing'
                    )
                    raise TypeError(
                        'palisade_id: %s, srdb_id: %s' % (name, srdb_long_id)
                    )
            else:
                parameter_srdb_id = row['PNAME']
                parameter_palisade_id = self.get_palisade_id(parameter_srdb_id)
                definition = ParameterDefinition.manager[parameter_srdb_id]
                (
                    parameter_type,
                    parameter_kind,
                    _,
                ) = self.split_parameter_SRDBID(parameter_srdb_id)

                # update the default value of the parameter
                definition.default = (
                    row['VALUE'] if row['VALUE'] != '' else None
                )

                # update the editable status and the max/min values

                if row['ELTYPE'] == 'F':
                    # if the parameter is fixed, max = min = default
                    definition.maximum = definition.default
                    definition.minimum = definition.default

                definition.is_editable = row['ELTYPE'] == 'E'

                parameter = Parameter(definition, parameter_type)
                # store the byte position and bit position inside the byte
                parameter.byte_position = row['BIT'] // 8
                parameter.bit_position = row['BIT'] % 8
                if parameter_kind != 'global':
                    packet.add_to_size(
                        parameter.definition.data_type.bit_length
                    )
                    packet.parameters.append(parameter)

            if group_size != 0:
                if parameter_kind != 'global':
                    if (group_size - 1) != group_position:
                        group_position += 1
                    else:
                        packet.set_group_properties(
                            group_size, spare_size=spare_size
                        )
                        # reset size and position
                        group_position = 0
                        group_size = row['GRPSIZE']
                        spare_size = 0
                else:
                    # update the group size to take into account subparams
                    # and remove global parameter
                    len_detailed = len(
                        self.global_parameters[parameter_srdb_id]
                    )
                    group_size += len_detailed - 1
            else:
                group_size = row['GRPSIZE']
                spare_size = 0

            logger.debug(
                'Update TC packet structure %s with %s parameter'
                % (name, parameter_palisade_id)
            )

    def add_tm_packetsubelement(self):
        """
        TM packet structure loading from vpd SRDB data
        """

        vpd_table = self.from_table(
            os.path.join(self.dir_path, 'vpd.dat'),
            dtype=dtypes.vpd_dtype,
            regex_dict={'NAME': '^NIW.*'},
        )

        # bit position of the parameter
        bit_cursor = 0

        # size of and position in the group of parameters
        group_size = 0
        group_position = 0

        # reorder the table by TPSD and POS
        for row in numpy.sort(vpd_table, order=['TPSD', 'POS']):
            # retrieve the variable packet using the tpsd_mapping
            packet = self.tpsd_mapping[row['TPSD']]

            # For the first parameter, reset the bit cursor
            if row['POS'] == 1:
                bit_cursor = 0
            bit_cursor += row['OFFSET']
            long_srdb_id = repr(packet)

            name = self.get_palisade_id(long_srdb_id)
            # verify that the packet is already defined in the packet manager
            assert packet == Packet.manager[name]

            parameter_srdb_id = row['NAME']

            definition = ParameterDefinition.manager[parameter_srdb_id]
            (parameter_type, parameter_kind, _) = self.split_parameter_SRDBID(
                parameter_srdb_id
            )

            parameter = Parameter(definition, parameter_type)

            # parameter.block_size =  bsize // 8  # in bytes

            # store the byte position and bit position inside the byte
            parameter.byte_position = bit_cursor // 8
            parameter.bit_position = bit_cursor % 8

            # increment the byte position with the size of the parameter
            # and store it
            bit_cursor += definition.data_type.bit_length

            if parameter_kind != 'global':
                # global parameters are not stored in the packet
                packet.update_size(bit_cursor)
                packet.parameters.append(parameter)
            # the group size (number of params in a group) is specified in the
            # parameter just before the beginning of the group
            if group_size != 0:
                if parameter_kind != 'global':
                    if (group_size - 1) != group_position:
                        # move ahead in the group
                        group_position += 1
                    else:
                        packet.set_group_properties(
                            group_size, bit_cursor - start_cursor
                        )
                        # reset size and position
                        group_position = 0
                        group_size = row['GRPSIZE']
                        start_cursor = bit_cursor
                else:
                    # update the group size to take into account the global parameter and the sub-params block
                    group_size += self.compute_global_param_group_size(
                        parameter_srdb_id
                    )

            else:
                group_size = row['GRPSIZE']
                start_cursor = bit_cursor

            logger.debug(
                'Update TM packet structure %s with %s parameter'
                % (name, parameter_srdb_id)
            )

    def compute_global_param_group_size(self, global_parameter_srdb_id):
        """
        Compute the global and sub-parameters block contribution to the group size.

        # packet structure:
        # =======================
        # param 1
        # param 2
        # ------ global param 3 -
        # > sub-parm 3.1           |
        # > sub-pram 3.2           | sub_param_list_len
        # > sub-pram 3.3           |
        # -----------------------
        # param 4
        # param 5
        # =======================

        :param global_parameter_srdb_id:
        :return:
        """
        sub_param_list_len = len(
            self.global_parameters[global_parameter_srdb_id]
        )
        return sub_param_list_len - 1

    def add_static_packetsubelement(self):
        """
        TM/TC static structure loading from plf SRDB data
        """

        plf_table = self.from_table(
            os.path.join(self.dir_path, 'plf.dat'),
            dtype=dtypes.plf_dtype,
            regex_dict={'NAME': '^NIW.*'},
        )

        # reorder the table and loop over rows
        for row in numpy.sort(plf_table, order=['SPID', 'OFFBY', 'OFFBI']):
            # since it's a static, use spid to retrieve the packets
            packet = self.spid_mapping[row['SPID']]
            srdb_long_id = repr(packet)
            packet_type, kind, srdbid = self.split_packet_SRDBID(srdb_long_id)
            name = self.get_palisade_id(srdb_long_id)
            # verify that the packet is already defined in the packet manager
            assert packet == Packet.manager[name]

            parameter_srdb_id = row['NAME']
            definition = ParameterDefinition.manager[parameter_srdb_id]
            (parameter_type, parameter_kind, _) = self.split_parameter_SRDBID(
                parameter_srdb_id
            )
            parameter = Parameter(definition, parameter_type)

            # store the byte position and bit position inside the byte
            header_byte_size = 16
            parameter.byte_position = row['OFFBY'] - header_byte_size
            parameter.bit_position = row['OFFBI']

            if parameter_kind != 'global':
                packet.parameters.append(parameter)
            logger.debug(
                'Update TM/TC static structure %s with %s parameter'
                % (name, parameter_srdb_id)
            )

    def create_parameters(self):
        # TC parameter in cpc SRDB data
        self.add_tc_parameter()
        logger.debug('TC parameter entries loaded.')

        # TM parameter in pcf SRDB data
        self.add_tm_parameter()
        logger.debug('TM parameter entries loaded.')

    def create_packets(self):
        # TC packet in ccf SRDB data
        self.add_tc_packet()
        logger.debug('TC packet entries loaded.')

        # TM packet in pid SRDB data
        self.add_tm_packet()
        logger.debug('TM packet entries loaded.')

    def populate_packets_with_parameters(self):
        # TC packet structure in cdf SRDB data
        self.add_tc_packetsubelement()
        logger.debug('TC packet subelement entries loaded.')

        # TM packet structure in vpd SRDB data (Variable packet definition)
        self.add_tm_packetsubelement()
        logger.debug('TM packet subelement entries loaded.')

        # TM/TC static structure in plf SRDB data
        self.add_static_packetsubelement()
        logger.debug('Static packet subelement entries loaded.')

    def add_enum_palisade_ids(self):
        """
        Enumeration palisade id loading from txf, paf SRDB data (WIP)

        FIXME: load the palisade ids
        """

        # textual calibrations
        txf_table = self.from_table(
            os.path.join(self.dir_path, 'txf.dat'), dtype=dtypes.txf_dtype
        )

        paf_table = self.from_table(
            os.path.join(self.dir_path, 'paf.dat'), dtype=dtypes.paf_dtype
        )

    def add_tf_palisade_ids(self):
        """
        TF palisade id loading from caf, cca SRDB data

        FIXME: load the palisade ids
        """

        # numerical calibrations
        caf_table = self.from_table(
            os.path.join(self.dir_path, 'caf.dat'), dtype=dtypes.caf_dtype
        )

        cca_table = self.from_table(
            os.path.join(self.dir_path, 'cca.dat'), dtype=dtypes.cca_dtype
        )

    def create_transfer_functions(self):
        """
        TF points loading from cap, ccs SRDB data (tabulated transfer functions)
        """

        cap_table = self.from_table(
            os.path.join(self.dir_path, 'cap.dat'),
            dtype=dtypes.cap_dtype,
            regex_dict={'NAME': '^CIW.*'},
        )

        ccs_table = self.from_table(
            os.path.join(self.dir_path, 'ccs.dat'),
            dtype=dtypes.ccs_dtype,
            regex_dict={'NAME': '^CIW.*'},
        )

        self.tf_dict = {}

        for row in ccs_table:
            # parse the TC transfer functions
            srdbid = row['NAME']
            self.tf_dict.setdefault(srdbid, []).append(
                {'raw': int(row['RAW']), 'eng': row['ENG']}
            )
            logger.debug('Reading TF parameter value: %s' % row['NAME'])

        for row in cap_table:
            # parse the TM transfer functions
            srdbid = row['NAME']
            self.tf_dict.setdefault(srdbid, []).append(
                {'raw': int(row['RAW']), 'eng': row['ENG']}
            )
            logger.debug('Reading TF parameter value: %s' % row['NAME'])

        logger.debug('End of parsing TF')

    def create_enumerations(self):
        """
        Search in the txp and pas for enumeration definition.
        """

        txp_table = self.from_table(
            os.path.join(self.dir_path, 'txp.dat'),
            dtype=dtypes.txp_dtype,
            regex_dict={'NAME': '^CIW.*'},
        )

        pas_table = self.from_table(
            os.path.join(self.dir_path, 'pas.dat'),
            dtype=dtypes.pas_dtype,
            regex_dict={'NAME': '^CIW.*'},
        )

        enumerations = {}

        for row in txp_table:
            # get the TM info
            srdb_id = row['NAME']
            enumerations.setdefault(srdb_id, {})[row['ENG']] = int(row['RAW'])
            logger.debug('Reading TF parameter value: %s' % row['NAME'])

        for row in pas_table:
            # get the TM info
            srdb_id = row['NAME']
            enumerations.setdefault(srdb_id, {})[row['ENG']] = int(row['RAW'])
            logger.debug('Reading TF parameter value: %s' % row['NAME'])

        for srdb_id in enumerations:
            enumeration = Enumeration(srdb_id)
            enumeration.values = enumerations[srdb_id]

        logger.debug('End of parsing Enumerations')

    def create_global_parameters_mapping(self):

        pcf_glob_det_table = self.from_table(
            os.path.join(self.dir_path, 'pcf_glob_det.dat'),
            dtype=dtypes.pcf_glob_det_dtype,
        )

        for row in pcf_glob_det_table:
            global_param_list = self.global_parameters.get(row['GLOBALID'])
            if global_param_list is None:
                global_param_list = []
            global_param_list.append(row['DETAILEDID'])
            self.global_parameters[row['GLOBALID']] = global_param_list

    def parse(self):
        """
        Call all methods to get the necessary information from the SRDB .dat
        files.
        """
        logger.debug('Loading and parsing %s files ...' % self._source)

        # create mapping between detailed and global parameters
        self.create_global_parameters_mapping()

        # load min and max values of parameters
        self.load_min_max_values()

        # create enumerations
        self.create_enumerations()

        # create transfer functions
        self.create_transfer_functions()

        # create TM and TC parameters
        self.create_parameters()

        # create TM and TC packets
        self.create_packets()

        # populate TM and TC packets with parameters
        self.populate_packets_with_parameters()

        # remove numpy dtype for parameters and packets attributes
        for packet in Packet:
            drop_numpy_type(packet)
            for parameter in packet.parameters:
                drop_numpy_type(parameter)

        for definition in ParameterDefinition:
            drop_numpy_type(definition)
        logger.debug('Loading and parsing %s files ... Done' % self._source)
