import os
import pytest
from tomwer.core.process.reconstruction.axis.params import AxisResource
from tomwer.core.utils.scanutils import MockHDF5
import numpy


def test_axis_resource(tmp_path):
    """
    Test AxisResource class
    """

    mock = MockHDF5(
        scan_path=os.path.join(tmp_path, "scan1"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=100,
    )
    scan = mock.scan

    first_proj = list(scan.projections.keys())[0]
    data_url = scan.projections[first_proj]

    axis_resource = AxisResource(data_url)

    with pytest.raises(TypeError):
        axis_resource.normalize_data(scan=None, log_=True)

    assert isinstance(
        axis_resource.normalize_data(scan=scan, log_=False), numpy.ndarray
    )
    assert isinstance(axis_resource.normalize_data(scan=scan, log_=True), numpy.ndarray)

    assert isinstance(axis_resource.normalized_data_paganin, numpy.ndarray)

    assert isinstance(axis_resource.normalized_data_paganin, numpy.ndarray)
