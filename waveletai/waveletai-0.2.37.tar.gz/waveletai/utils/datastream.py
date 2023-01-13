#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/8 2:27
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : datastream.py
@Desc    : 
"""

import io
import os
import stat
import tarfile
import mimetypes
from waveletai.envs import CHUNK_SIZE
from future.builtins import object

from waveletai.hardware.constants import BYTES_IN_ONE_MB


class FileChunk(object):
    def __init__(self, data, start, end):
        self.data = data
        self.start = start
        self.end = end

    def get_data(self):
        return io.BytesIO(self.data)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FileStream(object):

    def __init__(self, upload_entry):
        self.filename = upload_entry.filename
        self.fobj = io.open(upload_entry.source_path, 'rb')
        self.length = os.path.getsize(upload_entry.source_path)
        self.content_type = mimetypes.guess_type(upload_entry.source_path)[0]

    def close(self):
        self.fobj.close()


class FileChunkStream(object):

    def __init__(self, upload_entry):
        self.filename = upload_entry.filename
        if upload_entry.is_stream():
            self.fobj = upload_entry.source_path
            self.length = None
            self.permissions = '----------'
        else:
            self.fobj = io.open(upload_entry.source_path, 'rb')
            self.length = os.path.getsize(upload_entry.source_path)
            self.content_type = mimetypes.guess_type(upload_entry.source_path)[0]
            self.permissions = self.permissions_to_unix_string(upload_entry.source_path)

    @classmethod
    def permissions_to_unix_string(cls, path):
        st = 0
        if os.path.exists(path):
            st = os.lstat(path).st_mode
        is_dir = 'd' if stat.S_ISDIR(st) else '-'
        dic = {'7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--', '3': '-wx', '2': '-w-', '1': '--x', '0': '---'}
        perm = ("%03o" % st)[-3:]
        return is_dir + ''.join(dic.get(x, x) for x in perm)

    def __eq__(self, fs):
        if isinstance(self, fs.__class__):
            return self.__dict__ == fs.__dict__
        return False

    def generate(self, chunk_size=CHUNK_SIZE):
        last_offset = 0
        while True:
            chunk = self.fobj.read(chunk_size)
            if chunk:
                if isinstance(chunk, str):
                    chunk = chunk.encode('utf-8')
                new_offset = last_offset + len(chunk)
                yield FileChunk(chunk, last_offset, new_offset)
                last_offset = new_offset
            else:
                if last_offset == 0:
                    yield FileChunk(b'', 0, 0)
                break

    def close(self):
        self.fobj.close()


def compress_to_tar_gz_in_memory(upload_entries):
    f = io.BytesIO(b'')

    with tarfile.TarFile.open(fileobj=f, mode='w|gz', dereference=True) as archive:
        for entry in upload_entries:
            archive.add(name=entry.source_path, arcname=entry.target_path, recursive=True)

    f.seek(0)
    data = f.read()
    return data
