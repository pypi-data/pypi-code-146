#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/11 16:02
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : exceptions.py
@Desc    : 
"""

import platform

from waveletai import envs

UNIX_STYLES = {'h1': '\033[95m',
               'h2': '\033[94m',
               'python': '\033[96m',
               'bash': '\033[95m',
               'warning': '\033[93m',
               'correct': '\033[92m',
               'fail': '\033[91m',
               'bold': '\033[1m',
               'underline': '\033[4m',
               'end': '\033[0m'}

WINDOWS_STYLES = {'h1': '',
                  'h2': '',
                  'python': '',
                  'bash': '',
                  'warning': '',
                  'correct': '',
                  'fail': '',
                  'bold': '',
                  'underline': '',
                  'end': ''}

EMPTY_STYLES = {'h1': '',
                'h2': '',
                'python': '',
                'bash': '',
                'warning': '',
                'correct': '',
                'fail': '',
                'bold': '',
                'underline': '',
                'end': ''}

if platform.system() in ['Linux', 'Darwin']:
    STYLES = UNIX_STYLES
elif platform.system() == 'Windows':
    STYLES = WINDOWS_STYLES
else:
    STYLES = EMPTY_STYLES


class WaveletAIException(Exception):
    pass


class InitFailed(WaveletAIException):
    def __init__(self):
        super(InitFailed, self).__init__('Initialization failed. Please set the environment variable of WAVELETAI_TOKEN'
                                         ' or invoke the waveletai.init() method on manual before use waveletai sdk')


class SSLError(WaveletAIException):
    def __init__(self):
        super(SSLError, self).__init__('SSL certificate validation failed. Set WaveletAI_ALLOW_SELF_SIGNED_CERTIFICATE '
                                       'environment variable to accept self-signed certificates.')


class RequiredAppError(WaveletAIException):
    def __init__(self):
        super(RequiredAppError, self).__init__(
            '您需要先设置当前所在的项目! 使用 waveletai.set_app(YOUR_APP_ID) 设置项目后重试.')


class RequiredModelError(WaveletAIException):
    def __init__(self):
        super(RequiredModelError, self).__init__(
            '您需要先设置当前所在的模型! 使用 waveletai.set_model(YOUR_APP_ID) 设置模型后重试.')


class ConnectionLost(WaveletAIException):
    def __init__(self):
        super(ConnectionLost, self).__init__('Connection lost. Please try again.')


class ServerError(WaveletAIException):
    def __init__(self):
        super(ServerError, self).__init__('Server error. Please try again later.')


class Unauthorized(WaveletAIException):
    def __init__(self):
        super(Unauthorized, self).__init__('Your API token is invalid.')


class Forbidden(WaveletAIException):
    def __init__(self):
        super(Forbidden, self).__init__('You have no permissions to access this resource.')


class InvalidApiKey(WaveletAIException):
    def __init__(self):
        super(InvalidApiKey, self).__init__('The provided API key is invalid.')


class StorageLimitReached(WaveletAIException):
    def __init__(self):
        super(StorageLimitReached, self).__init__('Storage limit reached.')


class FileNotFound(WaveletAIException):
    def __init__(self, path):
        super(FileNotFound, self).__init__("File {} doesn't exist.".format(path))


class NotAFile(WaveletAIException):
    def __init__(self, path):
        super(NotAFile, self).__init__("Path {} is not a file.".format(path))


class NotADirectory(WaveletAIException):
    def __init__(self, path):
        super(NotADirectory, self).__init__("Path {} is not a directory.".format(path))


class LoginFailed(WaveletAIException):
    def __init__(self, error):
        super(LoginFailed, self).__init__(f'Login Failed. error = {error}')


class LibraryNotInstalledException(WaveletAIException):
    def __init__(self, library):
        message = """
{h1}     
----WaveletAILibraryNotInstalledException---------------------------------------------------------------------------------
{end}
Looks like library {library} wasn't installed.

To install run:
    {bash}pip install {library}{end}

You may also want to check the following docs pages:
    - 

{correct}Need help?{end}-> https://ai.xiaobodata.com/getting-started/getting-help.html
"""
        inputs = dict(list({'library': library}.items()) + list(STYLES.items()))
        super(LibraryNotInstalledException, self).__init__(message.format(**inputs))


class FileUploadException(WaveletAIException):
    def __init__(self, filename):
        super(FileUploadException, self).__init__(f"资源文件 {filename} 已重试三次，均上传失败，请稍后重试")


class MissingApiTokenException(WaveletAIException):
    def __init__(self):
        message = """"""
        super(MissingApiTokenException, self).__init__(f'需要提供有效的api_token用于登录 WaveletAI 平台')


class DeprecatedApiToken(WaveletAIException):
    def __init__(self, app_url):
        super(DeprecatedApiToken, self).__init__(
            "您的api_token已经失效. 请访问 WaveletAI平台 获取最新的api_token.".format(app_url))


class CannotResolveHostname(WaveletAIException):
    def __init__(self, host):
        super(CannotResolveHostname, self).__init__(
            "Cannot resolve hostname {}. Please contact WaveletAI平台 support.".format(host))


class UnsupportedClientVersion(WaveletAIException):
    def __init__(self, version, minVersion, maxVersion):
        super(UnsupportedClientVersion, self).__init__(
            "This client version ({}) is not supported. Please install WaveletAI-client{}".format(
                version,
                "==" + str(maxVersion) if maxVersion else ">=" + str(minVersion)
            ))


class InvalidMLProjectFile(WaveletAIException):
    def __init__(self):
        super(InvalidMLProjectFile, self).__init__('the content of MLPorject is invalid')


class InvalidAPIToken(WaveletAIException):
    def __init__(self):
        super(InvalidAPIToken, self).__init__('非法的api_token')
