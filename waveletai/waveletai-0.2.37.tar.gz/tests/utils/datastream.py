#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/9 14:34
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : datastream.py
@Desc    : 
"""

import unittest
from io import StringIO
from waveletai.utils.datastream import FileChunk, FileChunkStream
from waveletai.utils.storage_utils import UploadEntry

class TestFileChunkStream(unittest.TestCase):
    def test_generate_chunks_from_stream(self):
        # given
        text = u"ABCDEFGHIJKLMNOPRSTUWXYZ"

        # when
        stream = FileChunkStream(UploadEntry(StringIO(text), "some/path"))
        chunks = list()
        for chunk in stream.generate(chunk_size=10):
            chunks.append(chunk)

        # then
        print(chunks[0].data)
        print(chunks[1].data)
        print(chunks[2].data)
        self.assertEqual(stream.length, None)
        self.assertEqual(chunks, [
            FileChunk(b"ABCDEFGHIJ", 0, 10),
            FileChunk(b"KLMNOPRSTU", 10, 20),
            FileChunk(b"WXYZ", 20, 24)
        ])

        # when
        stream = FileChunkStream(UploadEntry(
            "C:\\Users\\janus\\Desktop\\test\\大文件\\Car-Price-Prediction-Highly-Comprehensive-Linear-Regression-Project--master.zip",
            "test.zip"))
        chunks = list()
        for chunk in stream.generate():
            chunks.append(chunk)
        print(len(chunks))


if __name__ == '__main__':
    unittest.main()


