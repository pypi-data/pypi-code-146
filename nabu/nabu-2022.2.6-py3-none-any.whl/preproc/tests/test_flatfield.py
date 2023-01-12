from tempfile import mkdtemp
import os
import numpy as np
import pytest
from silx.io.url import DataUrl
from silx.io import get_data
from silx.io.dictdump import dicttoh5
from nabu.cuda.utils import get_cuda_context, __has_pycuda__
from nabu.preproc.flatfield import FlatField, FlatFieldDataUrls

if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.preproc.flatfield_cuda import CudaFlatFieldDataUrls, CudaFlatField


# Flats values should be O(k) so that linear interpolation between flats gives exact results
flatfield_tests_cases = {
    "simple_nearest_interp": {
        "image_shape": (100, 512),
        "radios_values": np.arange(10) + 1,
        "radios_indices": None,
        "flats_values": [0.5],
        "flats_indices": [1],
        "darks_values": [1],
        "darks_indices": [0],
        "expected_result": np.arange(0, -2 * 10, -2),
    },
    "two_flats_no_radios_indices": {
        "image_shape": (100, 512),
        "radios_values": np.arange(10) + 1,
        "radios_indices": None,
        "flats_values": [2, 11],
        "flats_indices": [0, 9],
        "darks_values": [1],
        "darks_indices": [0],
        "expected_result": np.arange(10) / (np.arange(10) + 1),
    },
    "two_flats_with_radios_indices": {
        #  Type     D   F   R   R   R   F
        #  IDX      0   1   2   3   4   5
        #  Value    1   4   9   16  25  8
        #  F_interp         5   6   7
        "image_shape": (16, 17),
        # R_k = (k + 1)**2
        "radios_values": [9, 16, 25],
        "radios_indices": [2, 3, 4],
        # F_k = k+3
        "flats_values": [4, 8],
        "flats_indices": [1, 5],
        # D_k = 1
        "darks_values": [1],
        "darks_indices": [0],
        # Expected normalization result: N_k = k
        "expected_result": [2, 3, 4],
    },

    "three_flats_srcurrent": {
        #  Type     D   F   R   R  | R   F   R   R   F
        #  IDX      0   1   2   3  | 4   5   6   7   8
        #  Value    1   4   9   16 | 25  8   46  67  14
        #  F_interp         5   6  | 7       10  12
        #  srCurrent    20  10  10 | 16  32  16  8  16
        "image_shape": (16, 17),
        "radios_values": [9, 16, 25, 46, 67],
        "radios_indices": [2, 3, 4, 6, 7],
        "flats_values": [4, 8, 14],
        "flats_indices": [1, 5, 8],
        "darks_values": [1],
        "darks_indices": [0],
        # "expected_result": [2, 3, 4, 5, 6], # without SR normalization
        "expected_result": [4, 6, 8, 10, 12],
        # sr_flat/sr_radio = 2
        "radios_srcurrent": [10, 16, 16, 16, 8],
        # "flats_srcurrent": [20, 18, 6, 4, 2],
        "flats_srcurrent": [20, 32, 16],
    },


}


