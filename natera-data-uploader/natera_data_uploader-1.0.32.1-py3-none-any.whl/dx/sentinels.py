#!/usr/bin/env python
import logging
import os
from abc import ABCMeta, abstractmethod

import xml.etree.ElementTree as ET

from dxpy import DXRecord

from soyuz.data.records import RecordFactory, DNAnexusRecord, ExodusRecord
from soyuz.dx.variables import Type, Property
from soyuz.utils import get_instrument_type_from_name


class SentinelBase(object):
    __metaclass__ = ABCMeta

    DATA_KEY = "data"
    FASTQ_KEY = "fastq"
    METRICS_KEY = "run_metrics"
    DX_LINK_KEY = "$dnanexus_link"

    def __init__(self, storage, basedir, name):
        self.record = RecordFactory.create(storage, basedir, name)

    @abstractmethod
    def add_file(self, data_file, file_id):
        raise NotImplementedError()

    def add_link(self, file_id):
        if isinstance(self.record, DNAnexusRecord):
            return {SentinelBase.DX_LINK_KEY: file_id}
        elif isinstance(self.record, ExodusRecord):
            return file_id

    def get_id(self):
        return self.record.get_id()

    def close(self):
        self.record.close()

    def get_properties(self):
        return self.record.get_properties()

    def add_property(self, key, value):
        self.record.add_property(key, value)


class WesSignateraSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        details = self.record.get_details()
        sample_id = data_file.get_sample_id()
        if sample_id:
            self.record.add_tags([sample_id])
            self.__add_data_file_details(details, sample_id, self.add_link(file_id))
        else:
            self.__add_metrics_details(details, self.add_link(file_id))
        self.record.set_details(details)

    @staticmethod
    def __add_data_file_details(details, sample_id, file_link):
        if SentinelBase.DATA_KEY not in details:
            details[SentinelBase.DATA_KEY] = {}
        data_details = details[SentinelBase.DATA_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append(file_link)

    @staticmethod
    def __add_metrics_details(details, file_link):
        if SentinelBase.METRICS_KEY not in details:
            details[SentinelBase.METRICS_KEY] = []
        details[SentinelBase.METRICS_KEY].append(file_link)


class PersonalisSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        details = self.record.get_details()
        sample_id = data_file.get_sample_id()
        if sample_id:
            self.record.add_tags([sample_id])
            if data_file.get_type() == Type.BAM:
                self.__add_data_file_details(details, sample_id, self.add_link(file_id))
            elif data_file.get_type() == Type.FASTQ:
                self.__add_fastq_file_details(details, sample_id, self.add_link(file_id))
        else:
            self.__add_metrics_details(details, self.add_link(file_id))
        self.record.set_details(details)

    @staticmethod
    def __add_data_file_details(details, sample_id, file_link):
        if SentinelBase.DATA_KEY not in details:
            details[SentinelBase.DATA_KEY] = {}
        data_details = details[SentinelBase.DATA_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append(file_link)

    @staticmethod
    def __add_fastq_file_details(details, sample_id, file_link):
        if SentinelBase.FASTQ_KEY not in details:
            details[SentinelBase.FASTQ_KEY] = {}
        data_details = details[SentinelBase.FASTQ_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append(file_link)

    @staticmethod
    def __add_metrics_details(details, file_link):
        if SentinelBase.METRICS_KEY not in details:
            details[SentinelBase.METRICS_KEY] = []
        details[SentinelBase.METRICS_KEY].append(file_link)


class SangerSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        details = self.record.get_details()
        file_type = data_file.get_type()

        if file_type:
            if file_type not in details:
                details[file_type] = []
            details[file_type].append(self.add_link(file_id))

        self.record.set_details(details)


class NgsSentinel(SentinelBase):

    def __init__(self, storage, basedir, name, site_id, expected_upload_time):
        super(NgsSentinel, self).__init__(storage, basedir, name)

        if site_id:
            self.record.add_property(Property.SITE_ID, site_id)

            describe = DXRecord(self.record.get_id()).describe(incl_properties=True)

            # Double check siteId property if it exists, to be sure that we will not have any problems with it later
            # in other system parts
            if describe['properties'][Property.SITE_ID] != site_id:
                raise Exception("Sentinel record has incorrect siteId property: {}, but should be: {}".format(
                    describe['properties'][Property.SITE_ID], site_id))

        if expected_upload_time:
            self.record.add_property(Property.EXPECTED_UPLOAD_TIME, str(expected_upload_time))

    def add_file(self, data_file, file_id):
        details = self.record.get_details()

        file_type = data_file.get_type()

        if file_type and file_type == Type.METADATA:
            self.record.add_property(Property.INSTRUMENT_TYPE,
                                     self.__retrieve_instrument_type(data_file.get_seq_folder_path()))
            details[file_type] = self.add_link(file_id)
        elif file_type:
            if file_type not in details:
                details[file_type] = []

            details[file_type].append(self.add_link(file_id))

        self.record.set_details(details)

    @staticmethod
    def __retrieve_instrument_type(run_folder):
        try:
            run_info = ET.parse(os.path.join(run_folder, 'RunInfo.xml')).getroot()
            run = run_info.find('Run')
            instrument = run.find('Instrument')

            return get_instrument_type_from_name(instrument.text)
        except IOError as e:
            logging.error("Failed to read RunInfo.xml in {}: {}".format(run_folder, e))
        except AttributeError as e:
            logging.error("Failed to find instrument type in RunInfo.xml: {}".format(e))
        except Exception as e:
            logging.error("Parse error: {}".format(e))

        return None


class RawSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        pass
