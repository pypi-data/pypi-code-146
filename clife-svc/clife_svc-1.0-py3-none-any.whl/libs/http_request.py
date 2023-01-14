#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/8/21'

"""
import os
import time
import random
import string
import asyncio

import boto3
import aiohttp
from aiohttp.client_exceptions import ServerTimeoutError
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from clife_svc.errors.error_code import ParameterException, UploadFileException, TimeoutException
from clife_svc.libs.log import klogger, clogger


class ClientRequest:
    _S3_CLIENT = ''
    HTTP_TIMEOUT = None
    COS_REGION = None
    COS_SECRET_ID = None
    COS_SECRET_KEY = None
    COS_BUCKET = None
    # COS_DIR = None
    COS_BUCKET_HOST = None
    # 请求超时时间
    __http_sess_timeout = None

    def __init__(self, app):
        self.HTTP_TIMEOUT = int(app.get_conf('http.timeout', 5))
        self.__http_sess_timeout = aiohttp.ClientTimeout(total=self.HTTP_TIMEOUT)

        self.S3_TYPE = None

        self.S3_ACCESS_KEY = app.get_conf('s3.access.key', '')
        self.S3_SECRET_KEY = app.get_conf('s3.secret.key', '')
        self.S3_BUCKET = app.get_conf('s3.bucket', '')
        self.S3_BUCKET_PRIVATE = int(app.get_conf('s3.bucket.private', '0'))
        self.S3_ENDPOINT_URL = app.get_conf('s3.endpoint.url', '')
        if not all([self.S3_ACCESS_KEY, self.S3_SECRET_KEY, self.S3_BUCKET, self.S3_ENDPOINT_URL]):
            clogger.warning('S3 Client missing required parameters, trying COS Client.')
            self.COS_REGION = app.get_conf('cos.region', '')
            self.COS_SECRET_ID = app.get_conf('cos.secret.id', '')
            self.COS_SECRET_KEY = app.get_conf('cos.secret.key', '')
            self.COS_BUCKET = app.get_conf('cos.bucket', '')
            self.COS_BUCKET_HOST = app.get_conf('cos.bucket.host', 'cos.clife.net')
            if not all([self.COS_REGION, self.COS_SECRET_ID, self.COS_SECRET_KEY, self.COS_BUCKET]):
                clogger.warning('COS Client missing required parameters, upload file may disabled.')
            else:
                self.S3_TYPE = 'COS'
                clogger.info('COS Client parameters check success')
        else:
            self.S3_TYPE = 'S3'
            clogger.info('S3 Client parameters check success')

        if self.S3_TYPE:
            clogger.info(f'Object Storage System: {self.S3_TYPE}')

    def create_txy_client(self):
        """
        腾讯云上传client对象
        """
        try:
            if not self.S3_TYPE:
                raise Exception
            elif self.S3_TYPE == 'COS':
                config = CosConfig(Region=self.COS_REGION, Secret_id=self.COS_SECRET_ID,
                                   Secret_key=self.COS_SECRET_KEY,
                                   Token=None)
                client = CosS3Client(config)
            else:
                client = boto3.client('s3',
                                      aws_access_key_id=self.S3_ACCESS_KEY,
                                      aws_secret_access_key=self.S3_SECRET_KEY,
                                      endpoint_url=self.S3_ENDPOINT_URL)
            return client
        except Exception:
            raise UploadFileException(data='create cos client error')

    @staticmethod
    async def _request_get(session, url, params, resp_type):
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                if resp_type == 'json':
                    return await resp.json()
                elif resp_type == 'text':
                    return await resp.text()
                else:
                    return await resp.read()
            else:
                klogger.error(
                    'Error of ClientRequest._request_get,resp.status:{},resp.text:{}'.format(resp.status,
                                                                                             await resp.text()))

    @staticmethod
    async def _request_post(session, url, data, json, resp_type):
        async with session.post(url, data=data, json=json) as resp:
            if resp.status == 200:
                if resp_type == 'json':
                    return await resp.json()
                elif resp_type == 'text':
                    return await resp.text()
                else:
                    return await resp.read()
            else:
                klogger.error(
                    'Error of ClientRequest._request_post,resp.status:{},resp.text:{}'.format(resp.status,
                                                                                              await resp.text()))

    async def _async_request(self, method, url, params=None, data=None, json=None, headers=None, cookies=None,
                             resp_type='json', timeout=None):
        """
        http请求
        :param method:
        :param url:
        :param params:
        :param data:
        :param headers:
        :param cookies:
        :param resp_type: json | text | byte
        :return:
        """
        if not timeout:
            timeout = self.__http_sess_timeout
        else:
            timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=timeout) as sess:
            if method == 'GET':
                return await self._request_get(sess, url, params, resp_type=resp_type)
            elif method == 'POST':
                return await self._request_post(sess, url, data, json, resp_type=resp_type)
            else:
                raise ParameterException(data='async_request method must in [GET,POST]')

    async def download_file(self, file_url, retry=2, timeout=None):
        """
        图片下载，仅支持公有读权限的文件资源下载
        :param file_url:
        :param retry:
        :param timeout:
        :return: 文件字节数组
        """
        while retry > 0:
            retry -= 1
            if 'http' in file_url:
                klogger.info('Start download file: {}'.format(file_url))
                start = time.time()
                try:
                    resp_byte = await self._async_request('GET', file_url, resp_type='byte', timeout=timeout)
                    if resp_byte:
                        klogger.info('Download file cost: {}s'.format(round(time.time() - start, 2)))
                        klogger.info('Success download file.')
                        return resp_byte
                except (ServerTimeoutError, asyncio.TimeoutError):
                    if retry > 0:
                        klogger.warning('Error download file,retry left: {}'.format(retry + 1))
                        continue
                    raise TimeoutException(data='download file timeout, url:{}'.format(file_url))
            else:
                # 本地文件路径格式直接返回
                klogger.info('File path: {}'.format(file_url))
                return ''

    @staticmethod
    def rename_file(file: str):
        """文件更名"""
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        salt += str(int(time.time()))
        return salt + os.path.splitext(file)[1]

    async def upload_file_from_buffer(self, cos_dir: str, file_extension: str, body, retry=2) -> str:
        """
        :param cos_dir: 上传的cos子路径
        :param file_extension: 文件扩展名，如.txt|.png
        :param body: 文件流,必须实现了read方法
        :param retry: 失败重试次数
        :return: 文件url
        """
        if not self._S3_CLIENT:
            self._S3_CLIENT = self.create_txy_client()
        start = time.time()
        file_name = self.rename_file(str(time.time()) + file_extension)

        while retry >= 0:
            retry -= 1
            try:
                if self.S3_TYPE == 'COS':
                    cloud_path = '/' + cos_dir + '/' + file_name
                    client_resp = self._S3_CLIENT.upload_file_from_buffer(
                        Bucket=self.COS_BUCKET,
                        Key=cloud_path,
                        Body=body,
                        PartSize=10,
                        MAXThread=10
                    )
                    if client_resp and isinstance(client_resp, dict):
                        etag = str(client_resp.get('ETag', ''))
                        if etag:
                            file_url = 'http://' + self.COS_BUCKET_HOST + cloud_path
                            klogger.info('Upload file cost: {}s'.format(round(time.time() - start, 2)))
                            klogger.info('Upload file success: {}'.format(file_url))
                            return file_url
                    else:
                        klogger.warning('Error upload file,retry left: {}'.format(retry + 1))
                        continue
                else:
                    key = cos_dir + '/' + file_name
                    self._S3_CLIENT.upload_fileobj(
                        Fileobj=body,
                        Bucket=self.S3_BUCKET,
                        Key=key)  # noqa

                    file_url = self._S3_CLIENT.generate_presigned_url('get_object',
                                                                      Params={'Bucket': self.S3_BUCKET,
                                                                              'Key': key},
                                                                      ExpiresIn=600)
                    file_url = file_url if self.S3_BUCKET_PRIVATE else file_url.split('?')[0]
                    klogger.info('Upload file cost: {}s'.format(round(time.time() - start, 2)))
                    klogger.info('Upload file success: {}'.format(file_url))
                    return file_url
            except Exception:
                klogger.warning('Error upload file,retry left: {}'.format(retry + 1))
                continue
        raise UploadFileException

    async def upload_file(self, cos_dir: str, file_path: str, retry=2) -> str:
        """
        上传文件至腾讯云cos
        :param cos_dir 上传的cos子路径
        :param file_path 待上传的本地文件路径
        :param retry 失败重试次数
        :return 文件url
        """
        if not self._S3_CLIENT:
            self._S3_CLIENT = self.create_txy_client()

        if not os.path.isfile(file_path):
            raise ParameterException(data='file not exist:'.format(file_path))

        file_name = os.path.split(file_path)[1]
        file_name = self.rename_file(file_name)

        while retry > 0:
            retry -= 1
            start = time.time()

            try:
                if self.S3_TYPE == 'COS':
                    cloud_path = '/' + cos_dir + '/' + file_name
                    client_resp = self._S3_CLIENT.upload_file(
                        Bucket=self.COS_BUCKET,
                        LocalFilePath=file_path,
                        Key=cloud_path,
                        PartSize=10,
                        MAXThread=10
                    )
                    if client_resp and isinstance(client_resp, dict):
                        etag = str(client_resp.get('ETag', ''))
                        if etag:
                            file_url = 'http://' + self.COS_BUCKET_HOST + cloud_path
                            klogger.info('Upload file cost: {}s'.format(round(time.time() - start, 2)))
                            klogger.info('Upload file success: {}'.format(file_url))
                            return file_url
                    else:
                        klogger.warning('Error upload file,retry left: {}'.format(retry + 1))
                        continue
                else:
                    key = cos_dir + '/' + file_name
                    self._S3_CLIENT.upload_file(
                        Filename=file_path,
                        Bucket=self.S3_BUCKET,
                        Key=key)  # noqa

                    file_url = self._S3_CLIENT.generate_presigned_url('get_object',
                                                                      Params={'Bucket': self.S3_BUCKET,
                                                                              'Key': key},
                                                                      ExpiresIn=600)
                    file_url = file_url if self.S3_BUCKET_PRIVATE else file_url.split('?')[0]
                    klogger.info('Upload file cost: {}s'.format(round(time.time() - start, 2)))
                    klogger.info('Upload file success: {}'.format(file_url))
                    return file_url
            except Exception:
                klogger.warning('Error upload file,retry left: {}'.format(retry + 1))
                continue
        raise UploadFileException

    async def call_back(self, url: str, body: dict, retry=2, timeout=None):
        while retry > 0:
            retry -= 1
            klogger.info('Start call back: UUID:{}, URL:{}, Body: {}'.format(body.get('uuid'), url, body))
            start = time.time()
            try:
                resp = await self._async_request('POST', url, json=body, timeout=timeout)
                if resp:
                    klogger.info('Call back cost: {}s'.format(round(time.time() - start, 2)))
                    klogger.info('Success call back.')
                    return resp
            except (ServerTimeoutError, asyncio.TimeoutError):
                if retry > 0:
                    klogger.warning('Error call back,retry left: {}'.format(retry + 1))
                    continue
                raise TimeoutException(data='call back timeout')