def generate_test_flatfield_generalized(
    image_shape,
    radios_indices,
    radios_values,
    flats_indices,
    flats_values,
    darks_indices,
    darks_values,
    h5_fname,
    dtype=np.uint16,
):
    """
    Parameters
    -----------
    image_shape: tuple of int
        shape of each image.
    radios_indices: array of int
        Indices where radios are found in the dataset.
    radios_values: array of scalars
        Value for each radio image.
        Length must be equal to `radios_shape[0]`.
    flats_indices: array of int
        Indices where flats are found in the dataset.
    flats_values: array of scalars
        Values of flat images.
        Length must be equal to `len(flats_indices)`
    darks_indices: array of int
        Indices where darks are found in the dataset.
    darks_values: array of scalars
        Values of dark images.
        Length must be equal to `len(darks_indices)`

    Returns
    -------
    radios: numpy.ndarray
        3D array with raw radios
    darks: dict of DataUrls
        Dictionary where each key is the dark indice, and value is a DataUrl
    flats: dict of DataUrls
        Dictionary where each key is the flat indice, and value is a DataUrl
    """
    tempdir = mkdtemp(prefix="nabu_")
    testffname = os.path.join(tempdir, h5_fname)

    # Radios
    radios = np.zeros((len(radios_values),) + image_shape, dtype="f")
    n_radios = radios.shape[0]
    for i in range(n_radios):
        radios[i].fill(radios_values[i])
    img_shape = radios.shape[1:]

    # Flats
    flats = {}
    flats_urls = {}
    for i, flat_idx in enumerate(flats_indices):
        flats["flats_%04d" % flat_idx] = np.zeros(img_shape, dtype=dtype) + flats_values[i]
        flats_urls[flat_idx] = DataUrl(
            file_path=testffname, data_path=str("/flats/flats_%04d" % flat_idx), scheme="silx"
        )

    # Darks
    darks = {}
    darks_urls = {}
    for i, dark_idx in enumerate(darks_indices):
        darks["darks_%04d" % dark_idx] = np.zeros(img_shape, dtype=dtype) + darks_values[i]
        darks_urls[dark_idx] = DataUrl(
            file_path=testffname, data_path=str("/darks/darks_%04d" % dark_idx), scheme="silx"
        )

    dicttoh5(flats, testffname, h5path="/flats", mode="w")
    dicttoh5(darks, testffname, h5path="/darks", mode="a")

    return radios, flats_urls, darks_urls


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.tmp_files = []
    cls.tmp_dirs = []
    cls.n_radios = 10
    cls.n_z = 100
    cls.n_x = 512
    if __has_pycuda__:
        cls.ctx = get_cuda_context()
    yield
    # Tear-down
    for fname in cls.tmp_files:
        os.remove(fname)
    for dname in cls.tmp_dirs:
        os.rmdir(dname)


