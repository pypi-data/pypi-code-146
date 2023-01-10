#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

try:
    from poppy.core.db.connector import Connector
    from poppy.core.logger import logger
    from poppy.core.tools.exceptions import print_exception, MissingArgument
except:
    print('POPPy framework is not installed!')

try:
    from roc.idb.models.idb import PacketHeader, ItemInfo
    from roc.idb.models.idb import TransferFunction as idb_tf_model
    from roc.idb.exceptions import IdbQueryError
except:
    print('roc.idb plugin is not installed!')

from roc.rpl.packet_parser.packet_cache import PacketCache
from roc.rpl.exceptions import TransferFunctionError


__all__ = [ 'raw_to_eng']

class Enumeration:
    def __init__(self, srdb_id, idb_source, idb_version, model_instance=None):
        self.srdb_id = srdb_id
        self.idb_source = idb_source
        self.idb_version = idb_version
        if model_instance is None:
            self.model_instance = ItemInfo.objects.get(
                srdb_id=srdb_id,
                idb_source=idb_source,
                idb_version=idb_version
            )
        else:
            self.model_instance= model_instance
        transfer_function_values = idb_tf_model.objects.filter(item_info=self.model_instance)

        self.raw_to_eng = {}
        self.eng_to_raw = {}

        for values in transfer_function_values:
            self.raw_to_eng[values.raw] = values.eng
            self.eng_to_raw[values.eng] = values.raw

    @property
    def is_enumeration(self):
        return self.srdb_id.startswith('CIWT')

    def to_raw(self, value):
        return self.eng_to_raw[value]

    def to_eng(self, value):
        return self.raw_to_eng[value]

    @classmethod
    def from_model_instance(cls, model_instance):
        srdb_id = model_instance.srdb_id
        idb_source = model_instance.idb_source
        idb_version = model_instance.idb_version
        return cls(srdb_id, idb_source, idb_version, model_instance=model_instance)

class TransferFunction:

    def __init__(self, srdb_id, idb_source, idb_version, transfer_function=None):
        """
        Initialize instance of TransferFunction class

        :param srdb_id: SRDB ID of the transfer function
        :param idb_source: IDB source
        :param idb_version: IDB version
        :param transfer_function: transfer function data (if provided, skip the query of transfer function data in the database)
        """
        self.srdb_id = srdb_id
        self.idb_source = idb_source
        self.idb_version = idb_version
        try:
            if transfer_function is None:
                # get the IDB from IDBmanager
                self.idb_manager = Connector.manager['MAIN-DB'].idb_manager
                idb = self.idb_manager[(self.idb_source, self.idb_version)]
                # Get transfer function data for current IDB
                self.transfer_function = idb.transfer_function[srdb_id]
            else:
                self.transfer_function = transfer_function
        except:
            raise IdbQueryError(f'Retrieving TF {srdb_id} from IDB {self.idb_version} has failed!')

        self.raw_values, self.eng_values = self.transfer_function_values

        # compute monotonic chunks for reverse interpolation

        # compute the diff between eng values
        eng_values_diff = np.diff(self.eng_values)

        # split the raw and eng arrays to obtain monotonic chunks
        split_index = np.where(np.sign(eng_values_diff[:-1]) * np.sign(eng_values_diff[1:]) < 0 )[0] + 1

        raw_chunks = np.split(self.raw_values,  split_index)
        eng_chunks = np.split(self.eng_values,  split_index)

        # if there is more than one chunk
        chunk_num = len(eng_chunks)
        if chunk_num > 1:
            # ensure the continuity between chunks:
            for chunk_index in range(chunk_num-1):
                raw_chunks[chunk_index] = np.append(raw_chunks[chunk_index], raw_chunks[chunk_index+1][0])
                eng_chunks[chunk_index] = np.append(eng_chunks[chunk_index], eng_chunks[chunk_index+1][0])

        # convert chunk lists to numpy arrays
        eng_chunks = np.array(eng_chunks)
        raw_chunks = np.array(raw_chunks)

        # sort values for each chunk
        sorted_indices = np.argsort(eng_chunks, axis=1)

        self.eng_chunks = np.take_along_axis(eng_chunks, sorted_indices, axis=1)
        self.raw_chunks = np.take_along_axis(raw_chunks, sorted_indices, axis=1)

    @property
    def transfer_function_values(self):
        return zip(*[(float(values[0]), float(values[1])) for values in self.transfer_function])


    @property
    def is_enumeration(self):
        return False

    @staticmethod
    def find_nearest(array, value):
        value = float(value)
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def to_raw(self, value):

        result_list = []
        # check all monotonic chunks for the reverse interpolation

        for chunk_index, eng_values in enumerate(self.eng_chunks):
            raw_value = np.interp(value, eng_values, self.raw_chunks[chunk_index], left=np.NaN, right=np.NaN)
            if not np.isnan(raw_value):
                # the raw value shall be an integer
                result_list.append(int(raw_value))

        if not result_list:
            raise Exception(f"No raw value found for transfer function '{self.srdb_id}' and eng value '{value}'")
        elif len(result_list) == 1:
            result = result_list[0]
        else:
            # multiple result have been found
            # we need to determine the nearest result
            eng_list = [self.to_eng(raw_result) for raw_result in result_list]
            result = result_list[self.find_nearest(eng_list, value)]
        return result

    def to_eng(self, value):
        return np.interp(value, self.raw_values, self.eng_values, left=np.NaN, right=np.NaN)

