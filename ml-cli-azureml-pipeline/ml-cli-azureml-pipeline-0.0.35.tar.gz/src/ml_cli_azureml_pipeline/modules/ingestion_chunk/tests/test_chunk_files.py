import logging
import unittest
import shutil
from pathlib import Path

from chunk_files import chunk_files


BASE_PATH = Path(__file__).resolve().parent


raw_dir = BASE_PATH / 'raw'
output_dir = BASE_PATH / 'output'


class MountMock:
    def __init__(self,):
        self.mount_point = str(raw_dir)


class DatasetMountMock:
    def __enter__(self):
        return MountMock()

    def __exit__(__exit__, arg1, arg2, arg3, arg4=None):
        print("__exit__")


class DatasetMock:

    def mount(self):
        mnt = DatasetMountMock()
        return mnt

class TestFiltserData(unittest.TestCase):
    # Set log level to info
    logging.getLogger().setLevel(logging.INFO)

    def tearDown(self):
       """clean output dir"""
       if output_dir.is_dir():
           shutil.rmtree(str(output_dir))

    def test_chunk_files(self):

        chunk_files(DatasetMock(), str(output_dir), 4, False)

        dir_list = [p for p in Path(str(output_dir)).iterdir() if p.is_dir()]
        self.assertEqual(
            4,
            len(dir_list)
        )