@pytest.mark.usefixtures("bootstrap")
class TestFlatField:
    def get_test_elements(self, case_name):
        config = flatfield_tests_cases[case_name]
        radios_stack, flats_url, darks_url = generate_test_flatfield_generalized(
            config["image_shape"],
            config["radios_indices"],
            config["radios_values"],
            config["flats_indices"],
            config["flats_values"],
            config["darks_indices"],
            config["darks_values"],
            "test_ff.h5",
        )
        fname = flats_url[list(flats_url.keys())[0]].file_path()
        self.tmp_files.append(fname)
        self.tmp_dirs.append(os.path.dirname(fname))
        return radios_stack, flats_url, darks_url, config

    @staticmethod
    def check_normalized_radios(radios_corr, expected_values):
        # must be the same value everywhere in the radio
        std = np.std(np.std(radios_corr, axis=-1), axis=-1)
        assert np.max(np.abs(std)) < 1e-7
        # radios values must be 0, -2, -4, ...
        assert np.allclose(radios_corr[:, 0, 0], expected_values)

    def test_flatfield_simple(self):
        """
        Test the flat-field normalization on a radios stack with 1 dark and 1 flat.

        (I - D)/(F - D)   where I = (1, 2, ...), D = 1, F = 0.5
        = (0, -2, -4, -6, ...)
        """
        radios_stack, flats_url, darks_url, config = self.get_test_elements(
            "simple_nearest_interp"
        )

        flatfield = FlatFieldDataUrls(radios_stack.shape, flats_url, darks_url)
        radios_corr = flatfield.normalize_radios(np.copy(radios_stack))
        self.check_normalized_radios(radios_corr, config["expected_result"])

    def test_flatfield_simple_subregion(self):
        """
        Same as test_flatfield_simple, but in a vertical subregion of the radios.
        """
        radios_stack, flats_url, darks_url, config = self.get_test_elements(
            "simple_nearest_interp"
        )
        end_z = 51
        radios_chunk = np.copy(radios_stack[:, :end_z, :])
        # we only have a chunk in memory. Instantiate the class with the
        # corresponding subregion to only load the relevant part of dark/flat
        flatfield = FlatFieldDataUrls(
            radios_chunk.shape,
            flats_url,
            darks_url,
            sub_region=(None, None, None, end_z),  # start_x, end_x, start_z, end_z
        )
        radios_corr = flatfield.normalize_radios(radios_chunk)
        self.check_normalized_radios(radios_corr, config["expected_result"])

    def test_flatfield_linear_interp(self):
        """
        Test flat-field normalization with 1 dark and 2 flats, with linear
        interpolation between flats.
        I   = 1   2   3   4   5   6   7   8   9   10
        D   = 1                                         (one dark)
        F   = 2                                   11    (two flats)
        F_i = 2   3   4   5   6   7   8   9   10  11   (interpolated flats)
        R   = 0  .5  .66 .75 .8  .83  .86
            = (I-D)/(F-D)
            = (I-1)/I
        """
        radios_stack, flats_url, darks_url, config = self.get_test_elements(
            "two_flats_no_radios_indices"
        )
        flatfield = FlatFieldDataUrls(radios_stack.shape, flats_url, darks_url)
        radios_corr = flatfield.normalize_radios(np.copy(radios_stack))
        self.check_normalized_radios(radios_corr, config["expected_result"])

        # Test 2: one of the flats is not at the beginning/end
        # I   = 1    2    3    4    5    6    7    8    9    10
        # F   = 2                       11
        # F_i = 2   3.8  5.6 7.4  9.2   11   11   11   11    11
        # R   = 0   .357  .435 .469 .488 .5  .6   .7  .8     .9
        flats_url = flats_url.copy()
        flats_url[5] = flats_url[9]
        flats_url.pop(9)
        flatfield = FlatFieldDataUrls(radios_stack.shape, flats_url, darks_url)
        radios_corr = flatfield.normalize_radios(np.copy(radios_stack))
        self.check_normalized_radios(
            radios_corr, [0.0, 0.35714286, 0.43478261, 0.46875, 0.48780488, 0.5, 0.6, 0.7, 0.8, 0.9]
        )

    @pytest.mark.skipif(not (__has_pycuda__), reason="Need cuda/pycuda for this test")
    def test_cuda_flatfield(self):
        """
        Test the flat-field with cuda back-end.
        """
        radios_stack, flats_url, darks_url, config = self.get_test_elements(
            "two_flats_no_radios_indices"
        )
        d_radios = garray.to_gpu(radios_stack.astype("f"))
        cuda_flatfield = CudaFlatFieldDataUrls(
            d_radios.shape,
            flats_url,
            darks_url,
        )
        cuda_flatfield.normalize_radios(d_radios)
        radios_corr = d_radios.get()
        self.check_normalized_radios(radios_corr, config["expected_result"])

    # Linear interpolation, two flats, one dark
    def test_twoflats_simple(self):
        radios, flats, darks, config = self.get_test_elements("two_flats_with_radios_indices")
        FF = FlatFieldDataUrls(radios.shape, flats, darks, radios_indices=config["radios_indices"])
        FF.normalize_radios(radios)
        self.check_normalized_radios(radios, config["expected_result"])


    def _setup_numerical_issue(self):
        radios, flats, darks, config = self.get_test_elements("two_flats_with_radios_indices")

        # Retrieve the actual data for radios/darks/flats to use FlatField instead of FlatFieldDataUrl.
        # Create a setting yielding "0/0": one pixel such that flat==dark and radio==dark
        for flat_idx, flat_url in flats.items():
            flats[flat_idx] = get_data(flat_url)
            flats[flat_idx][0, 0] = 99
        for dark_idx, dark_url in darks.items():
            darks[dark_idx] = get_data(dark_url)
            darks[dark_idx][0, 0] = 99
        radios[:, 0, 0] = 99
        return radios, flats, darks, config

    def _check_numerical_issue(self, radios, expected_result, nan_value=None):
        if nan_value is None:
            assert np.alltrue(np.logical_not(np.isfinite(radios[:, 0, 0]))), "First pixel should be nan or inf"
            radios[:, 0, 0] = radios[:, 1, 1]
            self.check_normalized_radios(radios, expected_result)
        else:
            assert np.all(np.isfinite(radios)), "No inf/nan value should be there"
            assert np.allclose(radios[:, 0, 0], nan_value, atol=1e-7), "Handled NaN should have nan_value=%f" % nan_value
            radios[:, 0, 0] = radios[:, 1, 1]
            self.check_normalized_radios(radios, expected_result)


    def test_twoflats_numerical_issue(self):
        """
        Same as above, but for the first radio: I==Dark and Flat==Dark
        For this radio, nan is replaced with 1.
        """
        radios, flats, darks, config = self._setup_numerical_issue()
        radios0 = radios.copy()

        # FlatField without NaN handling yields NaN and raises RuntimeWarning
        FF_no_nan_handling = FlatField(
            radios.shape, flats, darks,
            radios_indices=config["radios_indices"], nan_value=None
        )
        with pytest.warns(RuntimeWarning):
            FF_no_nan_handling.normalize_radios(radios)
        self._check_numerical_issue(radios, config["expected_result"], None)

        # FlatField with NaN handling
        nan_value = 50
        radios = radios0.copy()
        FF_with_nan_handling = FlatField(
            radios.shape, flats, darks,
            radios_indices=config["radios_indices"], nan_value=nan_value
        )
        with pytest.warns(RuntimeWarning):
            FF_with_nan_handling.normalize_radios(radios)
        self._check_numerical_issue(radios, config["expected_result"], nan_value)


    @pytest.mark.skipif(not (__has_pycuda__), reason="Need cuda/pycuda for this test")
    def test_cuda_twoflats_numerical_issue(self):
        """
        Same as above, with the Cuda backend
        """
        radios, flats, darks, config = self._setup_numerical_issue()
        radios0 = radios.copy()
        d_radios = garray.to_gpu(radios)
        FF_no_nan_handling = CudaFlatField(
            radios.shape, flats, darks,
            radios_indices=config["radios_indices"], nan_value=None
        )
        # In a cuda kernel, no one can hear you scream
        FF_no_nan_handling.normalize_radios(d_radios)
        radios = d_radios.get()
        self._check_numerical_issue(radios, config["expected_result"], None)

        # FlatField with NaN handling
        nan_value = 50
        d_radios.set(radios0)
        FF_with_nan_handling = CudaFlatField(
            radios.shape, flats, darks,
            radios_indices=config["radios_indices"], nan_value=nan_value
        )
        FF_with_nan_handling.normalize_radios(d_radios)
        radios = d_radios.get()
        self._check_numerical_issue(radios, config["expected_result"], nan_value)


    def test_srcurrent(self):
        radios, flats, darks, config = self.get_test_elements("three_flats_srcurrent")

        FF = FlatFieldDataUrls(
            radios.shape, flats, darks,
            radios_indices=config["radios_indices"],
            radios_srcurrent=config["radios_srcurrent"],
            flats_srcurrent=config["flats_srcurrent"],
        )
        radios_corr = FF.normalize_radios(np.copy(radios))
        self.check_normalized_radios(radios_corr, config["expected_result"])


    @pytest.mark.skipif(not (__has_pycuda__), reason="Need cuda/pycuda for this test")
    def test_srcurrent_cuda(self):
        radios, flats, darks, config = self.get_test_elements("three_flats_srcurrent")
        d_radios = garray.to_gpu(radios)

        FF = CudaFlatFieldDataUrls(
            radios.shape, flats, darks,
            radios_indices=config["radios_indices"],
            radios_srcurrent=config["radios_srcurrent"],
            flats_srcurrent=config["flats_srcurrent"],
        )
        FF.normalize_radios(d_radios)
        radios_corr = d_radios.get()
        self.check_normalized_radios(radios_corr, config["expected_result"])


