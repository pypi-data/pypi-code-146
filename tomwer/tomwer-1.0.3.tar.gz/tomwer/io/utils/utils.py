# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""
contains utils for inputs and outputs
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/09/2020"


import numpy.lib.npyio
import os
from tomoscan.esrf.scan.utils import get_data as tomoscan_get_data
from tomoscan.io import HDF5File
from tomwer.core.utils import ftseriesutils
from PIL import Image
import logging
import h5py
from tomoscan.esrf import has_glymur

try:
    import tifffile  # noqa #F401 needed for later possible lazy loading
except ImportError:
    has_tifffile = False
else:
    has_tifffile = True


_logger = logging.getLogger(__name__)


def get_slice_data(url):
    """Return data from an url"""
    if os.path.exists(url.file_path()) and os.path.isfile(url.file_path()):
        if url.file_path().lower().endswith(
            ".vol.info"
        ) or url.file_path().lower().endswith(".vol"):
            data = _loadVol(url)

        elif url.scheme() == "tomwer":
            data = numpy.array(Image.open(url.file_path()))
            if url.data_slice() is not None:
                data = data[url.data_slice()]
        elif url.scheme() == ("tifffile"):
            if not has_tifffile:
                _logger.warning("tifffile must be installed to read tiff")
                data = None
            else:
                data = tifffile.imread(url.file_path())
                if url.data_slice() is not None:
                    data = data[url.data_slice()]
        elif url.scheme() in ("jp2", "jp2k", "glymur"):
            if not has_glymur:
                _logger.warning("glymur must be installed to read jpeg2000")
                data = None
            else:
                import glymur

                data = glymur.Jp2k(url.file_path())[:]
        else:
            try:
                data = tomoscan_get_data(url)
            except Exception as e:
                _logger.warning(
                    f"file {url} not longer exists or is empty. Error is {e}"
                )
                data = None
    else:
        _logger.warning("file %s not longer exists or is empty" % url)
        data = None
    return data


def _loadVol(url):
    """Load data from a .vol file and an url"""
    if url.file_path().lower().endswith(".vol.info"):
        infoFile = url.file_path()
        rawFile = url.file_path().replace(".vol.info", ".vol")
    else:
        assert url.file_path().lower().endswith(".vol")
        rawFile = url.file_path()
        infoFile = url.file_path().replace(".vol", ".vol.info")

    if not os.path.exists(rawFile):
        data = None
        mess = "Can't find raw data file %s associated with %s" % (rawFile, infoFile)
        _logger.warning(mess)
    elif not os.path.exists(infoFile):
        mess = "Can't find info file %s associated with %s" % (infoFile, rawFile)
        _logger.warning(mess)
        data = None
    else:
        shape = ftseriesutils.get_vol_file_shape(infoFile)
        if None in shape:
            _logger.warning("Fail to retrieve data shape for %s." % infoFile)
            data = None
        else:
            try:
                numpy.zeros(shape)
            except MemoryError:
                data = None
                _logger.warning(
                    "Raw file %s is to large for being " "readed %s" % rawFile
                )
            else:
                data = numpy.fromfile(rawFile, dtype=numpy.float32, count=-1, sep="")
                try:
                    data = data.reshape(shape)
                except ValueError:
                    _logger.warning(
                        "unable to fix shape for raw file %s. "
                        "Look for information in %s"
                        "" % (rawFile, infoFile)
                    )
                    try:
                        sqr = int(numpy.sqrt(len(data)))
                        shape = (1, sqr, sqr)
                        data = data.reshape(shape)
                    except ValueError:
                        _logger.info("deduction of shape size for %s failed" % rawFile)
                        data = None
                    else:
                        _logger.warning(
                            "try deducing shape size for %s "
                            "might be an incorrect "
                            "interpretation" % rawFile
                        )
    if url.data_slice() is None:
        return data
    else:
        return data[url.data_slice()]


