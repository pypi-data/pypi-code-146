import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from flatspin.data import *

def test_crop():
    # (height, width)
    X = [[1,2,3,4],
         [5,6,7,8],
         [9,1,2,3]]

    assert_array_equal(crop(X, ((1,1), (1,1))), [[6,7]])
    assert_array_equal(crop(X, (1,1)), [[6,7]])
    assert_array_equal(crop(X, 1), [[6,7]])
    assert_array_equal(crop(X, ((0,0), (1,1))),
            [[2,3],
             [6,7],
             [1,2]])
    assert_array_equal(crop(X, ((1,1), (0,0))), [[5,6,7,8]])

    # (time, height, width)
    X2 = [[[1,2,3,4],
           [5,6,7,8],
           [9,1,2,3]],
          [[4,5,6,7],
           [8,9,1,2],
           [3,4,5,6]]]

    assert_array_equal(crop(X2, ((1,1), (1,1))),
            [[[6,7]],
             [[9,1]]])
    assert_array_equal(crop(X2, ((0,0), (1,1))),
            [[[2,3],
              [6,7],
              [1,2]],
             [[5,6],
              [9,1],
              [4,5]]])
    assert_array_equal(crop(X2, ((1,1), (0,0))),
            [[[5,6,7,8]],
             [[8,9,1,2]]])


    # (time, height, width, 2) - vector image
    X3 = [[[[1,2],[3,4],[5,6]],
           [[7,8],[9,1],[2,3]],
           [[4,5],[6,7],[8,9]]],
          [[[0,1],[2,3],[4,5]],
           [[6,7],[8,0],[1,2]],
           [[3,4],[5,6],[7,8]]]]

    assert_array_equal(crop(X3, ((1,1), (1,1)), axis=-2),
            [[[[9,1]]],
             [[[8,0]]]])
    assert_array_equal(crop(X3, ((0,0), (1,1)), axis=-2),
            [[[[3,4]],
              [[9,1]],
              [[6,7]]],
             [[[2,3]],
              [[8,0]],
              [[5,6]]]])
    assert_array_equal(crop(X3, ((1,1), (0,0)), axis=-2),
            [[[[7,8],[9,1],[2,3]]],
             [[[6,7],[8,0],[1,2]]]])


def test_rolling_window():
    # (height, width)
    X = [[1,2,3,4],
         [5,6,7,8],
         [9,1,2,3]]

    Xr = rolling_window(X, 1)
    assert_array_equal(Xr, X)

    Xr = rolling_window(X, 2)
    expect = [[1+2+5+6, 2+3+6+7, 3+4+7+8],
              [5+6+9+1, 6+7+1+2, 7+8+2+3]]
    assert_array_equal(Xr, expect)

    Xr = rolling_window(X, (3,2))
    expect = [[1+2+5+6+9+1, 2+3+6+7+1+2, 3+4+7+8+2+3]]
    assert_array_equal(Xr, expect)

    Xr = rolling_window(X, (1,2))
    expect = [[1+2, 2+3, 3+4],
              [5+6, 6+7, 7+8],
              [9+1, 1+2, 2+3]]
    assert_array_equal(Xr, expect)

    Xr = rolling_window(X, 2, step=2)
    expect = [[1+2+5+6, 3+4+7+8]]
    assert_array_equal(Xr, expect)

    Xr = rolling_window(X, 2, step=(1,2))
    expect = [[1+2+5+6, 3+4+7+8],
              [5+6+9+1, 7+8+2+3]]
    assert_array_equal(Xr, expect)

    Xr = rolling_window(X, (1,2), step=(1,2))
    expect = [[1+2, 3+4],
              [5+6, 7+8],
              [9+1, 2+3]]
    assert_array_equal(Xr, expect)

    # (height, width, 2)
    X2 = [[[1,2],[3,4],[5,6],[7,8]],
          [[9,1],[2,3],[4,5],[6,7]]]

    Xr = rolling_window(X2, 1)
    assert_array_equal(Xr, X2)

    Xr = rolling_window(X2, (2,2,1), (2,2,1))
    expect = [[[1+3+9+2,2+4+1+3],[5+7+4+6,6+8+5+7]]]
    assert_array_equal(Xr, expect)

    # (time, height, width, 2)
    X3 = [[[[1,2],[3,4],[5,6],[7,8]],
           [[9,1],[2,3],[4,5],[6,7]]],
          [[[8,9],[1,2],[3,4],[5,6]],
           [[7,8],[9,1],[2,3],[4,5]]]]

    Xr = rolling_window(X3, 1)
    assert_array_equal(Xr, X3)

    Xr = rolling_window(X3, (1,2,2,1), (1,2,2,1))
    expect = [[[[1+3+9+2,2+4+1+3],[5+7+4+6,6+8+5+7]]],
              [[[8+1+7+9,9+2+8+1],[3+5+2+4,4+6+3+5]]]]
    assert_array_equal(Xr, expect)

    # Masked arrays
    X = [[1,2,3,4],
         [5,6,7,8],
         [9,1,2,3]]
    mask=[[0,1,0,1],
          [1,1,1,0],
          [1,1,0,1]]
    X = np.ma.array(X, mask=mask)

    Xr = rolling_window(X, 1)
    assert_array_equal(Xr, X)

    Xr = rolling_window(X, 2)
    expect = [[1, 3, 3+8],
              [0, 2, 8+2]]
    assert_array_equal(Xr, expect)