# This test should be closer to the ESRF standard setting.
# There are 2 flats, one dark, 4000 radios.
#  dark :  indice=0     value=10
#  flat1 : indice=1     value=4202
#  flat2 : indice=2102  value=2101
#
# The projections have the following indices:
#  j:    0     1        1998  1999  2000  2001                   3999
# idx:  [102, 103, ..., 2100, 2101, 2203, 2204, ..., 4200, 4201, 4202]
#  Notice the gap in the middle.
#
# The linear interpolation is
#    flat_i = (n2 - i)/(n2 - n1)*flat_1  + (i - n1)/(n2 - n1)*flat_2
#  where n1 and n2 are the indices of flat_1 and flat_2 respectively.
# With the above values, we have flat_i = 4203 - i.
#
# The projections values are dark + i*(flat_i - dark),
# so that the normalization norm_i = (proj_i - dark)/(flat_i - dark) gives
#
#   idx     102    103    104    ...
#   flat    4101   4102   4103   ...
#   norm    102    103    104    ...
#


class FlatFieldTestDataset:
    # Parameters
    shp = (27, 32)
    n1 = 1  # flat indice 1
    n2 = 2102  # flat indice 2
    dark_val = 10
    darks = {0: np.zeros(shp, "f") + dark_val}
    flats = {n1: np.zeros(shp, "f") + (n2 - 1) * 2, n2: np.zeros(shp, "f") + n2 - 1}
    projs_idx = list(range(102, 2102)) + list(range(2203, 4203))  # gap in the middle

    def __init__(self):
        self._generate_projections()
        self._dump_to_h5()
        self._generate_dataurls()

    def get_flat_idx(self, proj_idx):
        flats_idx = sorted(list(self.flats.keys()))
        if proj_idx <= flats_idx[0]:
            return (flats_idx[0],)
        elif proj_idx > flats_idx[0] and proj_idx < flats_idx[1]:
            return flats_idx
        else:
            return (flats_idx[1],)

    def get_flat(self, idx):
        flatidx = self.get_flat_idx(idx)
        if len(flatidx) == 1:
            flat = self.flats[flatidx[0]]
        else:
            nf1, nf2 = flatidx
            w1 = (nf2 - idx) / (nf2 - nf1)
            flat = w1 * self.flats[nf1] + (1 - w1) * self.flats[nf2]
        return flat

    def _generate_projections(self):
        self.projs_data = np.zeros((len(self.projs_idx),) + self.shp, "f")
        self.projs = {}
        for i, proj_idx in enumerate(self.projs_idx):

            flat = self.get_flat(proj_idx)

            proj_val = self.dark_val + proj_idx * (flat[0, 0] - self.dark_val)
            self.projs[str(proj_idx)] = np.zeros(self.shp, "f") + proj_val
            self.projs_data[i] = self.projs[str(proj_idx)]

    def _dump_to_h5(self):
        self.tempdir = mkdtemp(prefix="nabu_")
        self.fname = os.path.join(self.tempdir, "projs_flats.h5")
        dicttoh5(
            {
                "projs": self.projs,
                "flats": {str(k): v for k, v in self.flats.items()},
                "darks": {str(k): v for k, v in self.darks.items()},
            },
            h5file=self.fname,
        )

    def _generate_dataurls(self):
        self.flats_urls = {}
        for idx in self.flats.keys():
            self.flats_urls[int(idx)] = DataUrl(file_path=self.fname, data_path="/flats/%d" % idx)
        self.darks_urls = {}
        for idx in self.darks.keys():
            self.darks_urls[int(idx)] = DataUrl(file_path=self.fname, data_path="/darks/0")


