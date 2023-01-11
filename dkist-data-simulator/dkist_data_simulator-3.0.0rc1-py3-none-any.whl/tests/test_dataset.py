# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
import io
from pathlib import Path

import numpy as np
import pytest  # type: ignore
from astropy.io import fits

from dkist_data_simulator.dataset import Dataset, key_function
from dkist_data_simulator.spec122 import Spec122Schema


class DatasetTest(Dataset):
    @property
    def data(self):
        return np.random.random(self.array_shape)


@pytest.fixture
def dataset_1d():
    ds_shape = (2, 11, 10)
    array_shape = (1, 11, 10)
    return DatasetTest(Spec122Schema(), ds_shape, array_shape)


@pytest.fixture
def dataset_5d():
    ds_shape = (14, 13, 12, 11, 10)
    array_shape = (11, 10)
    return DatasetTest(Spec122Schema(), ds_shape, array_shape)


def test_dimensionality():
    ds_shape = (10, 10, 10, 10)
    array_shape = (1, 10, 10)
    ds = Dataset(Spec122Schema(), ds_shape, array_shape)
    assert ds.dataset_shape == ds_shape
    assert ds.array_shape == array_shape
    assert ds.data_shape == (10, 10)
    assert ds.files_shape == (10, 10)
    assert ds.array_ndim == 3
    assert ds.data_ndim == 2
    assert ds.dataset_ndim == 4


def test_dimensionality2():
    ds_shape = (14, 13, 12, 11, 10)
    array_shape = (1, 1, 1, 11, 10)
    ds = Dataset(Spec122Schema(), ds_shape, array_shape)
    assert ds.dataset_shape == ds_shape
    assert ds.array_shape == array_shape
    assert ds.data_shape == (11, 10)
    assert ds.files_shape == (14, 13, 12)
    assert ds.array_ndim == 5
    assert ds.data_ndim == 2
    assert ds.dataset_ndim == 5


def test_dimensionality3(dataset_5d):
    assert dataset_5d.dataset_shape == (14, 13, 12, 11, 10)
    assert dataset_5d.array_shape == (11, 10)
    assert dataset_5d.data_shape == (11, 10)
    assert dataset_5d.files_shape == (14, 13, 12)
    assert dataset_5d.array_ndim == 2
    assert dataset_5d.data_ndim == 2
    assert dataset_5d.dataset_ndim == 5


def test_index(dataset_5d):
    # pylint: disable=protected-access
    assert dataset_5d._index == dataset_5d.index == 0

    assert dataset_5d.file_index == (0, 0, 0)

    dataset_5d._index = 100

    assert dataset_5d.file_index == (0, 8, 4)


def test_dataset_subclass():
    class TestDataset(Dataset):
        @key_function("INSTRUME")
        def instrume(self, key):
            return "Test"

    ds = TestDataset(Spec122Schema(), (128, 10, 10), (10, 10))

    assert len(ds._generator_functions) == 1
    assert ds._generator_functions["INSTRUME"] == TestDataset.instrume


def test_dataset_subclass_tuple():
    class TestDataset(Dataset):
        @key_function("INSTRUME", "OBSERVAT")
        def instrume(self, key):
            return "Test"

    ds = TestDataset(Spec122Schema(), (128, 10, 10), (10, 10))

    assert len(ds._generator_functions) == 2
    assert ds._generator_functions["INSTRUME"] == TestDataset.instrume
    assert ds._generator_functions["OBSERVAT"] == TestDataset.instrume


def test_dataset_constant_key(dataset_5d):
    dataset_5d.add_constant_key("INSTRUME")
    assert len(dataset_5d._fixed_keys) == 1
    assert isinstance(dataset_5d._fixed_keys["INSTRUME"], str)


def test_generate_headers(dataset_5d):
    dataset_5d.add_constant_key("INSTRUME", "CADAIR")

    def make_index(ds, key):
        ind = int(key[-1])
        return ds.file_index[3 - ind]

    dataset_5d.add_generator_function(("DINDEX1", "DINDEX2", "DINDEX3"), make_index)

    with pytest.warns(UserWarning):
        headers = dataset_5d.generate_headers()

    assert len(headers) == dataset_5d.n_files


def test_generate_files(dataset_1d, tmpdir):
    dataset_1d.add_constant_key("INSTRUME", "CADAIR")

    files = dataset_1d.generate_files(Path(tmpdir), "{ds.index}.fits")

    for f in files:
        assert f.exists()


def test_generate_file_bytes_io(dataset_1d):
    dataset_1d.add_constant_key("INSTRUME", "CADAIR")

    for ds in dataset_1d:
        fobj = ds.file(io.BytesIO())

        assert isinstance(fobj, io.BytesIO)
        assert fobj.read(6) == b"SIMPLE"


def test_generate_hdu_uncompressed(dataset_1d):
    dataset_1d.add_constant_key("INSTRUME", "CADAIR")

    for ds in dataset_1d:
        hdu = ds.hdu()
        assert isinstance(hdu, fits.PrimaryHDU)
        assert hdu.header["INSTRUME"] == "CADAIR"
        target = io.BytesIO()
        hdu.writeto(target, output_verify="exception", overwrite=True, checksum=True)


def test_generate_hdu_compressed(dataset_1d):
    dataset_1d.add_constant_key("INSTRUME", "CADAIR")

    for ds in dataset_1d:
        hdu = ds.hdu(rice_compress=True)
        assert isinstance(hdu, fits.CompImageHDU)
        assert hdu.header["INSTRUME"] == "CADAIR"
        target = io.BytesIO()
        hdu.writeto(target, output_verify="exception", overwrite=True, checksum=True)


def test_generate_hdu_compressed_kwargs(dataset_1d):
    dataset_1d.add_constant_key("INSTRUME", "CADAIR")

    for ds in dataset_1d:
        hdu = ds.hdu(rice_compress={"compression_type": "GZIP_1"})
        assert isinstance(hdu, fits.CompImageHDU)
        assert hdu.header["INSTRUME"] == "CADAIR"
        assert hdu._header["ZCMPTYPE"] == "GZIP_1"
        target = io.BytesIO()
        hdu.writeto(target, output_verify="exception", overwrite=True, checksum=True)


@pytest.mark.parametrize("file_count", [1, 2])
def test_iteration(file_count):
    dataset_shape = (file_count, 10, 10)
    array_shape = (1, 10, 10)
    dataset = Dataset(Spec122Schema(), dataset_shape, array_shape)
    counter = [1 for _ in dataset]
    assert sum(counter) == file_count