def test_archive_key():
    assert archive_key("foo.npz/table") == ("foo.npz", "table")
    assert archive_key("foo.npz") == ("foo.npz", None)

def test_get_format():
    assert get_format("table.csv") == "csv"
    assert get_format("table.npy") == "npy"
    assert get_format("table.npz") == "npz"
    assert get_format("table.hdf") == "hdf"

    assert get_format("out/table.csv") == "csv"
    assert get_format("out/table.npy") == "npy"
    assert get_format("out/table.npz") == "npz"
    assert get_format("out/table.hdf") == "hdf"

    assert get_format("out.npz/table") == "npz"
    assert get_format("out.hdf/table") == "hdf"

def test_is_archive():
    assert is_archive("foo.hdf")
    assert is_archive("foo.hdf/table")
    assert is_archive("foo.npz")
    assert is_archive("foo.npz/table")

    assert not is_archive("foo.out/table.csv")
    assert not is_archive("foo.out/table.npy")

def test_is_tablefile():
    assert is_tablefile("foo.out/table.csv")
    assert is_tablefile("foo.out/table.npy")

    assert is_tablefile("foo.hdf")
    assert is_tablefile("foo.hdf/table")
    assert is_tablefile("foo.npz/table.npz")
    assert is_tablefile("foo.npz")
    assert is_tablefile("foo.npz/table")
    assert is_tablefile("foo.npz/table.npz")

    assert not is_tablefile("foo.out/file.png")
    assert not is_tablefile("foo/file")

def test_listfiles_dir(tmp_path):
    filenames = [f"file{i}.csv" for i in range(10)]
    for f in filenames:
        open(os.path.join(tmp_path, f), 'w').close()

    expect = [os.path.join(tmp_path, f) for f in filenames]
    assert_array_equal(listfiles(tmp_path), expect)

def test_listfiles_npz(tmp_path):
    tables = {f"tab{i}": np.array([0]) for i in range(10)}
    filename = os.path.join(tmp_path, "data.npz")
    np.savez_compressed(filename, **tables)

    expect = [os.path.join(tmp_path, "data.npz", t) for t in tables.keys()]
    assert_array_equal(listfiles(filename), expect)

@pytest.mark.parametrize("fmt", table_formats)
def test_save_table(tmp_path, fmt):
    df = pd.DataFrame(np.random.randint(0, 10, (10,10),dtype='int64'),
            columns=[f"col{i}" for i in range(10)])

    filename = f"foo.{fmt}"
    if is_archive_format(fmt):
        filename = os.path.join(filename, 'table')

    filename = os.path.join(tmp_path, filename)

    save_table(df, filename)

    if is_archive_format(fmt):
        head, tail = os.path.split(filename)
        assert os.path.isfile(head)
    else:
        assert os.path.isfile(filename)

    df2 = read_table(filename)
    assert df.equals(df2)

    assert_array_equal(table_columns(filename), df.columns)

@pytest.mark.parametrize("fmt", table_formats)
def test_save_dict(tmp_path, fmt):
    data = {'foo': 1, 'bar': 'baz', 'arr': np.arange(3)}
    df = to_table(data)

    filename = f"foo.{fmt}"
    if is_archive_format(fmt):
        filename = os.path.join(filename, 'table')

    filename = os.path.join(tmp_path, filename)

    save_table(df, filename)

    if is_archive_format(fmt):
        head, tail = os.path.split(filename)
        assert os.path.isfile(head)
    else:
        assert os.path.isfile(filename)

    df2 = read_table(filename)

    assert_array_equal(np.array(df), np.array(df2))
