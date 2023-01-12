#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 5:39
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : hosted_backend.py
@Desc    :
"""
import base64
import json
import logging
import os
import platform
import socket
import uuid
from waveletai import envs
from waveletai.model import Model
from contextlib import closing
import requests
from waveletai.envs import CHUNK_SIZE, WARN_SIZE
from multiprocessing.dummy import Pool
from waveletai.backend import Backend
from waveletai.utils import with_api_exceptions_handler, require_app, require_model
from waveletai.dataset import Dataset, Asset
from waveletai.feature import Feature
from waveletai.model import ModelVersion
from waveletai.app import App
from waveletai.exceptions import LoginFailed, NotADirectory, MissingApiTokenException, FileUploadException, \
    InvalidAPIToken
from waveletai.constants import DataType, ModelRegisterMode, Visibility, FeatureType, DataSource, DatasetImageType
from waveletai.utils.storage_utils import UploadEntry, scan_upload_entries, SilentProgressIndicator, \
    LoggingProgressIndicator, upload_to_storage
from waveletai.utils.datastream import FileStream, FileChunkStream, FileChunk
import zipfile
from waveletai.experiment import Experiment, MLFlowExperiment, MLFlowRun, MLflowLatestMetric, MLFlowParam, MLFlowTag
import pandas as pd
import time

_logger = logging.getLogger(__name__)


class HostedBackend(Backend):

    @with_api_exceptions_handler
    def create_app(self, name, tags, desc, visibility):
        """
        : 添加新应用
        :param name str 应用名称
        :param tags list 应用标签
        :param desc str 应用描述
        :param visibility: 公有私有 public private 默认 private
        :return: Class `app` Object
        """
        res = self._session.post(url=f'{self.api_address}/application/app/',
                                 json={"name": name, "tags": tags, "desc": desc, "visibility": visibility})
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        data = res.json()['data']
        self.set_app(data['id'])
        return App(self, data['id'], data['name'], data['desc'], data['create_time'], data['create_user_id'],
                   data['update_time'], data['update_user_id'])

    @with_api_exceptions_handler
    @require_app
    def get_app(self):
        """
        : 获取应用信息，
        :return: Class `app` Object
        """
        res = self._session.get(url=f'{self.api_address}/application/app/{self.app_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return App(self, data['id'], data['name'], data['desc'], data['create_time'], data['create_user_id'],
                   data['update_time'], data['update_user_id'])

    @with_api_exceptions_handler
    @require_app
    def update_app(self, name=None, tags=None, desc=None):
        """
        更新应用信息
        :param desc:
        :param tags:
        :param name:
        :return: Class `app` Object
        """
        res = self._session.put(url=f'{self.api_address}/application/app/{self.app_id}',
                                json={"name": name, "tags": tags, "desc": desc})
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        data = res.json()['data']
        return App(self, data['id'], data['name'], data['desc'], data['create_time'], data['create_user_id'],
                   data['update_time'], data['update_user_id'])

    @with_api_exceptions_handler
    @require_app
    def delete_app(self):
        """
        : 删除项目
        :return:
        """
        res = self._session.delete(url=f'{self.api_address}/application/app/{self.app_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['code']
        return data

    @with_api_exceptions_handler
    @require_app
    def list_models(self):
        """
        : 获取应用下模型对象列表
        :return: List of Class `Model` Object
        """
        res = self._session.get(
            url=f'{self.api_address}/{self.app_id}/training/model/?query={{"app_id": "{self.app_id}"}}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    def __init__(self, api_token=None, internal_login=True):
        """
        :param api_token:
        :param internal_login: bool
            `True`:内部登录，不记录登录日志；
            `False`:外部登录，记录登录日志；
        """
        if not api_token:
            api_token = os.getenv(envs.API_TOKEN)
        if api_token:
            pass
        else:
            raise MissingApiTokenException()
        if os.getenv(envs.API_PROJ):
            self.set_app(os.getenv(envs.API_PROJ))
        if os.getenv(envs.API_MODEL):
            self.set_model(os.getenv(envs.API_MODEL))
        from waveletai import __version__
        self.client_lib_version = __version__
        self._session = requests.session()
        user_agent = 'waveletai-client/{lib_version} ({system}, python {python_version})'.format(
            lib_version=self.client_lib_version,
            system=platform.platform(),
            python_version=platform.python_version())
        headers = {'User-Agent': user_agent}

        # api-token登录
        try:
            od = json.loads(base64.b64decode(api_token).decode('utf-8'))
            if os.environ.get(envs.API_URL):
                pass
            else:
                os.environ.update({envs.API_URL: od['api_url']})
        except Exception:
            raise InvalidAPIToken()
        res = self._session.post(
            url=f'{self.api_address}/account/users/sdk/login/',
            json={'api_token': api_token, 'internal_login': internal_login},
            headers=headers,
        )
        if res.json()["message"]:
            raise LoginFailed(res.json()["message"])
        print("WaveletAI Backend connected")
        data = res.json()['data']
        api_token = 'Bearer ' + data["token"]
        user_id = data['user_id']
        os.environ.update({
            'LOGNAME': user_id
        })

        self._session.headers.update({"X-TOKEN": api_token})

    def close(self):
        """
        清理数据, 关闭连接
        :return:
        """
        clean_key = [envs.API_TOKEN, 'LOGNAME']
        for k in clean_key:
            if os.environ.get(k):
                os.environ.pop(k)
        self._session.close()

    @property
    def api_address(self):
        api_url = os.getenv(envs.API_URL)
        if api_url:
            return api_url
        return "https://ai.xiaobodata.com/api"

    @with_api_exceptions_handler
    def get_dataset(self, dataset_id):
        res = self._session.get(url=f'{self.api_address}/data/dataset/{dataset_id}')
        if res.json()["message"]:
            return None
        dict = res.json()['data']
        self.set_app(dict['app_id'])

        return Dataset(self, dict['id'], dict['name'], dict['visibility'], dict['desc'], dict['create_time'],
                       dict['type'],
                       dict['create_user_id'], dict['update_time'], dict['update_user_id'])

    @with_api_exceptions_handler
    @require_app
    def update_dataset(self, dataset_id, name, visibility, desc, label_type=None):
        """
        更新数据集信息
        :param desc: 数据集描述
        :param visibility: 可见性
        :param name: 数据集名字
        :param dataset_id: 数据集id
        :return: Class `Dataset` Object
        """
        jsondata = {}
        if name:
            jsondata['name'] = name
        if visibility and visibility in (Visibility.PRIVATE.value, Visibility.PUBLIC.value):
            jsondata['visibility'] = visibility
        if desc:
            jsondata['desc'] = desc
        if label_type is not None:
            if label_type != DatasetImageType.CLASSIFY.value\
            and label_type != DatasetImageType.POLYGON.value\
            and label_type != DatasetImageType.RECTANGLE.value:
                raise Exception(f'图片数据集类型{label_type}不存在')
            jsondata['json_data'] = {'labelType': label_type}
        res = self._session.put(url=f'{self.api_address}/{self.app_id}/data/dataset/{dataset_id}', json=jsondata)
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    @require_app
    def delete_dataset(self, dataset_id):
        """
        删除数据集
        :param dataset_id:
        :return:
        """
        res = self._session.delete(url=f'{self.api_address}/{self.app_id}/data/dataset/{dataset_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    @require_app
    def create_dataset(self, name, path, data_type=DataType.TYPE_FILE.value, visibility=Visibility.PRIVATE.value,
                       desc=None, label_type=None):
        json={'name': name, 'type': data_type, 'visibility': visibility, 'desc': desc}
        if data_type == DataType.TYPE_IMAGE.value:
            if label_type != DatasetImageType.CLASSIFY.value\
            and label_type != DatasetImageType.POLYGON.value\
            and label_type != DatasetImageType.RECTANGLE.value:
                raise Exception(f'图片数据集类型{label_type}不存在')
            json={'name': name, 'type': data_type, 'visibility': visibility, 'desc': desc, 'json_data':{'labelType': label_type}}
        res = self._session.post(
            url=f'{self.api_address}/{self.app_id}/data/dataset/',
            json=json,
        )
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        print(f"Dataset id = {res.json()['data']['id']} created succ")

        dict = res.json()['data']
        self.upload_dataset_artifacts(dict['id'], path)
        return Dataset(self, dict['id'], dict['name'], dict['visibility'], dict['desc'], dict['create_time'],
                       dict['type'],
                       dict['create_user_id'], dict['update_time'], dict['update_user_id'])

    @with_api_exceptions_handler
    def upload_dataset_artifacts(self, dataset_id, path):
        """
        :param dataset_id: 文件所属数据集
        :param path: 要上传的文件夹/文件路径
        :return:  上传文件 succ，共xxx个
        """

        entries = scan_upload_entries({UploadEntry(path)})
        upload_to_storage(entries, self._dataset_upload, self._dataset_chunk_upload_loop,
                          warn_limit=WARN_SIZE, oid=dataset_id)

    @with_api_exceptions_handler
    # @retrying(stop_max_attempt_number=3)
    @require_app
    def _dataset_upload(self, entry: UploadEntry, oid):
        dataset_id = oid
        fs = FileStream(entry)
        progress_indicator = SilentProgressIndicator(fs.length, fs.filename)
        payload = {"path": entry.prefix.replace('\\', '/'), "dataset_id": dataset_id, 'final': 'true'}
        res = self._session.post(url=f'{self.api_address}/{self.app_id}/data/dataset/upload', files=[('file', (
            fs.filename, fs.fobj, fs.content_type))], data=payload)
        if res.json()["message"]:
            _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            raise FileUploadException(fs.filename)
        else:
            progress_indicator.complete()
        fs.close()

    @with_api_exceptions_handler
    # @retrying(stop_max_attempt_number=3)
    @require_app
    def _dataset_chunk_upload_loop(self, entry: UploadEntry, oid):
        uid = uuid.uuid4()
        dataset_id = oid
        stream = FileChunkStream(entry)
        progress_indicator = LoggingProgressIndicator(stream.length, stream.filename)
        for ind, fc in enumerate(stream.generate(chunk_size=CHUNK_SIZE * 1024 * 1)):
            self._dataset_chunk_upload(fc, entry.filename, str(ind), entry.prefix.replace('\\', '/'),
                                       progress_indicator, dataset_id, uid)

        res = self._session.get(url=f'{self.api_address}/{self.app_id}/data/dataset/upload/success',
                                params={'filename': entry.filename, 'dataset_id': dataset_id,
                                        'path': entry.prefix.replace('\\', '/'), 'uuid': uid, 'final': 'true'})
        if res.json()["message"]:
            _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            raise FileUploadException(entry.filename)
        else:
            progress_indicator.complete()
        stream.close()

    @with_api_exceptions_handler
    @require_app
    def _dataset_chunk_upload(self, file: FileChunk, filename, chunk, path, progress_indicator, oid, uid):
        dataset_id = oid
        payload = {"chunk": chunk, "path": path, "dataset_id": dataset_id, "uuid": uid}
        res = self._session.post(url=f'{self.api_address}/{self.app_id}/data/dataset/upload',
                                 files=[('file', (file.data))],
                                 data=payload)
        if res.json()["message"]:
            _logger.error(f"file {filename} upload failed,{res.json()['message']}")
            raise FileUploadException(filename + '_' + chunk)
        else:
            progress_indicator.progress(file.end - file.start)

    @with_api_exceptions_handler
    @require_model
    # @retrying(stop_max_attempt_number=3)
    def _model_upload(self, entry: UploadEntry, oid):
        model_repo_id = oid
        fs = FileStream(entry)
        progress_indicator = SilentProgressIndicator(fs.length, fs.filename)
        payload = {"path": entry.prefix, "task_id": model_repo_id}
        res = self._session.post(url=f'{self.api_address}/{self.model_id}/deploy/model/upload', files=[('file', (
            fs.filename, fs.fobj, fs.content_type))], data=payload)
        if res.json()["message"]:
            _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            raise FileUploadException(fs.filename)
        else:
            progress_indicator.complete()
        fs.close()

    @with_api_exceptions_handler
    @require_model
    def _model_chunk_upload_loop(self, entry: UploadEntry, oid):
        uid = uuid.uuid4()
        model_repo_id = oid
        stream = FileChunkStream(entry)
        progress_indicator = LoggingProgressIndicator(stream.length, stream.filename)
        for ind, fc in enumerate(stream.generate(chunk_size=CHUNK_SIZE * 1024 * 20)):
            self._model_chunk_upload(fc, entry.filename, str(ind), entry.prefix, progress_indicator, model_repo_id, uid)

        res = self._session.get(url=f'{self.api_address}/{self.model_id}/deploy/model/upload/success',
                                params={'filename': entry.filename, 'uuid': uid, 'task_id': model_repo_id, 'path': entry.prefix})
        if res.json()["message"]:
            _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            raise FileUploadException(entry.filename)
        else:
            progress_indicator.complete()
        stream.close()

    # @retrying(stop_max_attempt_number=3)
    @require_model
    def _model_chunk_upload(self, file: FileChunk, filename, chunk, path, progress_indicator, oid, uid):
        model_repo_id = oid
        payload = {"chunk": chunk, "path": path, "uuid": uid, "task_id": model_repo_id}
        res = self._session.post(url=f'{self.api_address}/{self.model_id}/deploy/model/upload',
                                 files=[('file', (file.data))],
                                 data=payload)
        if res.json()["message"]:
            _logger.error(f"file {filename} upload failed,{res.json()['message']}")
            # raise FileUploadException(filename + '_' + chunk)
        else:
            progress_indicator.progress(file.end - file.start)

    @with_api_exceptions_handler
    def _url_download(self, urls):
        url, destination, filename = urls
        destination_loc = os.path.join(destination, filename)
        content_size = 0
        # headers_types = ['application/octet-stream', 'application/zip', 'image/png', 'image/jpeg',
        #                  'application/vnd.ms-excel', 'text/plain', 'application/json', 'application/xml',
        #                  'application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
        progress_indicator = None
        with closing(requests.get(url, stream=True)) as response:
            # 暂时取消文件类型校验
            # if response.headers.get('Content-Type') not in headers_types:
            #     _logger.error(f"当前文件 {filename} 不是可下载的文件流地址，请检查后再试")
            #     return
            if 'Content-Length' in response.headers:
                content_size = int(response.headers.get('Content-Length'))  # 内容体总大小
            else:
                content_size = len(response.content)
            if content_size >= WARN_SIZE:
                progress_indicator = LoggingProgressIndicator(content_size, filename)
            else:
                progress_indicator = SilentProgressIndicator(content_size, filename)
            with open(destination_loc, 'wb') as f:
                for data in response.iter_content(chunk_size=CHUNK_SIZE):
                    progress_indicator.progress(len(data))
                    f.write(data)
        progress_indicator.complete()

    @with_api_exceptions_handler
    def download_dataset_artifact(self, dataset_id, path, destination):
        """
        :param dataset_id:
        :param path:
        :param destination:
        :return:
        """
        dataset = self.get_dataset(dataset_id)
        dataset_type = dataset.data_type
        name = dataset.name
        self.download_dataset_artifact_(dataset_id, dataset_type, name, path, destination)

    @with_api_exceptions_handler
    def download_dataset_artifact_(self, dataset_id, type, name, path, destination):
        """
        :param type
        :param dataset_id:
        :param path: 当数据集类型为 DataSource.WTHINGS 时 path传参为 None
        :param destination:
        :return:
        """
        if not destination:
            destination = os.getcwd()

        if not os.path.exists(destination):
            os.makedirs(destination)
        elif not os.path.isdir(destination):
            raise NotADirectory(destination)

        try:
            if type == DataSource.WTHINGS.value:
                self._timeseries_download(dataset_id, name, destination)
            else:
                with Pool(5) as pool:
                    urls = []
                    artifacts = self._list_dataset_artifacts(dataset_id)
                    if '.' not in path:
                        resultinfo, dir = self._list_dir_artifacts(dataset_id, path, [], [])
                        for i in dir:
                            if not os.path.exists(destination + i):
                                os.makedirs(destination + i)
                        for asset in artifacts:
                            for res in resultinfo:
                                if asset.name in res:
                                    if '/' in res:
                                        res_des = res.rsplit('/', 1)
                                        res_des = res_des[0]
                                    else:
                                        res_des = ''
                                    urls.append((asset.path, destination + res_des, asset.name))
                    else:
                        for asset in artifacts:
                            if path in asset.path:
                                urls.append((asset.path, destination, asset.name))
                    pool.map(self._url_download, urls)
                    pool.close()
                    pool.join()
        except Exception as e:
            raise e

    @with_api_exceptions_handler
    def download_dataset_artifacts(self, data_id, destination, unzip, feature_type=None):
        """
        :param data_id:
        :param destination:
        :param unzip:
        :param feature_type:
        :return:
        """
        dataset = self.get_dataset(data_id)

        if dataset is not None:
            dataset_type = dataset.data_type
            name = dataset.name
            self.download_dataset_artifacts_(data_id, dataset_type, name, destination)
        else:
            feature = self.get_feature(data_id)
            self._download_feature_zip(data_id, destination, unzip, feature_type)
            if feature is None:
                raise Exception('需下载的数据集/特征库ID未找到，请检查后重新尝试')

    @with_api_exceptions_handler
    def download_dataset_artifacts_(self, dataset_id, type, name, destination):
        """
        :param type 数据集类型
        :param dataset_id:
        :param destination:
        :return:
        """

        if not destination:
            destination = os.getcwd()
        if not destination.endswith("/"):
            destination = destination + "/"
        if not os.path.exists(destination):
            os.makedirs(destination)
        elif not os.path.isdir(destination):
            raise NotADirectory(destination)

        try:
            if type == DataSource.WTHINGS.value:
                self._timeseries_download(dataset_id, name, destination)
            else:
                with Pool(5) as pool:
                    artifacts = self._list_dataset_artifacts(dataset_id)
                    resultinfo, dir = self._list_dir_artifacts(dataset_id=dataset_id, path=None, result=[], dir=[])
                    urls = []
                    for d in dir:
                        if not os.path.exists(destination + d):
                            os.makedirs(destination + d)
                    for asset in artifacts:
                        for res in resultinfo:
                            if res in asset.path:
                                if '/' in res:
                                    res_des = res.rsplit('/', 1)
                                    res_des = res_des[0]
                                else:
                                    res_des = ''
                                urls.append((asset.path, destination + res_des, asset.name))
                    pool.map(self._url_download, list(set(urls)))
                    pool.close()
                    pool.join()
        except Exception as e:
            raise e

    @with_api_exceptions_handler
    def _check_ip(self, ipAddr):
        import re
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(ipAddr):
            return True
        else:
            return False

    @with_api_exceptions_handler
    def _get_ip(self):
        from urllib.parse import urlparse
        hostname = urlparse(self.api_address).hostname
        if self._check_ip(hostname):
            import ipaddress
            if ipaddress.ip_address(hostname).is_private:
                return hostname
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @with_api_exceptions_handler
    @require_app
    def _list_dir_artifacts(self, dataset_id, path, result, dir):
        """
        递归获取所有的文件，文件夹
        :param dataset_id:
        :path 文件路径
        :return: 返回文件，图片数据集文件，文件夹列表
        """
        res = self._session.get(url=f'{self.api_address}/{self.app_id}/data/dataset/dir/{dataset_id}?path={path}')
        if not path:
            res = self._session.get(url=f'{self.api_address}/{self.app_id}/data/dataset/dir/{dataset_id}')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        for d in res.json()['data']:
            if d['isDir'] is True:
                dir.append(d['path'])
                self._list_dir_artifacts(dataset_id, d['path'], result, dir)
            else:
                if '/' in d['path'] and '.' in d['path']:
                    dir_path = d['path'].split('/')
                    dir_path.remove(dir_path[-1])
                    dp = ''
                    for p in dir_path:
                        dp = dp + '/' + p
                    dir.append(dp)
                result.append(d['path'])
        return list(set(result)), list(set(dir))

    @with_api_exceptions_handler
    @require_app
    def _list_dataset_artifacts(self, dataset_id):
        """
        :param dataset_id:
        :return: 返回文件，图片数据集文件列表
        """
        res = self._session.get(url=f'{self.api_address}/{self.app_id}/data/dataset/{dataset_id}/asset?page=-1')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        artifacts = []
        for art in res.json()['data']['data']:
            artifacts.append(
                Asset(art['id'], art['name'], art['path'], art['content_type'], art['size'], art['type'], dataset_id))
        return artifacts

    @with_api_exceptions_handler
    @require_app
    def _timeseries_download(self, dataset_id, name, destination):
        """
        时序数据整体下载
        :param dataset_id:
        :param destination
        :return true or false
        """
        res = self._session.get(
            url=f'{self.api_address}/{self.app_id}/data/dataset/filedownload/device/{dataset_id}/all')
        try:
            destination_loc = os.path.join(destination, f'{name}.csv')
            content_size = len(res.content)
            progress_indicator = SilentProgressIndicator(content_size, f'{name}.csv')
            if content_size >= WARN_SIZE:
                progress_indicator = LoggingProgressIndicator(content_size, f'{name}.csv')
            with open(destination_loc, 'wb') as f:
                for data in res.iter_content(chunk_size=CHUNK_SIZE):
                    progress_indicator.progress(len(data))
                    f.write(data)
            progress_indicator.complete()
        except Exception as e:
            return e

    @with_api_exceptions_handler
    @require_app
    def create_model(self, name, desc, git_url, http_url, visibility, source):
        """
        当前应用下创建模型
        :param visibility: 公有私有 public private 默认 private
        :param name:模型名称
        :param desc:模型备注
        :param auth_id: auth_id 默认空
        :param git_url: git地址 默认空
        :param http_url: http地址 默认空
        :param source:模型来源 flow:画布 gitcode:git代码
        :return: List of Class `Model` Object
        """
        res = self._session.post(url=f'{self.api_address}/{self.app_id}/training/model/', json={"name": name,
                                                                                                "app_id": self.app_id,
                                                                                                "desc": desc,
                                                                                                "git_url": git_url,
                                                                                                "http_url": http_url,
                                                                                                "visibility": visibility,
                                                                                                "source": source})
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        self.set_model(data['id'])
        return Model(self, data['id'], data['name'], data['desc'], data['app_id'],
                     data['create_time'], data['create_user_id'], data['update_time'],
                     data['update_user_id'], data['source'])

    @with_api_exceptions_handler
    @require_app
    @require_model
    def get_model(self):
        """
        获取模型信息
        :return: Model instance
        """
        res = self._session.get(url=f'{self.api_address}/{self.app_id}/training/model/{self.model_id}/')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        dict = res.json()['data']
        return Model(self, dict['id'], dict['name'], dict['desc'], dict['app_id'],
                     dict['create_time'], dict['create_user_id'], dict['update_time'],
                     dict['update_user_id'], dict['source'])

    @with_api_exceptions_handler
    @require_app
    @require_model
    def update_model(self, name, visibility, desc):
        """
        更新模型信息
        :param name:
        :param desc:
        :return:
        """
        res = self._session.put(url=f'{self.api_address}/{self.app_id}/training/model/{self.model_id}',
                                json={"app_id": self.app_id, "name": name, "desc": desc, "visibility": visibility})
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return Model(self, data['id'], data['name'], data['desc'], data['app_id'],
                     data['create_time'], data['create_user_id'], data['update_time'],
                     data['update_user_id'], data['source'])

    @with_api_exceptions_handler
    @require_app
    @require_model
    def delete_model(self):
        """
        删除模型
        :return:
        """
        res = self._session.delete(url=f'{self.api_address}/{self.app_id}/training/model/{self.model_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    @require_model
    def get_model_version(self, version):
        """
        根据模型id，模型版本查询
        :param version:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/model-repo/ver/{version}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return ModelVersion(self, data['id'], data['version'], data['desc'], data['model_id'], data['model_name'],
                            data['mode'], data['create_user_name'], data['create_time'], data['create_user_id'])

    @with_api_exceptions_handler
    @require_model
    def list_model_versions(self, page, pagesize):
        """
        根据模型id，模型版本查询
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/model-repo/?page={page}&pagesize={pagesize}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        dict = res.json()['data']['data']
        datas = []
        for d in dict:
            datas.append(ModelVersion(self, d['id'], d['version'], d['desc'], d['model_id'], d['model_name'],
                                      d['mode'], d['create_user_name'], d['create_time'], d['create_user_id']))
        return datas

    @with_api_exceptions_handler
    @require_model
    def abandon_model_version(self, version):
        """
        根据模型id，删除模型版本
        :param version:
        :return:
        """
        res = self._session.delete(url=f'{self.api_address}/{self.model_id}/training/model-repo/ver/{version}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    @require_model
    def update_model_version(self, version, desc):
        """
        根据模型id，修改模型版本
        :param desc:
        :param version:
        :return:
        """
        res = self._session.put(url=f'{self.api_address}/{self.model_id}/training/model-repo/ver/{version}',
                                json={"desc": desc})
        if res.json()['message']:
            raise Exception(res.json()['message'])
        dict = res.json()['data']
        return ModelVersion(self, dict['id'], dict['version'], dict['desc'], dict['model_id'], dict['model_name'],
                            dict['mode'], dict['create_user_name'], dict['create_time'], dict['create_user_id'])

    @with_api_exceptions_handler
    @require_model
    def list_experiments(self):
        """
        根据模型id，获取实验数据
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/experiment/getexperiment')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    def download_model_artifact(self, model_id, path, destination):
        pass

    @with_api_exceptions_handler
    def download_model_artifacts(self, model_id, destination):
        pass

    @with_api_exceptions_handler
    @require_model
    def list_model_releases(self, version=None):
        """
        根据模型id，版本，获取发布数据
        :param version:
        :return:
        """
        if version is None:
            res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/model-release/getrelease')
        else:
            res = self._session.get(
                url=f'{self.api_address}/{self.model_id}/training/model-release/getrelease?version={version}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    @require_model
    def list_model_releases_by_repo(self, repo_id):
        """
        查询当前模型版本的发布服务列表
        :param repo_id:
        :return:
        """
        res = self._session.get(
            url=f'{self.api_address}/{self.model_id}/training/model-release/getrelease_byrepo/{repo_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return data

    @with_api_exceptions_handler
    @require_model
    def register_model_version(self, desc, artifacts, mode, json_data=None):
        """
        注册自定义模型
        :param desc:  模型版本说明
        :param artifacts:  上传文件路径
        :param mode:  模型模式
        :param json_data: 模型版本其他信息
        :return:
        """
        if mode == ModelRegisterMode.DOCKER.value:
            _logger.warning("暂不支持此功能，功能即将上线，敬请期待。")
            pass
        if mode == ModelRegisterMode.PYFUNC.value:
            res = self._session.post(
                url=f'{self.api_address}/{self.model_id}/deploy/model/',
                json={'desc': desc, 'mode': mode, 'json_data': json_data},
            )
            if res.json()["message"]:
                raise Exception(res.json()["message"])
            model_repo_id = res.json()['data']['task_id']
            entries = scan_upload_entries({UploadEntry(artifacts, "")})
            upload_to_storage(entries, self._model_upload, self._model_chunk_upload_loop,
                              warn_limit=CHUNK_SIZE * 1024 * 50, oid=model_repo_id)

            res = self._session.get(
                url=f'{self.api_address}/{self.model_id}/deploy/model/{model_repo_id}'
            )
            dict = res.json()['data']
            return ModelVersion(self, dict['id'], dict['version'], dict['desc'], dict['model_id'], dict['model_name'],
                                dict['mode'], dict['create_user_name'], dict['create_time'], dict['create_user_id'])

    @with_api_exceptions_handler
    @require_model
    def download_model_version_asset(self, repo_id, path, destination=''):
        if not destination:
            destination = os.getcwd()

        if not os.path.exists(destination):
            os.makedirs(destination)
        elif not os.path.isdir(destination):
            raise NotADirectory(destination)

        try:
            urls = []
            minio_path = self.api_address.rsplit('/', 1)
            minio_path = minio_path[0] + '/resource'
            s3path = self._get_repo_s3path(repo_id)
            if s3path is None:
                return 's3path不存在'
            with Pool(5) as pool:
                if '.' not in path:
                    resultinfo, dir = self._list_dir_model_artifacts(repo_id, path, [], [])
                    for i in dir:
                        if i[0] != '/':
                            continue
                        if not os.path.exists(destination + i):
                            os.makedirs(destination + i)
                    for result in resultinfo:
                        result_path = result.rsplit('/', 1)
                        des_path = result_path[0]
                        result_path = result_path[-1]
                        file_path = minio_path + s3path + '/' + result_path
                        urls.append((file_path, destination + '/' + des_path, result_path))
                else:
                    if '/' in path:
                        path = path.rsplit('/', 1)
                        des_path = path[0]
                        path = path[-1]
                        file_path = minio_path + s3path + path
                        urls.append((file_path, destination + '/' + des_path, path))
                    else:
                        file_path = path + s3path + path
                        urls.append((file_path, destination, path))
                pool.map(self._url_download, urls)
                pool.close()
                pool.join()
        except Exception as e:
            raise e

    @with_api_exceptions_handler
    def download_model_version_artifacts(self, repo_id, destination=''):
        if not destination:
            destination = os.getcwd()

        if not os.path.exists(destination):
            os.makedirs(destination)
        elif not os.path.isdir(destination):
            raise NotADirectory(destination)

        try:
            urls = []
            minio_path = self.api_address.rsplit('/', 1)
            minio_path = minio_path[0] + '/resource'
            s3path = self._get_repo_s3path(repo_id)
            if s3path is None:
                return '当前模型库下无文件，请检查模型库ID或模型库文件是否已经存在'
            s3path = s3path.split("/")
            s3path.pop()
            s3path.pop(0)
            model_path = "/".join(s3path)
            with Pool(5) as pool:
                resultinfo, dir = self._list_dir_model_artifacts(repo_id, None, [], [])
                for i in dir:
                    if i[0] != '/':
                        continue
                    if not os.path.exists(destination + i):
                        os.makedirs(destination + i)
                for result in resultinfo:
                    result_path = result.rsplit('/', 1)
                    des_path = result_path[0]
                    result_path = result_path[-1]
                    file_path = minio_path + model_path + '/' + des_path + "/" + result_path
                    urls.append((file_path, destination + '/' + des_path, result_path))
                pool.map(self._url_download, urls)
                pool.close()
                pool.join()
        except Exception as e:
            raise e

    @with_api_exceptions_handler
    def _list_dir_model_artifacts(self, repo_id, path, result, dir):
        """
        递归获取所有的文件，文件夹
        :param repo_id:
        :path 文件路径
        :return: 返回文件，图片数据集文件，文件夹列表
        """
        res = self._session.get(url=f'{self.api_address}/training/run/{repo_id}/artifacts/list?path={path}')
        if not path:
            res = self._session.get(url=f'{self.api_address}/training/run/{repo_id}/artifacts/list')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        for d in res.json()['data']:
            if d['isDir'] is True:
                dir.append(d['path'])
                self._list_dir_model_artifacts(repo_id, d['path'], result, dir)
            else:
                if '/' in d['path']:
                    dir_path = d['path'].split('/')
                    dir_path.remove(dir_path[-1])
                    dp = ''
                    for p in dir_path:
                        dp = dp + '/' + p
                    dir.append(dp)
                result.append(d['path'])
        return list(set(result)), list(set(dir))

    @with_api_exceptions_handler
    @require_model
    def _get_repo_s3path(self, repo_id):
        res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/model-repo/{repo_id}/')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        data = res.json()['data']
        s3path = ''
        if data['json_data'] is not None:
            s3path = data['json_data']['model_uri']
        return s3path

    @with_api_exceptions_handler
    @require_model
    def get_repo_by_repo_id(self, repo_id):
        res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/model-repo/{repo_id}/')
        if res.json()["message"]:
            raise Exception(res.json()["message"])
        data = res.json()['data']
        return ModelVersion(self, data['id'], data['version'], data['desc'], data['model_id'], data['model_name'],
                            data['create_user_name'], data['create_time'], data['create_user_id'], data['mode'])

    @with_api_exceptions_handler
    @require_app
    def _get_feature_zip_path(self, feature_id, feature_type):
        if feature_type is None:
            feature_type = FeatureType.FILE.value
        for i in range(100):
            res = self._session.get(
                url=f'{self.api_address}/{self.app_id}/data/feature/{feature_id}/asset?type={feature_type}')
            if res.json()["message"]:
                raise Exception(res.json()["message"])
            data = res.json()['data']
            if data is '':
                time.sleep(6)
                continue
            if data['path'] is not None:
                return data['path']
        raise Exception('转换超时，请联系管理员处理。')

    @with_api_exceptions_handler
    def _download_feature_zip(self, feature_id, destination, unzip, feature_type):
        """
        :param feature_id:特征id
        :param destination:本地存储路径
        :param unzip: 是否解压
        :param feature_type:特征库类型,参考constants.FeatureType
        :return:
        """
        if not destination:
            destination = os.getcwd()

        if not os.path.exists(destination):
            os.makedirs(destination)
        elif not os.path.isdir(destination):
            raise NotADirectory(destination)
        feature_path = self._get_feature_zip_path(feature_id, feature_type)
        if feature_path is None:
            return '该特征下无可下载资源'
        try:
            file_name = feature_path.rsplit('/', 1)
            file_name = file_name[-1]
            self._url_download((feature_path, destination, file_name))
            zip_path = destination + '/' + file_name
            if unzip is True:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(destination)
                os.remove(zip_path)
        except Exception as e:
            raise e

    @with_api_exceptions_handler
    @require_model
    def get_experiment(self, experiment_id):
        """
        获取实验对象
        :param experiment_id:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/{self.model_id}/training/experiment/{experiment_id}/')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        self.app_id = data['model']['app_id']
        self.model_id = data['model_id']
        return Experiment(self, id=data['id'], name=data['name'], desc=data['desc'], param_json=data['param_json'],
                          host_id=data['host_id'], model_id=data['model_id'], dataset_id=data['dataset_id'],
                          state=data['state'], best_run_id=data['best_run_id'], create_time=data['create_time'],
                          create_user_id=data['create_user_id'], mlflow_experiments_id=data['mlflow_experiments_id'],
                          ml_experiment=data['ml_experiment'])

    @with_api_exceptions_handler
    def get_mlflow_experiment(self, experiment_id):
        """
        获取mlflow实验对象
        :param experiment_id:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/training/mlflow/experiment/{experiment_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return MLFlowExperiment(self, data['experiment_id'], data['name'], data['artifact_location'],
                                data['lifecycle_stage'])

    @with_api_exceptions_handler
    @require_app
    @require_model
    def get_mlproject_file(self, model_id):
        """
        根据模型id获取mlproject的内容
        :param model_id:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/{self.app_id}/training/model/{self.model_id}/file')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return data

    @with_api_exceptions_handler
    @require_model
    def create_experiment(self, name, params=None, host_id=None, dataset_id=None, docker_args=None,
                          feature_id=None, is_train=None, desc=None, mlexp_id=None, artifact_location=None,
                          online_train=False):
        """
        创建实验
        :param name:
        :param params:
        :param host_id:
        :param dataset_id:
        :param docker_args:
        :param feature_id:
        :param is_train:
        :param desc:
        :param mlexp_id:
        :param online_train:
        :param artifact_location:
        :return:
        """

        def _get_type(ins):
            if isinstance(ins, int):
                return 'int'
            if isinstance(ins, float):
                return 'float'
            if isinstance(ins, str):
                return 'str'
            if isinstance(ins, list):
                return 'list'
            if isinstance(ins, dict):
                return 'dict'
            return None

        param_json = []
        if params is not None:
            for k, v in params.items():
                _d = {'label': k, 'prop': k, 'default': v}
                if v:
                    _d.update({'type': _get_type(v)})
                param_json.append(_d)

        data = dict(name=name, model_id=self.model_id,
                    param_json=param_json,
                    host_id=host_id,
                    dataset_id=dataset_id,
                    docker_args=docker_args,
                    feature_id=feature_id,
                    is_train=is_train,
                    desc=desc,
                    # mlexp_id=mlexp_id,
                    artifact_location=artifact_location,
                    online_train=False
                    )
        res = self._session.post(url=f'{self.api_address}/{self.model_id}/training/experiment/', json=data)
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        return Experiment(self, id=data['id'], name=data['name'], desc=data['desc'], host_id=data['host_id'],
                          param_json=data['param_json'], model_id=data['model_id'], dataset_id=data['dataset_id'],
                          state=data['state'], best_run_id=data['best_run_id'], create_time=data['create_time'],
                          create_user_id=data['create_user_id'], mlflow_experiments_id=data['mlflow_experiments_id'],
                          ml_experiment=data['ml_experiment'])

    @with_api_exceptions_handler
    def create_mlflow_experiment(self, name, artifact_location):
        """
        创建mlflow实验
        :param name:
        :param artifact_location:
        :return:
        """
        data = dict(name=name, artifact_location=artifact_location)
        res = self._session.post(url=f'{self.api_address}/training/run/ml-experiment/', json=data)
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return data['mlflow_experiment_id']

    @with_api_exceptions_handler
    @require_model
    def get_experiment_by_mlflow_experiment(self, experiment_id):
        """
        根据mlflow 查询wai experiment
        :param experiment_id:
        :return:
        """
        res = self._session.get(f'{self.api_address}/{self.model_id}/training/experiment/mlflow/{experiment_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        self.set_model(data['model_id'])
        self.set_app(data['model']['app_id'])
        return Experiment(self, id=data['id'], name=data['name'], desc=data['desc'], host_id=data['host_id'],
                          param_json=data['param_json'], model_id=data['model_id'], dataset_id=data['dataset_id'],
                          state=data['state'], best_run_id=data['best_run_id'], create_time=data['create_time'],
                          create_user_id=data['create_user_id'], mlflow_experiments_id=data['mlflow_experiments_id'],
                          ml_experiment=data['ml_experiment'])

    @with_api_exceptions_handler
    @require_model
    def get_experiment_by_mlflow_run(self, run_id):
        """
        根据mlflow run_id 查询 wai experiment
        :param run_id:
        :return:
        """
        res = self._session.get(f'{self.api_address}/{self.model_id}/training/experiment/mlflow/run/{run_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        self.set_model(data['model_id'])
        self.set_app(data['model']['app_id'])
        return Experiment(self, id=data['id'], name=data['name'], desc=data['desc'], host_id=data['host_id'],
                          param_json=data['param_json'],
                          model_id=data['model_id'], dataset_id=data['dataset_id'], state=data['state'],
                          best_run_id=data['best_run_id'], create_time=data['create_time'],
                          create_user_id=data['create_user_id'], mlflow_experiments_id=data['mlflow_experiments_id'],
                          ml_experiment=data['ml_experiment'])

    @with_api_exceptions_handler
    def create_mlflow_run(self, name, artifact_uri, run_uuid, experiment_id, source_type,
                          source_name, entry_point_name, user_id, status, start_time, end_time,
                          source_version, lifecycle_stage):
        """
        创建mlflow run
        :param name:
        :param artifact_uri:
        :param run_uuid:
        :param experiment_id:
        :param source_type:
        :param source_name:
        :param entry_point_name:
        :param user_id:
        :param status:
        :param start_time:
        :param end_time:
        :param source_version:
        :param lifecycle_stage:
        :return:
        """
        data = dict(name=name, artifact_uri=artifact_uri, run_uuid=run_uuid, experiment_id=experiment_id,
                    source_type=source_type, source_name=source_name, entry_point_name=entry_point_name,
                    user_id=user_id, status=status, start_time=start_time, end_time=end_time,
                    source_version=source_version, lifecycle_stage=lifecycle_stage)
        res = self._session.post(url=f'{self.api_address}/training/run/', json=data)

        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return MLFlowRun(self, **data)

    @with_api_exceptions_handler
    def get_mlflow_run(self, run_id):
        """
        查询mlflow run
        :param run_id:
        :return:
        """
        res = self._session.get(f'{self.api_address}/training/mlflow/run/{run_id}')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']
        info = data['run_info']
        metrics, params, tags = data['run_data']['metrics'], data['run_data']['params'], data['run_data']['tags']

        return MLFlowRun(self, name='',
                         artifact_uri=info['artifact_uri'],
                         run_uuid=info['run_uuid'],
                         experiment_id=info['experiment_id'],
                         source_type=tags.get('mlflow.source.type'),
                         source_name=tags.get('mlflow.source.name'),
                         entry_point_name=tags.get('mlflow.project.entryPoint'),
                         user_id=tags['mlflow.user'],
                         status=info['status'],
                         start_time=info['start_time'],
                         end_time=info['end_time'],
                         source_version='',
                         lifecycle_stage=info['lifecycle_stage']
                         )

    @with_api_exceptions_handler
    def log_params(self, run_id, params):
        """
        log param
        :param run_id:
        :param params:
        :return:
        """
        data = []
        for param in params:
            data.append({'key': param.key, 'value': param.value})
        res = self._session.post(f'{self.api_address}/training/mlflow/run/{run_id}/log_params', json={'data': data})
        if res.json()['message']:
            raise Exception(res.json()['message'])

    @with_api_exceptions_handler
    def log_metrics(self, run_id, metrics):
        """
        log metric
        :param run_id:
        :param metrics: List[Dict[metric]]
        :return:
        """
        res = self._session.post(f'{self.api_address}/training/mlflow/run/{run_id}/log_metrics', json={'data': metrics})
        if res.json()['message']:
            raise Exception(res.json()['message'])

    @with_api_exceptions_handler
    def set_tags(self, run_id, tags):
        """
        log tag
        :param run_id:
        :param tags:
        :return:
        """
        data = []
        for tag in tags:
            data.append({'key': tag.key, 'value': tag.value})
        res = self._session.post(f'{self.api_address}/training/mlflow/run/{run_id}/set_tags', json={'data': data})
        if res.json()['message']:
            raise Exception(res.json()['message'])

    @with_api_exceptions_handler
    def update_run_info(self, run_id, run_status, end_time):
        """
        更新run
        :param run_id:
        :param run_status:
        :param end_time:
        :return:
        """
        data = {
            'run_status': run_status,
            'end_time': end_time
        }
        res = self._session.post(f'{self.api_address}/training/mlflow/run/{run_id}', json=data)
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return MLFlowRun(self, **data)

    @with_api_exceptions_handler
    def _upload_artifact(self, entry: UploadEntry, oid):
        run_id = oid
        fs = FileStream(entry)
        progress_indicator = SilentProgressIndicator(fs.length, fs.filename)
        payload = {"path": entry.prefix, "run_id": run_id}
        res = self._session.post(url=f'{self.api_address}/training/mlflow/upload/artifact', files=[('file', (
            fs.filename, fs.fobj, fs.content_type))], data=payload)
        if res.json()["message"]:
            _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            raise FileUploadException(fs.filename)
        else:
            progress_indicator.complete()
        fs.close()

    @with_api_exceptions_handler
    def _upload_chunk_artifact_loop(self, entry: UploadEntry, oid):
        run_id = oid
        stream = FileChunkStream(entry)
        progress_indicator = LoggingProgressIndicator(stream.length, stream.filename)
        for ind, fc in enumerate(stream.generate(chunk_size=CHUNK_SIZE * 1024 * 20)):
            self._upload_chunk_artifact(fc, entry.filename, str(ind), entry.prefix, progress_indicator, run_id)

        res = self._session.get(url=f'{self.api_address}/training/mlflow/upload/artifact/success',
                                params={'filename': entry.filename, 'run_id': run_id, 'path': entry.prefix})
        if res.json()["message"]:
            _logger.error(f"file {entry.source_path} upload failed,{res.json()['message']}")
            raise FileUploadException(entry.filename)
        else:
            progress_indicator.complete()
        stream.close()

    @with_api_exceptions_handler
    def _upload_chunk_artifact(self, file: FileChunk, filename, chunk, path, progress_indicator, oid):
        model_repo_id = oid
        payload = {"chunk": chunk, "path": path, "run_id": model_repo_id}
        res = self._session.post(url=f'{self.api_address}/training/mlflow/upload/artifact',
                                 files=[('file', (file.data))],
                                 data=payload
                                 )
        if res.json()["message"]:
            _logger.error(f"file {filename} upload failed,{res.json()['message']}")
            # raise FileUploadException(filename + '_' + chunk)
        else:
            progress_indicator.progress(file.end - file.start)

    @with_api_exceptions_handler
    def upload_artifact(self, local_file, artifact_path, run_id):
        """
        模型文件上传接口
        :param local_file:
        :param artifact_path:
        :param run_id:
        :return:
        """
        entries = scan_upload_entries({UploadEntry(local_file, artifact_path)})
        upload_to_storage(entries, self._upload_artifact, self._upload_chunk_artifact_loop,
                          warn_limit=CHUNK_SIZE * 1024 * 50, oid=run_id)

    # @with_api_exceptions_handler
    # def record_logged_model(self, key, value, run_id):
    #     """
    #     记录模型保存记录
    #     :param key:
    #     :param value:
    #     :param run_id:
    #     :return:
    #     """
    #     data = {
    #         'key': key,
    #         'value': value
    #     }
    #     res = self._session.post(f'{self.api_address}/training/mlflow/run/{run_id}', json=data)
    #     if res.json()['message']:
    #         raise Exception(res.json()['message'])

    @with_api_exceptions_handler
    def get_latest_metrics(self, run_id):
        """
        获取mlflow的运行标量
        :param run_id:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/training/mlflow/run/{run_id}/latest_metric/')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return [MLflowLatestMetric(**d) for d in data]

    @with_api_exceptions_handler
    def get_params(self, run_id):
        """
        获取mlflow的运行参数
        :param run_id:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/training/mlflow/run/{run_id}/param/')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return [MLFlowParam(**d) for d in data]

    @with_api_exceptions_handler
    def get_tags(self, run_id):
        """
        获取mlflow的运行的标签
        :param run_id:
        :return:
        """
        res = self._session.get(url=f'{self.api_address}/training/mlflow/run/{run_id}/tag/')
        if res.json()['message']:
            raise Exception(res.json()['message'])
        data = res.json()['data']

        return [MLFlowTag(**d) for d in data]

    @with_api_exceptions_handler
    @require_app
    def get_feature(self, feature_id):
        res = self._session.get(url=f'{self.api_address}/{self.app_id}/data/feature/{feature_id}/')
        if res.json()["message"]:
            return None
        dict = res.json()['data']['data']
        return Feature(self, dict['id'], dict['name'], dict['desc'], dict['zone'], dict['type'], dict['json_data'],
                       dict['create_time'], dict['create_user_id'], dict['update_time'], dict['update_user_id'])

    @with_api_exceptions_handler
    @require_app
    def download_data(self, dataset_id, path, destination_dir, datasource, fileext, query):
        """
        获取外部数据源数据
        :param dataset_id
        :param path
        :param destination_dir
        :param datasource
        :param fileext
        :param query
        """
        filename = path
        if not destination_dir:
            destination_dir = os.getcwd()
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        elif not os.path.isdir(destination_dir):
            raise NotADirectory(destination_dir)
        try:
            if DataSource.MAMMUT.value == datasource or DataSource.WTHINGS.value == datasource:
                res = self._session.post(
                    url=f'{self.api_address}/{self.app_id}/data/dataset/netease/data/sdk/{dataset_id}',
                    json={"query": query, "datasource": datasource})
                if res.json()["message"]:
                    return res.json()["message"]
                path = res.json()['data']
                urls = [(path, destination_dir, path)]
                self._url_download((path, destination_dir, filename))
                res = self._session.get(
                    url=f'{self.api_address}/{self.app_id}/data/dataset/netease/data/sdk/{dataset_id}')
                if res.json()["message"]:
                    return res.json()["message"]
            else:
                _logger.error("您提供DataSource类型暂不支持")
                pass
        except Exception as e:
            raise e