def get_default_directory() -> str:
    """

    :return: default directory where to open a QFolder dialdg for example
    :rtype: str
    """
    if "TOMWER_DEFAULT_INPUT_DIR" in os.environ and os.path.exists(
        os.environ["TOMWER_DEFAULT_INPUT_DIR"]
    ):
        return os.environ["TOMWER_DEFAULT_INPUT_DIR"]
    else:
        try:
            return os.getcwd()
        except FileNotFoundError:
            return os.sep


def format_stderr_stdout(stdout, stderr, config=None):
    s_out = stdout.decode("utf-8") if stdout is not None else ""
    s_err = stderr.decode("utf-8") if stderr is not None else ""
    if config is None:
        config = ""
    else:
        assert isinstance(config, dict)
    return (
        "############# nabu ############## \nconfig: {}\n"
        "------------- stderr -------------\n{}\n"
        "------------- stdout -------------\n{}\n".format(config, s_err, s_out)
    )


def get_linked_files_with_entry(hdf5_file: str, entry: str) -> set:
    """
    parse all datasets under the entry and look for connections with external files (vds or ExternalLink)
    """
    items_to_treat = set()  # abs_file_path, file_path, data_path
    final_datasets = set()  # file_path, dataset_path
    treated_items = set()  # abs_file_path, data_path

    abs_hdf5_file = os.path.realpath(hdf5_file)
    items_to_treat.add((abs_hdf5_file, hdf5_file, entry))

    while len(items_to_treat) > 0:
        to_treat = list(items_to_treat)
        items_to_treat.clear()
        for (abs_file_path, file_path, data_path) in to_treat:
            item = abs_file_path, data_path
            if item in treated_items:
                continue
            dirname = os.path.dirname(abs_file_path)
            with HDF5File(abs_file_path, mode="r") as h5f:
                node = h5f.get(data_path, getlink=True)
                if isinstance(node, h5py.ExternalLink):
                    ext_file_path = node.filename
                    if not os.path.isabs(ext_file_path):
                        ext_file_path = os.path.join(dirname, ext_file_path)
                    items_to_treat.add(
                        (os.path.realpath(ext_file_path), node.filename, node.path)
                    )
                node = h5f.get(data_path, getlink=False)
                if isinstance(node, h5py.Dataset) and node.is_virtual:
                    final_datasets.update(
                        get_linked_files_with_vds(abs_file_path, data_path)
                    )
                elif abs_file_path != abs_hdf5_file:
                    final_datasets.add((file_path, data_path))

                treated_items.add(item)

                if isinstance(node, h5py.Group):
                    for key in node.keys():
                        data_sub_path = "/".join((data_path, key))
                        if (
                            abs_file_path,
                            data_sub_path,
                        ) not in treated_items:
                            items_to_treat.add(
                                (abs_file_path, file_path, data_sub_path)
                            )
    return final_datasets


def get_linked_files_with_vds(hdf5_file: str, dataset_path: str) -> set:
    """
    parse all virtual sources of a virtual dataset and return a set of files / dataset connected to it
    """
    items_to_treat = set()  # abs_file_path, file_path, dataset_path
    final_datasets = set()  # file_path, dataset_path
    treated_items = set()  # abs_file_path, dataset_path

    abs_hdf5_file = os.path.realpath(hdf5_file)
    items_to_treat.add((abs_hdf5_file, hdf5_file, dataset_path))

    while len(items_to_treat) > 0:
        to_treat = list(items_to_treat)
        items_to_treat.clear()
        for (abs_file_path, file_path, dataset_path) in to_treat:
            item = abs_file_path, dataset_path
            if item in treated_items:
                continue
            dirname = os.path.dirname(abs_file_path)
            with HDF5File(abs_file_path, mode="r") as h5f:
                dataset = h5f[dataset_path]
                if dataset.is_virtual:
                    for vs_info in dataset.virtual_sources():
                        vs_file_path = vs_info.file_name
                        if not os.path.isabs(vs_file_path):
                            vs_file_path = os.path.join(dirname, vs_file_path)
                        items_to_treat.add(
                            (
                                os.path.realpath(vs_file_path),
                                vs_info.file_name,
                                vs_info.dset_name,
                            )
                        )
                else:
                    final_datasets.add((file_path, dataset_path))
            treated_items.add(item)

    return final_datasets
