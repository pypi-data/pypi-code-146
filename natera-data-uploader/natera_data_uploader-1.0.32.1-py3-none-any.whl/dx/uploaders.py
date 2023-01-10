#!/usr/bin/env python

import logging
import threading
from multiprocessing.pool import ThreadPool
import os
import time
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

import zope.event
import zope.event.classhandler

from soyuz.data.folders import WesSignateraSeqFolder, PersonalisSeqFolder, RawSeqFolder, BgiSeqFolder, SeqFolderBase, \
    SangerSeqFolder, NgsSeqFolder
from soyuz.data.storages import StorageFactory
from soyuz.dx.context import Context
from soyuz.dx.sentinels import WesSignateraSentinel, RawSentinel, PersonalisSentinel, SangerSentinel, NgsSentinel
from soyuz.dx.variables import Type, Property
from soyuz.event.upload import SeqFolderUploadStart, SeqFolderUploadComplete, UploadJobTerminated, \
    SeqFolderUploadTerminated, NewUploadJob
from soyuz.utils import UploaderException, timeit, get_expected_time, NotValidFolderException


@contextmanager
def poolcontext(*args, **kwargs):
    pool = ThreadPool(*args, **kwargs)
    yield pool
    pool.terminate()


class WatchUploader(object):
    __metaclass__ = ABCMeta

    def __init__(self, context):
        # type: (Context) -> None

        self.__context = context

    def watch(self, watch_dir):
        if self.__context.get_params().is_force_upload():
            watch_dir.remove_uploaded_file()
            watch_dir.remove_uploading_file()

        while True:
            for seq_folder in watch_dir.get_seq_folders():
                if watch_dir.is_uploaded(seq_folder.get_name()):
                    logging.info("{} already uploaded. Skipping".format(seq_folder.get_name()))
                    continue

                if watch_dir.is_uploading(seq_folder.get_name()):
                    logging.info("{} is uploading. Skipping".format(seq_folder.get_name()))
                    continue

                threading.Thread(target=self.__upload, args=(seq_folder,), daemon=True).start()

            time.sleep(self.__context.get_settings().get_interval())

    def __upload(self, seq_folder):
        try:
            uploader = DxUploaderFactory.create(self.__context, seq_folder)
            uploader.upload(seq_folder)
        except Exception as e:
            logging.error("{}. Skipping".format(e))


class DxUploaderBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, context):
        # type: (Context) -> None

        self._params = context.get_params()
        self._settings = context.get_settings()
        self._storage = StorageFactory.create(context)
        self.__terminated_seq_folder_names = set()
        self.__upload_conditions = {}
        self.__seq_folder_name_to_upload_job_id = {}

        self.__init_listeners()

    def __call__(self, data_file):
        return self.upload_file(data_file)

    @timeit
    def upload(self, seq_folder):
        try:
            if self._params.is_force_upload():
                logging.info("Force upload is enabled, removing folder {} before upload".format(seq_folder.get_name()))

                self.remove_target_dir(seq_folder)

            self._validate_target_dir(seq_folder)

            logging.info("Starting upload for {}".format(seq_folder.get_name()))

            sentinel = self._create_sentinel(seq_folder.get_name())

            zope.event.notify(SeqFolderUploadStart(seq_folder, sentinel))

            if self._params.is_constellation_portal_mode():
                event = threading.Event()
                self.__upload_conditions[seq_folder.get_name()] = event
                logging.info("Constellation mode is enabled, waiting for the job to be started from Constellation Portal")
                event.wait()

                sentinel.add_property(Property.JOB_ID, self.__seq_folder_name_to_upload_job_id[seq_folder.get_name()])

            if self._settings.get_process_count() > 1:
                with poolcontext(processes=self._settings.get_process_count()) as pool:
                    results = pool.map(self, seq_folder.list_files())
            else:
                results = [self.upload_file(data_file) for data_file in seq_folder.list_files()]

            if seq_folder.get_name() not in self.__terminated_seq_folder_names:
                for data_file, file_id in results:
                    sentinel.add_file(data_file, file_id)

                sentinel.close()

                logging.info("{} folder has been successfully uploaded".format(seq_folder.get_name()))
                zope.event.notify(SeqFolderUploadComplete(seq_folder))
            else:
                zope.event.notify(SeqFolderUploadTerminated(seq_folder))
                logging.info("Upload {} folder has been terminated".format(seq_folder.get_name()))
                self.__terminated_seq_folder_names.remove(seq_folder.get_name())
        except NotValidFolderException as e:
            logging.error("Upload {} folder has been failed due to validation error: {}".format(seq_folder.get_name(), e))
            self.remove_target_dir(seq_folder)
            raise e

    def upload_file(self, data_file):
        if data_file.get_seq_folder_name() not in self.__terminated_seq_folder_names:
            remote_folder = os.path.join(self._settings.get_base_dir(),
                                         data_file.get_seq_folder_name(),
                                         data_file.get_relative_path()).replace("\\", "/")
            types = self._get_additional_types(data_file)
            types.append(Type.UPLOAD_DATA)
            properties = self._get_additional_properties(data_file, data_file.get_seq_folder_name())
            properties[Property.RUN_FOLDER] = data_file.get_seq_folder_name()
            file_id = self._storage.upload_file(data_file, remote_folder, types, properties)
            return data_file, file_id
        else:
            return data_file, None

    def remove_target_dir(self, seq_folder):
        self._storage.remove_target_dir(seq_folder)

    def _validate_target_dir(self, folder):
        self._storage.validate_target_dir(folder)

    @abstractmethod
    def _create_sentinel(self, seq_folder_name):
        raise NotImplementedError()

    @abstractmethod
    def _get_additional_types(self, data_file):
        raise NotImplementedError()

    @abstractmethod
    def _get_additional_properties(self, data_file, seq_folder_name):
        raise NotImplementedError()

    def __init_listeners(self):
        @zope.event.classhandler.handler(UploadJobTerminated)
        def on_upload_job_terminated(event):
            # type: (UploadJobTerminated) -> None
            self.__terminated_seq_folder_names.add(event.seq_folder_name)

        @zope.event.classhandler.handler(NewUploadJob)
        def on_new_upload_job(event):
            # type: (NewUploadJob) -> None
            if event.seq_folder_name in self.__upload_conditions:
                logging.info('Upload job was found: {}, resuming upload'.format(event.job_id))
                self.__seq_folder_name_to_upload_job_id[event.seq_folder_name] = event.job_id
                self.__upload_conditions[event.seq_folder_name].set()


class WesSignateraDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = WesSignateraSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return WesSignateraSentinel(self._storage, self._settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        types = []
        data_type = data_file.get_type()
        if data_type:
            types.append(data_type)
            if data_type == Type.CSV and data_file.get_name().startswith("WES-QCMetrics"):
                types.append(Type.WESQCREPORT)
        return types

    def _get_additional_properties(self, data_file, seq_folder_name):
        properties = {}
        if data_file.get_sample_id():
            properties[Property.SAMPLE_REFERENCE] = "{}/{}".format(seq_folder_name, data_file.get_sample_id())
        return properties


class PersonalisDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = PersonalisSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return PersonalisSentinel(self._storage, self._settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        types = []
        data_type = data_file.get_type()
        if data_type:
            types.append(data_type)
            if data_type == Type.CSV and data_file.get_name().startswith("QCMetrics"):
                types.append(Type.WESQCREPORT)
        return types

    def _get_additional_properties(self, data_file, seq_folder_name):
        properties = {}
        if data_file.get_sample_id():
            properties[Property.SAMPLE_REFERENCE] = "{}/{}".format(seq_folder_name, data_file.get_sample_id())
        return properties


class RawDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = RawSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return RawSentinel(self._storage, self._settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class BgiDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = BgiSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return RawSentinel(self._storage, self._settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class SangerDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = SangerSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return SangerSentinel(self._storage, self._settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class NgsDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = NgsSeqFolder

    def upload_file(self, data_file):
        data_file, file_id = super(NgsDxUploader, self).upload_file(data_file)

        logging.info("Removing uploaded tar file {}".format(data_file.get_full_path()))
        os.remove(data_file.get_full_path())

        return data_file, file_id

    def _create_sentinel(self, seq_folder_name):
        return NgsSentinel(self._storage,
                           self._settings.get_base_dir(),
                           seq_folder_name,
                           self._params.get_site_id(),
                           get_expected_time('NgsDxUploader', 'upload'))

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class DxUploaderFactory(object):
    @staticmethod
    def create(settings, seq_folder):
        # type: (Context, SeqFolderBase) -> DxUploaderBase

        if isinstance(seq_folder, BgiDxUploader.SEQ_FOLDER_TYPE):
            return BgiDxUploader(settings)
        elif isinstance(seq_folder, RawDxUploader.SEQ_FOLDER_TYPE):
            return RawDxUploader(settings)
        elif isinstance(seq_folder, WesSignateraDxUploader.SEQ_FOLDER_TYPE):
            return WesSignateraDxUploader(settings)
        elif isinstance(seq_folder, PersonalisDxUploader.SEQ_FOLDER_TYPE):
            return PersonalisDxUploader(settings)
        elif isinstance(seq_folder, SangerDxUploader.SEQ_FOLDER_TYPE):
            return SangerDxUploader(settings)
        elif isinstance(seq_folder, NgsDxUploader.SEQ_FOLDER_TYPE):
            return NgsDxUploader(settings)
        raise UploaderException(
            "Uploader for the folder {} was not found".format(seq_folder.get_name()))
