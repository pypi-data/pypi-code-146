import os
from abc import ABC

class Export(ABC):
    def cleanup(self):
        pass

class Data(Export):
    def __init__(self, data):
        self.data = data

class URL(Export):
    def __init__(self, url):
        self.url = url

class LocalFile(Export):
    def __init__(self, path):
        self.path = path

    def cleanup(self):
        os.remove(self.path)

class CloudFile(Export):
    def __init__(self, client, bucket, key):
        self.client = client
        self.bucket = bucket
        self.key = key

    def cleanup(self):
        self.client.rm(self.bucket, self.key)

class CloudDir(Export):
    def __init__(self, client, bucket, directory):
        self.client = client
        self.bucket = bucket
        self.directory = directory

    def cleanup(self):
        self.client.rmtree(self.bucket, self.directory)
