from indra import api
import numpy as np
import deeplake
import pytest
from .constants import (
    MNIST_DS_NAME,
)


def check_equality(dsv, ds, slice):
    for i, x in enumerate(slice):
        assert dsv.tensors[1][i] == ds.tensors[1][x]


def test_dataset_slicing():
    ds = api.dataset(MNIST_DS_NAME)
    dsv = ds[0:1000]
    check_equality(dsv, ds, range(0, 1000))
    dsv = ds[0:1000:7]
    check_equality(dsv, ds, range(0, 1000, 7))
    dsv = ds[0:1000:5]
    check_equality(dsv, ds, range(0, 1000, 5))
    dsv = ds[337:5647:13]
    check_equality(dsv, ds, range(337, 5647, 13))

    dsvv = dsv[1:50:6]
    check_equality(dsvv, dsv, range(1, 50, 6))
    dsvv = dsv[[5, 3, 8, 1, 90, 80, 70]]
    check_equality(dsvv, dsv, [5, 3, 8, 1, 90, 80, 70])
    with pytest.raises(IndexError):
        dsvv = dsv[[5, 3, 8, 1, 2000, 90, 80, 70]]

    dsv = ds[[1, 59999, 49999, 4999, 399, 29]]
    check_equality(dsv, ds, [1, 59999, 49999, 4999, 399, 29])
    dsvv = dsv[[5, 3, 1, 4, 2, 0]]
    check_equality(dsvv, dsv, [5, 3, 1, 4, 2, 0])
    dsvv = dsv[1:5:2]
    check_equality(dsvv, dsv, range(1, 5, 2))


def test_advanced_slicing_and_equality():
    ds = api.dataset(MNIST_DS_NAME)
    deeplake_ds = deeplake.dataset(MNIST_DS_NAME, read_only=True)
    assert (
        len(ds[slice(None, None, None)])
        == len(deeplake_ds[slice(None, None, None)])
        == 60000
    )
    assert (
        len(ds[slice(None, None, -1)])
        == len(deeplake_ds[slice(None, None, -1)])
        == 60000
    )
    assert len(ds[slice(None, -1, -1)]) == len(deeplake_ds[slice(None, -1, -1)]) == 0
    assert len(ds[slice(None, -2, -1)]) == len(deeplake_ds[slice(None, -2, -1)]) == 1

    ds_view = ds[slice(None, -3, -1)]
    dp_ds_view = deeplake_ds[slice(None, -3, -1)]
    assert len(ds_view) == len(dp_ds_view)

    for i in range(len(ds_view)):
        assert np.array_equal(ds_view.tensors[0][i], dp_ds_view.images[i].numpy())
