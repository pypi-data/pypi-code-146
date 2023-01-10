#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
import logging
import os
import requests
import subprocess

import dxpy

from soyuz.utils import UploaderException, read_in_chunks, FolderAlreadyExistsException, NotValidFolderException


class Storage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_target_dir(self):
        raise NotImplementedError()

    @abstractmethod
    def upload_file(self):
        raise NotImplementedError()

    @abstractmethod
    def remove_target_dir(self, folder):
        raise NotImplementedError()


class DNAnexusStorage(Storage):
    NAME = "dnanexus"

    def __init__(self, context):
        # type: (Context) -> None

        settings = context.get_settings()

        self.basedir = settings.get_base_dir()
        self.token = settings.get_token()
        self.ua_path = settings.get_ua_path()
        self.ua_parameters = settings.get_ua_parameters()
        self.__project = context.get_project_id()

        super(DNAnexusStorage, self).__init__()

    def get_project_id(self):
        return self.__project

    def get_project(self):
        return dxpy.DXProject(self.get_project_id())

    def get_file_by_id(self, file_id):
        return dxpy.get_handler(file_id)

    def validate_target_dir(self, folder):
        if not folder.is_valid:
            raise NotValidFolderException(
                    "{} is not valid".format(folder.get_name()))
        project = dxpy.DXProject(self.get_project_id())
        try:
            entities = project.list_folder(os.path.join(self.basedir, folder.get_name()))
            if len(entities["objects"]) > 0 or len(entities["folders"]) > 0:
                raise FolderAlreadyExistsException(
                    "{} already exists under {}".format(folder.get_name(), self.basedir))
        except dxpy.exceptions.ResourceNotFound:
            pass

    def upload_file(self, data_file, remote_folder, types, properties):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        dx_file = dxpy.upload_local_file(data_file.get_full_path(),
                                         folder=remote_folder,
                                         keep_open=True,
                                         parents=True)
        if dx_file:
            dx_file.add_types(types)
            dx_file.set_properties(properties)
            dx_file.close()
        else:
            raise UploaderException("Failed to upload {}".format(data_file.get_full_path()))
        return dx_file.get_id()

    def remove_target_dir(self, folder):
        logging.debug("{} folder will be removed from DNANexus".format(folder.get_name()))

        project = dxpy.DXProject(self.get_project_id())
        project.remove_folder(os.path.join(self.basedir, folder.get_name()), recurse=True, force=True)


class DNAnexusStorageUA(DNAnexusStorage):
    def upload_file(self, data_file, remote_folder, types, properties):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        args = [r'"{}"'.format(self.ua_path), data_file.get_full_path().replace("(", "\(").replace(")", "\)")]
        args.extend(["--auth-token", self.token])
        args.extend(["-p", self.get_project_id()])
        args.extend(["-f", remote_folder])
        args.extend([self.ua_parameters])
        args.extend(["--type {}".format(_type) for _type in types])
        args.extend(["--property {}={}".format(key, val) for key, val in properties.items()])
        file_id = subprocess.check_output(" ".join(args), shell=True).strip().decode('utf8').replace("'", '"')
        return file_id


class ExodusStorage(Storage):
    NAME = "stella"

    def __init__(self, settings):
        if not settings.get_exodus_url():
            raise UploaderException("Exodus URL was not specified")

        self.base_headers = {}
        self.basedir = settings.get_base_dir()
        self.exodus_url = settings.get_exodus_url()
        self.exodus_username = settings.get_exodus_username()
        self.exodus_password = settings.get_exodus_password()
        self.chunk_size = settings.get_chunk_size()

        if settings.get_exodus_aws_access_key_id():
            self.base_headers['X-AWS_ACCESS_KEY_ID'] = settings.get_exodus_aws_access_key_id()

        if settings.get_exodus_aws_secret_access_key():
            self.base_headers['X-AWS_SECRET_ACCESS_KEY'] = settings.get_exodus_aws_secret_access_key()

        if settings.get_exodus_s3_bucket_name():
            self.base_headers['X-AWS_S3_BUCKET_NAME'] = settings.get_exodus_s3_bucket_name()

        if settings.get_exodus_aws_region():
            self.base_headers['X-AWS_DEFAULT_REGION'] = settings.get_exodus_aws_region()

        if settings.get_exodus_sample_source():
            self.base_headers['X-SAMPLE_SOURCE'] = settings.get_exodus_sample_source()

        super(ExodusStorage, self).__init__()

    def validate_target_dir(self, folder):
        if not folder.is_valid:
            raise NotValidFolderException(
                    "{} is not valid".format(folder.get_name()))

    def upload_file(self, data_file, remote_folder, types, properties):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        data = {'name': data_file.get_name(),
                'folder': remote_folder,
                'types': types,
                'properties': properties,
                'tags': []}
        response = requests.post(os.path.join(self.exodus_url, "2.0/data/files/new"), json=data, auth=(self.exodus_username, self.exodus_password), headers=self.base_headers)
        response.raise_for_status()
        data = response.json()
        file_id = data['file']['link']
        uploadId = data['uploadId']

        with open(data_file.get_full_path(), 'rb') as file_object:
            parts = []
            for i, chunk in enumerate(read_in_chunks(file_object, self.chunk_size)):
                data = {'file': {
                            'link': file_id},
                        'uploadId': uploadId,
                        'part': i+1}
                response = requests.post(os.path.join(self.exodus_url, "2.0/data/files/part-upload"), json=data, auth=(self.exodus_username, self.exodus_password), headers=self.base_headers)
                response.raise_for_status()
                data = response.json()
                uploadUrl = data['uploadUrl']

                response = requests.put(uploadUrl, data=chunk, headers=self.base_headers)
                response.raise_for_status()
                headers = response.headers
                etag = headers['ETag']
                parts.append({'eTag': etag,
                              'part': i+1})

        data = {'file': {
                    'link': file_id},
                'uploadId': uploadId,
                'contentLength': os.path.getsize(data_file.get_full_path()),
                'parts': parts
                }
        response = requests.post(os.path.join(self.exodus_url, "2.0/data/files/finish-upload"), json=data, auth=(self.exodus_username, self.exodus_password), headers=self.base_headers)
        response.raise_for_status()
        data = response.json()
        file_id = data['link']
        logging.info("Successfully uploaded: {} to {}".format(data_file.get_full_path(), remote_folder))
        return file_id

    def remove_target_dir(self, folder):
        raise NotImplementedError()


class StorageType(object):
    DNANEXUS = DNAnexusStorage.NAME
    EXODUS = ExodusStorage.NAME
    DEFAULT = DNANEXUS
    ALL = [DNANEXUS, EXODUS]


class StorageFactory(object):
    @staticmethod
    def create(context):
        # type: (Context) -> Storage
        settings = context.get_settings()

        if settings.get_storage() == DNAnexusStorage.NAME:
            return DNAnexusStorageUA(context) if settings.get_ua_path() else DNAnexusStorage(context)
        elif settings.get_storage() == ExodusStorage.NAME:
            return ExodusStorage(settings)
        raise UploaderException("Storage with name {} was not found".format(settings.get_storage()))
