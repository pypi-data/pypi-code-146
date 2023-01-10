#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from sqlalchemy.orm.exc import NoResultFound

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.db.handlers import get_or_create
from poppy.core.logger import logger
from poppy.core.task import Task
from roc.idb.models.idb import IdbRelease
from roc.idb.models.idb import (
    ItemInfo,
    PacketHeader,
    PacketMapInfo,
    ParamInfo,
    TransferFunction,
)
from roc.idb.parsers import MIBParser
from roc.idb.parsers import PALISADEParser, SRDBParser
from roc.idb.parsers.idb_elements import Packet as IDBPacket
from roc.idb.parsers.idb_elements import ParameterDefinition, Enumeration
from roc.idb.tasks.load_palisade_metadata import put_palisade_metadata

__all__ = ['LoadTask']


class IdbLoadTaskError(Exception):
    pass


class LoadTask(Task):
    plugin_name = 'roc.idb'
    name = 'idb_load_idb'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        Use the appropriate parser to load the selected IDB into the ROC database.
        """
        # get the database session
        self.session = self.pipeline.db.session

        # create the parser of IDB
        self.source = self.pipeline.args.idb_source
        if self.source == 'SRDB':
            Parser = SRDBParser
        elif self.source == 'PALISADE':
            Parser = PALISADEParser
        elif self.source == 'MIB':
            Parser = MIBParser
        else:
            raise IdbLoadTaskError('Wrong parameter idb source')

        self.parser = Parser(
            self.pipeline.args.idb_path, self.pipeline.args.mapping
        )

        idb_version = self.parser.version()

        # check if the release already exists in the database
        try:
            existing_release = (
                self.session.query(IdbRelease)
                .filter_by(idb_version=idb_version, idb_source=self.source)
                .one()
            )

            logger.warning(
                f"IDB release ('{self.source}', '{idb_version}') already exists in the database"
            )
            return

        except NoResultFound:
            pass

        # parse the XML/dat files
        logger.debug(f'Start parsing using {self.source} parser')
        self.parser.parse()

        # put enum/tf into the database
        self._put_enumeration()
        self._put_tf()

        # put parameters into the database
        self._put_parameters()

        # put packets into the database
        self._put_packets()

        if self.source == 'PALISADE':
            # load the PALISADE metadata
            put_palisade_metadata(self.session, self.parser)

        # update the database
        self.pipeline.db.update_database()

    def _get_idb(self):
        """
        To get the database_descr of the IDB to use.
        """
        # create the version of the IDB or retrieve it
        idb = get_or_create(
            self.session,
            IdbRelease,
            idb_version=self.parser.version(),
            idb_source=self.parser.source(),
            mib_version=self.parser.mib_version,
            current=False,
        )
        return idb

    def _put_enumeration(self):
        """
        Put Enumerations information into roc dataase
        """

        # get the idb
        idb = self._get_idb()

        enumerations_count = len(Enumeration.manager.instances)

        for i, enumeration in enumerate(Enumeration):
            print(
                '\rLoading enumerations {}%'.format(
                    self._progress(i, enumerations_count)
                ),
                end='',
                flush=True,
            )

            srdb_id = enumeration.srdb_id
            palisade_id = enumeration.palisade_id

            # skip internal enumerations that uses PALISADE IDs instead of SRDB IDs
            if '_' in srdb_id:
                continue

            info = get_or_create(
                self.session,
                ItemInfo,
                srdb_id=srdb_id,
                palisade_id=palisade_id.strip()
                if isinstance(palisade_id, str)
                else palisade_id,
                idb=idb,
            )

            for eng, raw in enumeration.values.items():
                get_or_create(
                    self.session,
                    TransferFunction,
                    item_info_id=info.id_item_info,
                    raw=raw,
                    eng=eng,
                )
        logger.debug('END LOADING ENUMERATIONS IN DATABASE')

    def _put_tf(self):
        """
        Put transfer function information into roc database.
        """

        # get the idb
        idb = self._get_idb()

        tf_dict = self.parser.tf_dict

        tf_count = len(tf_dict)

        for i, srdb_id in enumerate(tf_dict):
            print(
                '\rLoading transfer functions {}%'.format(
                    self._progress(i, tf_count)
                ),
                end='',
                flush=True,
            )

            # create the info

            info = get_or_create(
                self.session, ItemInfo, srdb_id=srdb_id, idb=idb,
            )

            for raw_eng_values in tf_dict[srdb_id]:
                get_or_create(
                    self.session,
                    TransferFunction,
                    item_info_id=info.id_item_info,
                    raw=raw_eng_values['raw'],
                    eng=raw_eng_values['eng'],
                )
        logger.debug('END LOADING TF IN DATABASE')

    def _put_packets(self):
        """
        Put packets SRDB information into roc database.
        """
        # get the idb
        idb = self._get_idb()

        # loop over registered packets
        packets = IDBPacket.manager.instances

        packets_count = len(packets)

        for i, packet in enumerate(packets):

            print(
                '\rLoading packets {}%'.format(
                    self._progress(i, packets_count)
                ),
                end='',
                flush=True,
            )

            if packet.pid is None:
                print('\r', end='', flush=True)
                logger.warning(
                    'Packet {} does not have a PROCESS_ID'.format(palisade_id)
                )

            palisade_id = packet.name
            try:
                srdb_id = self.parser.palisade_to_srdb_id[packet.type][
                    palisade_id
                ]
            except KeyError:
                srdb_id = None
                print('\r', end='', flush=True)
                logger.warning(
                    'Could not find {} in srdb/palisade mapping file'.format(
                        palisade_id
                    )
                )

            # create the info
            info = get_or_create(
                self.session,
                ItemInfo,
                srdb_id=srdb_id,
                palisade_id=palisade_id.strip()
                if isinstance(palisade_id, str)
                else palisade_id,
                idb=idb,
            )

            # set the description of the packet
            info.item_descr = packet.description

            # if node is None, the packet is not defined in IDB
            if packet.node is None and self.parser is PALISADEParser:
                print('\r', end='', flush=True)
                logger.warning('{0} is not defined in IDB'.format(packet.name))
                continue

            # create a representation of the packet
            pkt = get_or_create(
                self.session,
                PacketHeader,
                item_info_id=info.id_item_info,
                cat_eng=str(packet.category),
                cat=packet.category,
                packet_type=packet.type,
                byte_size=packet.byte_size,
                pid=packet.pid,
                pid_eng=str(packet.pid),
                spid=packet.spid,
                sid=packet.sid,
                service_type=packet.service_type,
                service_subtype=packet.service_subtype,
            )

            # now link parameters
            parameters = self._link_parameters(packet.parameters)

            # for each parameter and packet, create the map between them
            maps = []
            for parameter, pkt_param in zip(parameters, packet.parameters):
                # get the info if already present or create a new one
                info = get_or_create(
                    self.session,
                    PacketMapInfo,
                    parameter=parameter,
                    packet=pkt,
                )

                # update the information with what is in the database
                info.byte_position = pkt_param.byte_position
                info.bit_position = pkt_param.bit_position
                info.group_size = pkt_param.group_size
                info.block_size = pkt_param.block_size
                info.loop_value = pkt_param.group_counter

                # add to the maps
                maps.append(info)

            # add maps to the session for update
            self.session.add_all(maps)

    def _link_parameters(self, parameters):
        """
        Returns database representation of parameters given in argument.
        """
        # get the idb
        idb = self._get_idb()

        params = []
        for parameter in parameters:
            # create the info
            info = (
                self.session.query(ItemInfo)
                .filter_by(srdb_id=parameter.srdb_id, idb=idb)
                .one()
            )

            # create a representation of the parameter
            param = self.session.query(ParamInfo).filter_by(info=info).one()

            # add to list
            params.append(param)

        return params

    def _progress(self, index, total):
        return int((index + 1) / total * 100)

    def _put_parameters(self):
        """
        Put parameters SRDB information into roc database.
        """
        # get the idb
        idb = self._get_idb()

        # list of parameter definitions
        parameters = ParameterDefinition.manager.instances

        parameters_count = len(parameters)
        # loop over registered parameters
        for i, parameter in enumerate(parameters):
            print(
                '\rLoading parameters {}%'.format(
                    self._progress(i, parameters_count)
                ),
                end='',
                flush=True,
            )

            palisade_id = parameter.palisade_id

            # create the info
            if parameter.srdb_id:

                packet_type, _, _ = self.parser.split_parameter_SRDBID(
                    parameter.srdb_id
                )

                assert packet_type in ['TM', 'TC']
                info = get_or_create(
                    self.session,
                    ItemInfo,
                    srdb_id=parameter.srdb_id,
                    palisade_id=palisade_id.strip()
                    if isinstance(palisade_id, str)
                    else palisade_id,
                    idb=idb,
                )

                # add the description of the parameter
                info.item_descr = parameter.description

                # get the associated transfer function if any
                if parameter.transfer_function:
                    # FIXME: handle multiple TF for one Palisade ID
                    if isinstance(parameter.transfer_function, list):
                        tf_srdb_id = parameter.transfer_function[0]
                    else:
                        tf_srdb_id = parameter.transfer_function
                    transfer_function = (
                        self.session.query(ItemInfo)
                        .filter_by(srdb_id=tf_srdb_id, idb=idb)
                        .filter(ItemInfo.srdb_id.like('%' + packet_type))
                        .first()
                    )
                    if transfer_function is None:
                        logger.warning(
                            f'No transfer function found for the {packet_type} {parameter.srdb_id} (Expected TF id: {parameter.transfer_function})'
                        )

                else:
                    transfer_function = None

                # create a representation of the parameter
                get_or_create(
                    self.session,
                    ParamInfo,
                    info=info,
                    par_bit_length=parameter.data_type.bit_length,
                    par_type=parameter.data_type.numpy_type,
                    par_max=numpy.float64(parameter.maximum),
                    par_min=numpy.float64(parameter.minimum),
                    par_unit=parameter.unit,
                    par_def=parameter.default,
                    par_is_editable=parameter.is_editable,
                    transfer_function=transfer_function,
                )
            else:
                logger.warning(
                    f'No SRDB ID found for the parameter {palisade_id}'
                )
