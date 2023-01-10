#!/usr/bin/env python

import logging
import os
import re
import threading
import time
from abc import ABCMeta, abstractmethod

import zope.event.classhandler

from soyuz.data.files import WesDataFile, RawDataFile, QcDataFile, PersonalisDataFile, PersonalisQcDataFile, \
    SangerDataFile, NgsDataFile, TarDataFile
from soyuz.dx.context import Context
from soyuz.dx.variables import Type
from soyuz.event.upload import UploadJobTerminated, SeqFolderUploadStart, SeqFolderUploadComplete, \
    SeqFolderUploadTerminated
from soyuz.utils import UploaderException, NotValidFolderException, stoppable_sleep


class WatchDirectory(object):
    UPLOADED_FILE = ".uploaded"
    UPLOADING_FILE = ".uploading"

    def __init__(self, context):
        # type: (Context) -> None
        self.__context = context
        self.__path = self.__context.get_params().get_folder()
        self.__lock = threading.Lock()

        self.__init_listeners()

    def is_uploaded(self, folder):
        return str(folder) in self.__read_file(self.__uploaded_file)

    def is_uploading(self, folder):
        return str(folder) in self.__read_file(self.__uploading_file)

    def complete(self, folder):
        self.remove_folder_from_uploading_file(str(folder))
        self.__write_file(self.__uploaded_file, str(folder))

    def start_upload(self, folder):
        self.remove_folder_from_uploaded_file(str(folder))
        self.__write_file(self.__uploading_file, str(folder))

    def remove_uploaded_file(self):
        if os.path.exists(self.__uploaded_file):
            os.remove(self.__uploaded_file)

    def remove_uploading_file(self):
        if os.path.exists(self.__uploading_file):
            os.remove(self.__uploading_file)

    def remove_folder_from_uploading_file(self, seq_folder_name):
        if os.path.exists(self.__uploading_file):
            self.__remove_from_file(self.__uploading_file, seq_folder_name)

    def remove_folder_from_uploaded_file(self, seq_folder_name):
        if os.path.exists(self.__uploaded_file):
            self.__remove_from_file(self.__uploaded_file, seq_folder_name)

    def __init_listeners(self):
        @zope.event.classhandler.handler(SeqFolderUploadStart)
        def on_seq_folder_upload_start(event):
            # type: (SeqFolderUploadStart) -> None

            self.start_upload(event.seq_folder.get_name())

        @zope.event.classhandler.handler(SeqFolderUploadComplete)
        def on_seq_folder_upload_complete(event):
            # type: (SeqFolderUploadComplete) -> None

            self.complete(event.seq_folder.get_name())

        @zope.event.classhandler.handler(SeqFolderUploadTerminated)
        def on_seq_folder_upload_terminated(event):
            # type: (SeqFolderUploadTerminated) -> None

            self.remove_folder_from_uploading_file(event.seq_folder.get_name())
            self.remove_folder_from_uploading_file(event.seq_folder.get_name())

    @property
    def __uploaded_file(self):
        return os.path.join(self.__context.get_params().get_folder(), self.UPLOADED_FILE)

    @property
    def __uploading_file(self):
        return os.path.join(self.__context.get_params().get_folder(), self.UPLOADING_FILE)

    def get_seq_folders(self):
        return self.__get_seq_folders(self.__path)

    def __get_seq_folders(self, root):
        result = []
        if not os.path.exists(root):
            logging.error("Watch directory {} doesn't exist".format(root))
            return result

        for f in os.listdir(root):
            path = os.path.join(root, f)
            if os.path.isdir(path):
                seq_folder = SeqFolderFactory.create(root, f, self.__context)
                if seq_folder:
                    result.append(seq_folder)
                else:
                    result += self.__get_seq_folders(path)
        return result

    @staticmethod
    def __read_file(file_with_history):
        result = []
        if not os.path.isfile(file_with_history):
            return result
        with open(file_with_history, "r") as f:
            for line in f.readlines():
                result.append(line.strip())
        return result

    def __write_file(self, file_with_history, seq_folder_name):
        try:
            self.__lock.acquire()
            with open(file_with_history, "a") as f:
                f.write("{}\n".format(seq_folder_name))
        finally:
            self.__lock.release()

    def __remove_from_file(self, file_with_history, seq_folder_name):
        try:
            self.__lock.acquire()
            with open(file_with_history, "r") as f:
                content = f.readlines()

            with open(file_with_history, "w") as f:
                for line in content:
                    if seq_folder_name in line:
                        continue

                    f.write(line)
        finally:
            self.__lock.release()


class SeqFolderBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, path):
        self._path = self.__get_abs_path(path).replace("\\", "/")

    def get_name(self):
        return os.path.basename(self._path)

    def get_path(self):
        return self._path

    @property
    @abstractmethod
    def is_valid(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_completed(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def complete(self):
        raise NotImplementedError()

    def is_older_than(self, seconds):
        return time.time() - os.path.getmtime(self.__str__()) > seconds

    @abstractmethod
    def list_files(self):
        raise NotImplementedError()

    @staticmethod
    def __get_abs_path(path):
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(abs_path):
            raise UploaderException("{} does not exist".format(abs_path))
        return abs_path


class WesSignateraSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("[A-Z0-9]*_[0-9]{8}")

    def __init__(self, path):
        SeqFolderBase.__init__(self, path)
        self.__wes_subfolder = os.path.join(self._path, "WES_data")
        self.__qc_subfolder = os.path.join(self._path, "QC_reports")

    @property
    def is_valid(self):
        if WesSignateraSeqFolder.FOLDER_REGEX.match(self.get_name()) is None \
                or not os.path.isdir(self.__wes_subfolder) \
                or not os.path.isdir(self.__qc_subfolder):
            return False

        if len(self.__list_from_wes()) == 0:
            logging.info("{} does not contain any data".format(self.__wes_subfolder))
            return False
        if len(self.__list_from_qc_reports()) == 0:
            logging.info("{} does not contain any data".format(self.__qc_subfolder))
            return False

        success = True
        for f in self.list_files():
            if not f.is_valid:
                logging.info("{} has invalid format".format(f.get_full_path()))
                success = False
        return success

    def list_files(self):
        return self.__list_from_wes() + self.__list_from_qc_reports()

    def __list_from_wes(self):
        result = []
        for f in os.listdir(self.__wes_subfolder):
            result.append(WesDataFile(self.__wes_subfolder, f, self))
        return result

    def __list_from_qc_reports(self):
        result = []
        for f in os.listdir(self.__qc_subfolder):
            result.append(QcDataFile(self.__qc_subfolder, f, self))
        return result


class PersonalisSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("^[A-Za-z0-9_-]{1,48}$")

    def __init__(self, path):
        SeqFolderBase.__init__(self, path)
        self.__alignment_subfolder = os.path.join(self._path, '{}', "Alignment")
        self.__fastq_subfolder = os.path.join(self._path, '{}', "FASTQ")
        self.__qc_metrics_path = self._path

    @property
    def is_valid(self):
        if PersonalisSeqFolder.FOLDER_REGEX.match(self.get_name()) is None:
            return False

        if len(self.__list_qc_metrics(self._path)) == 0:
            logging.info("{} does not contain any data".format(self.__qc_metrics_path))
            return False

        for folder in os.listdir(self._path):
            if not os.path.isdir(os.path.join(self._path, folder)):
                continue
            if not os.path.isdir(self.__alignment_subfolder.format(folder)):
                return False
            if len(self.__list_from(self.__alignment_subfolder.format(folder))) == 0:
                logging.info("{} does not contain any data".format(self.__alignment_subfolder))
                return False
            if os.path.isdir(self.__fastq_subfolder.format(folder)) and \
                    len(self.__list_from(self.__fastq_subfolder.format(folder))) == 0:
                logging.info("{} does not contain any data".format(self.__fastq_subfolder))
                return False

        success = True
        for f in self.list_files():
            if not f.is_valid:
                logging.info("{} has invalid format".format(f.get_full_path()))
                success = False
        return success

    def list_files(self):
        list_files = self.__list_qc_metrics(self._path)
        for folder in os.listdir(self._path):
            if not os.path.isdir(os.path.join(self._path, folder)):
                continue
            list_files.extend(self.__list_from(self.__alignment_subfolder.format(folder)))
            if os.path.isdir(self.__fastq_subfolder.format(folder)):
                list_files.extend(self.__list_from(self.__fastq_subfolder.format(folder)))
        return list_files

    def __list_from(self, subfolder):
        result = []
        for f in os.listdir(subfolder):
            result.append(PersonalisDataFile(subfolder, f, self))
        return result

    def __list_qc_metrics(self, path):
        result = []
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                result.append(PersonalisQcDataFile(path, f, self))
        return result


class RawSeqFolder(SeqFolderBase):
    def __init__(self, path):
        super(RawSeqFolder, self).__init__(path)

    @property
    def is_valid(self):
        return True

    def list_files(self):
        result = []
        for root, subdirs, files in os.walk(self._path):
            for f in files:
                result.append(RawDataFile(root, f, self))
        return result


class BgiSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("V[A-Za-z0-9]{9}")

    def __init__(self, path):
        super(BgiSeqFolder, self).__init__(path)
        self.__lane_folders = [os.path.join(self._path, lane) for lane in ["L01", "L02", "L03", "L04"]]
        self.__wes_subfolder = os.path.join(self._path, "WES_data")
        self.__qc_subfolder = os.path.join(self._path, "QC_reports")

    @property
    def is_completed(self):
        if self.is_valid:
            return all([os.path.isfile(os.path.join(lane_folder,
                                                    "{}_{}_FileInfo.csv".format(os.path.basename(self._path),
                                                                                os.path.basename(lane_folder)))) for
                        lane_folder in self.__lane_folders])
        return False

    @property
    def is_valid(self):
        if (BgiSeqFolder.FOLDER_REGEX.match(self.get_name())
                and all([os.path.join(self._path, folder) in self.__lane_folders for folder in os.listdir(self._path) if
                         os.path.isdir(os.path.join(self._path, folder))])):
            return True
        return False

    def list_files(self):
        result = []
        for root, subdirs, files in os.walk(self._path):
            for f in files:
                result.append(RawDataFile(root, f, self))
        return result


class SangerSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("^[0-9\\-]{10}_[A-Za-z0-9_\\-]*_[A-Za-z0-9\\-]*_Q[0-9]*$")
    WITH_QUADRANT_FILES_COUNT = 96

    def __init__(self, path, check_interval):
        super(SangerSeqFolder, self).__init__(path)
        self.__check_interval = check_interval
        self.__force_stop = False

        @zope.event.classhandler.handler(UploadJobTerminated)
        def on_upload_job_terminated(event):
            # type: (UploadJobTerminated) -> None
            if self.get_name() == event.seq_folder_name:
                self.__force_stop = True

    @property
    def is_completed(self):
        return len(self.__list_files()) == self.WITH_QUADRANT_FILES_COUNT

    @property
    def is_valid(self):
        return bool(SangerSeqFolder.FOLDER_REGEX.match(self.get_name()))

    def list_files(self):
        while not self.__force_stop:
            result = self.__list_files()

            logging.info("Found {} files for {}".format(len(result), self.get_name()))

            if len(result) > self.WITH_QUADRANT_FILES_COUNT:
                raise NotValidFolderException('Data folder is not in a valid state')

            if len(result) == self.WITH_QUADRANT_FILES_COUNT:
                return result

            stoppable_sleep(self.__check_interval, lambda: self.__force_stop)

        return []

    def __list_files(self):
        result = []
        for root, subdirs, files in os.walk(self._path):
            for f in files:
                data_file = SangerDataFile(root, f, self)
                if data_file.is_valid:
                    result.append(data_file)

        return result


class NgsSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile('^[0-9]{6,8}_[A-Za-z0-9]*_[0-9]*_[^_ ]*$')

    def __init__(self, path, completion_marker, check_interval, file_age_time, archive_temp_folder):
        super(NgsSeqFolder, self).__init__(path)

        self.__archived_files = {}
        self.__archive_part_index = 0
        self.__completion_marker = completion_marker
        self.__check_interval = check_interval
        self.__file_age_time = file_age_time
        self.__temp_tar_file_folder = os.path.join(archive_temp_folder, self.get_name())
        self.__force_stop = False

        @zope.event.classhandler.handler(UploadJobTerminated)
        def on_upload_job_terminated(event):
            # type: (UploadJobTerminated) -> None
            if self.get_name() == event.seq_folder_name:
                self.__force_stop = True

    @property
    def is_valid(self):
        return bool(NgsSeqFolder.FOLDER_REGEX.match(self.get_name()))

    def list_files(self):
        while not self.__force_stop:
            is_completion_marker_exists = os.path.exists(os.path.join(self._path, self.__completion_marker))
            wait_time = max(self.__check_interval,
                            self.__file_age_time) if is_completion_marker_exists else self.__check_interval

            stoppable_sleep(wait_time, lambda: self.__force_stop)

            files_to_upload = self.__find_files_to_upload()
            if len(files_to_upload) != 0:
                tar_archive_name = "upload_{:03d}.tar.gz".format(self.__archive_part_index)
                tar_archive = TarDataFile(self.__temp_tar_file_folder, tar_archive_name, self, Type.BCL)
                tar_archive.add_files(files_to_upload)
                tar_archive.create_tar_archive()

                self.__archive_part_index += 1

                yield tar_archive
            else:
                logging.info('List of files for upload is empty')

            if is_completion_marker_exists:
                logging.info('The completion marker {} was found'.format(self.__completion_marker))
                break

        if not self.__force_stop:
            yield self.__create_metadata_tar_archive()

    def __find_files_to_upload(self):
        files_to_upload = []

        for root, subdirs, files in os.walk(self._path):
            for f in files:
                data_file = NgsDataFile(root, f, self)

                if data_file.is_valid:
                    cur_time = int(time.time())
                    cur_mtime = os.path.getmtime(data_file.get_full_path())
                    file_was_change = cur_mtime > self.__archived_files.get(data_file.get_full_path(), 0)

                    if cur_time - cur_mtime > self.__file_age_time:
                        if file_was_change:
                            files_to_upload.append(data_file.get_full_path())
                            self.__archived_files[data_file.get_full_path()] = cur_mtime
                    else:
                        logging.info(
                            "Age of file {} is {} less then {}. Skipping...".format(data_file.get_full_path(),
                                                                                    cur_time - cur_mtime,
                                                                                    self.__file_age_time))
        return files_to_upload

    def __create_metadata_tar_archive(self):
        metadata_files = ["RunInfo.xml", "Data/Intensities/config.xml", "runParameters.xml", "RunParameters.xml"]
        metadata_folders = ["InterOp"]
        metadata_tar_archive = TarDataFile(self.__temp_tar_file_folder, 'metadata.tar.gz', self, Type.METADATA)

        for metadata_file in metadata_files + metadata_folders:
            full_path = os.path.join(self._path, metadata_file)

            if os.path.exists(full_path):
                metadata_tar_archive.add_file(full_path)

        metadata_tar_archive.create_tar_archive()

        return metadata_tar_archive


class SeqFolderFactory(object):
    @staticmethod
    def create(base_path, name, context):
        params = context.get_params()

        if BgiSeqFolder.FOLDER_REGEX.match(name):
            return BgiSeqFolder(os.path.join(base_path, name))
        if WesSignateraSeqFolder.FOLDER_REGEX.match(name):
            return WesSignateraSeqFolder(os.path.join(base_path, name))
        if SangerSeqFolder.FOLDER_REGEX.match(name):
            return SangerSeqFolder(os.path.join(base_path, name), params.get_sanger_check_interval())
        if NgsSeqFolder.FOLDER_REGEX.match(name):
            return NgsSeqFolder(os.path.join(base_path, name),
                                params.get_ngs_completion_marker(),
                                params.get_ngs_check_interval(),
                                params.get_ngs_file_age_time(),
                                params.get_ngs_archive_temp_folder())

        logging.error("Folder {} is not allowed.".format(os.path.join(base_path, name)))

        return None

    @staticmethod
    def create_from_full_path(full_path, context):
        base_path, name = SeqFolderFactory.__parse_full_path(full_path)
        return SeqFolderFactory.create(base_path, name, context)

    @staticmethod
    def __parse_full_path(full_path):
        path = full_path.rstrip('/')
        return os.path.dirname(path), os.path.basename(path)