@pytest.fixture(scope="class")
def bootstraph5(request):
    cls = request.cls

    cls.dataset = FlatFieldTestDataset()
    n1, n2 = cls.dataset.n1, cls.dataset.n2

    # Interpolation function
    cls._weight1 = lambda i: (n2 - i) / (n2 - n1)

    cls.tol = 5e-4
    cls.tol_std = 1e-3

    yield
    # tear-down
    os.remove(cls.dataset.fname)
    os.rmdir(cls.dataset.tempdir)


@pytest.mark.usefixtures("bootstraph5")
class TestFlatFieldH5:
    def check_normalization(self, projs):
        # Check that each projection is filled with the same values
        std_projs = np.std(projs, axis=(-2, -1))
        assert np.max(np.abs(std_projs)) < self.tol_std
        # Check that the normalized radios are equal to 102, 103, 104, ...
        errs = projs[:, 0, 0] - self.dataset.projs_idx
        assert np.max(np.abs(errs)) < self.tol, "Something wrong with flat-field normalization"

    def test_flatfield(self):
        flatfield = FlatFieldDataUrls(
            self.dataset.projs_data.shape,
            self.dataset.flats_urls,
            self.dataset.darks_urls,
            radios_indices=self.dataset.projs_idx,
            interpolation="linear",
        )
        projs = np.copy(self.dataset.projs_data)
        flatfield.normalize_radios(projs)
        self.check_normalization(projs)

    @pytest.mark.skipif(not (__has_pycuda__), reason="Need cuda/pycuda for this test")
    def test_cuda_flatfield(self):
        d_projs = garray.to_gpu(self.dataset.projs_data)
        cuda_flatfield = CudaFlatFieldDataUrls(
            self.dataset.projs_data.shape,
            self.dataset.flats_urls,
            self.dataset.darks_urls,
            radios_indices=self.dataset.projs_idx,
        )
        cuda_flatfield.normalize_radios(d_projs)
        projs = d_projs.get()
        self.check_normalization(projs)


