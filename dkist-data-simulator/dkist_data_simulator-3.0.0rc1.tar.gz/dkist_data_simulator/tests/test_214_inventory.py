"""
this file contains tests which verify that inventory generation works.

Because this file leads to a circular test-time dependency between
dkist-inventory and the simulator, these tests are in their own file which is
conditionally skipped depending on the version of the dkist-inventory package.

If you make large changes to dkist-inventory and the simulator which need to be
co-versioned you should bump the major version number of dkist-inventory and
update the skip directive here.

This means that incremental changes to the simulator have unit tests which
verify inventory generation doesn't fail spectacularly.
"""
import pytest

dkist_inventory = pytest.importorskip("dkist_inventory", minversion="0.8.0")

import astropy.units as u
import numpy as np
from astropy.table import Table
from astropy.wcs import WCS
from dkist_header_validator import spec214_validator
from dkist_inventory.inventory import extract_inventory, make_sorted_table

from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec214 import Spec214Dataset
from dkist_data_simulator.spec214.cryo import SimpleCryoCIDataset, SimpleCryoSPDataset
from dkist_data_simulator.spec214.dlnirsp import SimpleDLNIRSPDataset
from dkist_data_simulator.spec214.vbi import MosaicedVBIBlueDataset, SimpleVBIDataset
from dkist_data_simulator.spec214.visp import SimpleVISPDataset
from dkist_data_simulator.spec214.vtf import SimpleVTFDataset


class DatasetTest214(Spec214Dataset):
    @property
    def fits_wcs(self):
        w = WCS(naxis=2)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = 1, 1
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @key_function("FRAMEWAV")
    def framewav(self, key: str):
        """
        Add a random framewav around the line centre
        """
        return (np.random.random() - 0.5) * 100


@pytest.mark.parametrize(
    "ds",
    (
        DatasetTest214(
            dataset_shape=(2, 2, 40, 50), array_shape=(40, 50), time_delta=10
        ),
        SimpleVISPDataset(
            n_maps=2, n_steps=3, n_stokes=4, time_delta=10, linewave=500 * u.m
        ),
        SimpleVISPDataset(
            n_maps=2, n_steps=3, n_stokes=0, time_delta=10, linewave=500 * u.m
        ),
        SimpleVBIDataset(n_time=2, time_delta=10, linewave=400 * u.nm),
        SimpleVTFDataset(
            n_wave=2, n_repeats=3, n_stokes=4, time_delta=10, linewave=400 * u.nm
        ),
        SimpleVTFDataset(
            n_wave=2, n_repeats=3, n_stokes=0, time_delta=10, linewave=400 * u.nm
        ),
        SimpleCryoSPDataset(
            n_maps=3, n_steps=3, n_stokes=4, time_delta=10, linewave=500 * u.m
        ),
        SimpleCryoSPDataset(
            n_maps=3, n_steps=3, n_stokes=0, time_delta=10, linewave=500 * u.m
        ),
        SimpleCryoCIDataset(
            n_maps=3, n_steps=3, n_stokes=4, time_delta=10, linewave=500 * u.m
        ),
        SimpleCryoCIDataset(
            n_maps=3, n_steps=3, n_stokes=0, time_delta=10, linewave=500 * u.m
        ),
        SimpleDLNIRSPDataset(
            n_exposures=3, n_stokes=4, time_delta=10, linewave=400 * u.nm
        ),
        SimpleDLNIRSPDataset(
            n_exposures=3, n_stokes=0, time_delta=10, linewave=400 * u.nm
        ),
        MosaicedVBIBlueDataset(n_time=2, time_delta=10, linewave=400 * u.nm),
    ),
    ids=[
        "DatasetTest214",
        "SimpleVISPDataset-polarized",
        "SimpleVISPDataset",
        "SimpleVBIDataset",
        "SimpleVTFDataset-polarized",
        "SimpleVTFDataset",
        "SimpleCRYOSPDataset-polarized",
        "SimpleCRYOSPDataset",
        "SimpleCRYOCIDataset-polarized",
        "SimpleCRYOCIDataset",
        "SimpleDLNIRSPDataset-polarized",
        "SimpleDLNIRSPDataset",
        "MosaicedVBIBlueDataset",
    ],
)
def test_generate_214(ds):
    headers = ds.generate_headers()

    for h in headers:
        spec214_validator.validate(h)

    # Assert that the datasets generated here pass through gwcs generation and inventory creation.
    # This is the most minimal sanity check possible.

    filenames = [f"{i}.fits" for i in range(len(headers))]
    table_headers = make_sorted_table(Table(headers), filenames)
    inv = extract_inventory(table_headers)
    assert isinstance(inv, dict)