class PalisadeTransferFunction(TransferFunction):
    """
    Class used to mitigate differences between MIB and PALISADE
    """

    transfer_function_exceptions = {
        # Discrepancies between TF_CP_BIA_P011 in MIB associated with CIWP0075TC and CIW00107TM
        # and TF_CP_BIA_0011 in PALISADE associated CIWP0040TC and CIW00104TM
        # IMPORTANT : TF_CP_BIA_0011 is obsolete and should not be used (use TF_CP_BIA_P011 instead)
        'CIWP0040TC': ([0, 32767, 32768, 65535], [0, 60, -60, -0.001831]),
        'CIW00104TM': ([0, 32767, 32768, 65535], [0, 60, -60, -0.001831])
    }

    @property
    def transfer_function_values(self):
        if self.srdb_id in self.transfer_function_exceptions:
            logger.warning(f'{self.srdb_id} is not defined in the MIB, use TF at your own risk!')
            return self.transfer_function_exceptions[self.srdb_id]
        else:
            return super().transfer_function_values

    @classmethod
    def from_idb(cls, tf_srdb_id,
                 idb_source='MIB',
                 idb_version=None):

        if not (idb_source and idb_version):
            raise MissingArgument('idb_source and idb_version arguments must be defined to run "raw_to_eng" function!')

        # Check if tf_instance already in the packetCache
        key = (tf_srdb_id, idb_source, idb_version)
        packet_cache = PacketCache()
        tf_instance = packet_cache.transfer_function.get(key, None)

        # If not, get it (and store it in the cache)
        if not tf_instance:
            tf_instance = cls(tf_srdb_id, idb_source, idb_version)
            packet_cache.transfer_function[key] = tf_instance

        return tf_instance


@Connector.if_connected('MAIN-DB')
def raw_to_eng(raw_values, tf_srdb_id,
               idb_source=None,
               idb_version=None):
    """
    Convert input raw values into engineering

    :param raw_values: numpy array containing raw values
    :param tf_srdb_id: string providing the SRDB_ID of the transfer function
    :param idb_source: string with the source of IDB
    :param idb_version: string with the version of IDB
    :return: engineering values
    """

    tf_instance = PalisadeTransferFunction.from_idb(tf_srdb_id,
                                                    idb_source=idb_source,
                                                    idb_version=idb_version)

    # Get instance of TransferFunction for the input transfer function srdb id
    try:
        eng_values = tf_instance.to_eng(raw_values)
    except:
        raise TransferFunctionError(f'Cannot convert "raw" to "eng" for transfer function {tf_srdb_id}!')

    # return engineering values
    return eng_values