#
# Another test with more than two flats.
#
# Here we have
#
#   F_i = i + 2
#   R_i = i*(F_i - 1) + 1
#   N_i = (R_i - D)/(F_i - D) = i*(F_i - 1)/( F_i - 1) = i
#

def generate_test_flatfield(n_radios, radio_shape, flat_interval, h5_fname):
    radios = np.zeros((n_radios,) + radio_shape, "f")
    dark_data = np.ones(radios.shape[1:], "f")
    tempdir = mkdtemp(prefix="nabu_")
    testffname = os.path.join(tempdir, h5_fname)
    flats = {}
    flats_urls = {}
    # F_i = i + 2
    # R_i = i*(F_i - 1) + 1
    # N_i = (R_i - D)/(F_i - D) = i*(F_i - 1)/( F_i - 1) = i
    for i in range(n_radios):
        f_i = i + 2
        if (i % flat_interval) == 0:
            flats["flats_%04d" % i] = np.zeros(radio_shape, "f") + f_i
            flats_urls[i] = DataUrl(
                file_path=testffname, data_path=str("/flats/flats_%04d" % i), scheme="silx"
            )
        radios[i] = i * (f_i - 1) + 1
    dark = {"dark_0000": dark_data}
    dicttoh5(flats, testffname, h5path="/flats", mode="w")
    dicttoh5(dark, testffname, h5path="/dark", mode="a")
    dark_url = {0: DataUrl(file_path=testffname, data_path="/dark/dark_0000", scheme="silx")}
    return radios, flats_urls, dark_url


@pytest.fixture(scope="class")
def bootstrap_multiflats(request):
    cls = request.cls

    n_radios = 50
    radio_shape = (20, 21)
    cls.flat_interval = 11
    h5_fname = "testff.h5"

    radios, flats, dark = generate_test_flatfield(
        n_radios, radio_shape, cls.flat_interval, h5_fname
    )
    cls.radios = radios
    cls.flats_urls = flats
    cls.darks_urls = dark
    cls.expected_results = np.arange(n_radios)

    cls.tol = 5e-4
    cls.tol_std = 1e-4

    yield
    # tear down
    os.remove(dark[0].file_path())
    os.rmdir(os.path.dirname(dark[0].file_path()))


@pytest.mark.usefixtures("bootstrap_multiflats")
class TestFlatFieldMultiFlat:
    def check_normalization(self, projs):
        # Check that each projection is filled with the same values
        std_projs = np.std(projs, axis=(-2, -1))
        assert np.max(np.abs(std_projs)) < self.tol_std
        # Check that the normalized radios are equal to 0, 1, 2, ...
        stop = (projs.shape[0] // self.flat_interval) * self.flat_interval
        errs = projs[:stop, 0, 0] - self.expected_results[:stop]
        assert np.max(np.abs(errs)) < self.tol, "Something wrong with flat-field normalization"

    def test_flatfield(self):
        flatfield = FlatFieldDataUrls(
            self.radios.shape, self.flats_urls, self.darks_urls, interpolation="linear"
        )
        projs = np.copy(self.radios)
        flatfield.normalize_radios(projs)
        print(projs[:, 0, 0])
        self.check_normalization(projs)

    @pytest.mark.skipif(not (__has_pycuda__), reason="Need cuda/pycuda for this test")
    def test_cuda_flatfield(self):
        d_projs = garray.to_gpu(self.radios)
        cuda_flatfield = CudaFlatFieldDataUrls(
            self.radios.shape,
            self.flats_urls,
            self.darks_urls,
        )
        cuda_flatfield.normalize_radios(d_projs)
        projs = d_projs.get()
        self.check_normalization(projs)
