# coding:utf-8
import requests
import os
from tools_hjh.Tools import rm, mkdir
from urllib3 import disable_warnings
disable_warnings()


class HTTPRequest:
    """ 用户向网站提出请求的类 """
    
    def __init__(self, url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False):
        self.url = url.strip()
        self.headers = headers
        self.data = data
        self.proxies = proxies
        self.encoding = encoding
        self.timeout = timeout
        self.stream = stream
        self.allow_redirects = allow_redirects
        self.verify = verify
        self.response = None
        self.head = None

    def connect(self):
        """ 发出get或post请求, 返回状态码 """
        if self.data is None:
            self.response = requests.get(self.url, headers=self.headers, proxies=self.proxies, timeout=self.timeout, stream=self.stream, allow_redirects=self.allow_redirects, verify=self.verify)
        else:
            self.response = requests.post(self.url, headers=self.headers, data=self.data, proxies=self.proxies, timeout=self.timeout, stream=self.stream, allow_redirects=self.allow_redirects, verify=self.verify)
        self.response.encoding = self.encoding
        
        return self.get_status_code()

    def get_status_code(self):
        """ 返回请求状态码 """
        if self.response is None:
            self.connect()
        return self.response.status_code
    
    def get_size(self):
        """ 返回请求大小 """
        if self.head is None:
            self.head = requests.head(self.url, headers=self.headers, data=self.data, proxies=self.proxies, timeout=self.timeout, stream=self.stream, allow_redirects=self.allow_redirects, verify=self.verify)
        return int(self.head.headers['Content-Length'])
        
    def get_text(self):
        """ 返回请求页面text """
        if self.response is None:
            self.connect()
        return self.response.text
    
    def get_content(self):
        """ 返回请求页面content """
        if self.response is None:
            self.connect()
        return self.response.content
    
    def download(self, filepath, replace=False):
        """ 下载请求的文件, 返回文件大小 """
        if self.response is None:
            self.connect()
        
        filepath = filepath.replace('\\', '/')
        path = filepath.rsplit('/', 1)[0] + '/'
        mkdir(path)
        
        # 判断文件是否已经存在，如果存在且大小一致，视为已下载，不重复下载
        content_size = self.get_size()
        if content_size > 0 and os.path.exists(filepath):
            existsFileSize = os.path.getsize(filepath)
            if existsFileSize == content_size:
                return existsFileSize
            elif existsFileSize != content_size and replace:
                rm(filepath)
            else:
                return 0
        elif content_size == 0:
            return 0
        
        try:
            with open(filepath, 'wb') as f:
                for ch in self.response.iter_content(1024):
                    if ch:
                        f.write(ch)
        except Exception as _:
            pass
        finally:
            try:
                f.close()
            except:
                pass
        
        download_size = os.path.getsize(filepath)
        
        if content_size != download_size:
            rm(filepath)
            pass
        
        return download_size
    
    def close(self):
        self.response = None
        self.head = None
    
    def __del__(self):
        self.close()
    
