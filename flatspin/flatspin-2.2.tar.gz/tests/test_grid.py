import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from .utils import approx, assert_allclose
from flatspin.grid import Grid

# Some test data: 10x6 grid
# Y/X
#    0  1  2  3  4  5  6  7  8  9
# 0 00 01 02 03 04 05 06 07 08 09
# 1 10 11 12 13 14 15 16 17 18 19
# 2 20 21 22 23 24 25 26 27 28 29
# 3 30 31 32 33 34 35 36 37 38 39
# 4 40 41 42 43 44 45 46 47 48 49
# 5 50 51 52 53 54 55 56 57 58 59
X, Y = np.meshgrid(np.arange(10.0), np.arange(6.0))
X = X.flatten()
Y = Y.flatten()
XY = np.column_stack([X, Y])
YX = np.flip(XY, axis=-1)

def test_cell_size():
    grid = Grid(XY, cell_size=(1,1))

    assert grid.cell_size == (1,1)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (6, 10)
    assert grid.extent == (-0.5, -0.5, 9.5, 5.5)

    assert_array_equal(grid._grid_index, YX)

    grid = Grid(XY, cell_size=1)
    assert grid.cell_size == (1,1)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (6, 10)
    assert grid.extent == (-0.5, -0.5, 9.5, 5.5)

    # auto cell size
    XY2 = XY.copy()
    XY2[:,0] = XY2[:,0] / 2
    XY2[:,1] = XY2[:,1] / 3
    grid = Grid(XY2)

    assert grid.cell_size[0] == approx(1/2)
    assert grid.cell_size[1] == approx(1/3)
    assert grid.padding[0] == approx(1/4)
    assert grid.padding[1] == approx(1/6)
    assert grid.size == (6, 10)
    assert grid.extent == approx((-1/4, -1/6, 9/2 + 1/4, 5/3 + 1/6))

    grid = Grid(XY, cell_size=(2,2), padding=(0.5, 0.5))

    assert grid.cell_size == (2,2)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (3, 5)
    assert grid.extent == (-0.5, -0.5, 9.5, 5.5)

    grid = Grid(XY, cell_size=(3, 3), padding=(0.5, 0.5))

    assert grid.cell_size == (3,3)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (2, 4)
    assert grid.extent == (-0.5, -0.5, 11.5, 5.5)

def test_fixed_grid():
    grid = Grid.fixed_grid(XY, (10, 6))

    assert grid.cell_size == (1, 1)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (6, 10)
    assert grid.extent == (-0.5, -0.5, 9.5, 5.5)

    grid = Grid.fixed_grid(XY, (5, 6))
    assert grid.cell_size == (2, 1)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (6, 5)
    assert grid.extent == (-0.5, -0.5, 9.5, 5.5)

    grid = Grid.fixed_grid(XY, (5, 3))
    assert grid.cell_size == (2, 2)
    assert grid.padding == (0.5, 0.5)
    assert grid.size == (3, 5)
    assert grid.extent == (-0.5, -0.5, 9.5, 5.5)

def test_center_grid():
    grid = Grid(XY, cell_size=(1,1))

    assert_array_equal(grid.center_grid(), XY.reshape(grid.size + (2,)))

    grid = Grid.fixed_grid(XY, (5, 6))
    xx, yy = np.meshgrid(0.5 + np.arange(0, 10.0, 2), np.arange(6.0))
    expect = np.stack([xx, yy], axis=-1)
    assert_array_equal(grid.center_grid(), expect)

    grid = Grid.fixed_grid(XY, (5, 3))
    xx, yy = np.meshgrid(0.5 + np.arange(0, 10.0, 2), 0.5 + np.arange(0, 6.0, 2))
    expect = np.stack([xx, yy], axis=-1)
    assert_array_equal(grid.center_grid(), expect)

def test_grid_index():
    grid = Grid(XY, cell_size=1)
    assert np.all([grid.grid_index(i) == YX[i] for i in range(len(YX))])

    gi, gj = grid.grid_index(np.arange(len(XY)))
    assert_array_equal(gi, Y.astype(int))
    assert_array_equal(gj, X.astype(int))

    grid = Grid(XY, cell_size=2, padding=0.5)
    # refer to table at the top of this file...
    assert grid.grid_index( 0) == grid.grid_index( 1) == (0,0)
    assert grid.grid_index(10) == grid.grid_index(11) == (0,0)
    assert grid.grid_index( 2) == grid.grid_index( 3) == (0,1)
    assert grid.grid_index(12) == grid.grid_index(13) == (0,1)
    assert grid.grid_index( 4) == grid.grid_index( 5) == (0,2)
    assert grid.grid_index(14) == grid.grid_index(15) == (0,2)
    assert grid.grid_index( 6) == grid.grid_index( 7) == (0,3)
    assert grid.grid_index(16) == grid.grid_index(17) == (0,3)
    assert grid.grid_index( 8) == grid.grid_index( 9) == (0,4)
    assert grid.grid_index(18) == grid.grid_index(19) == (0,4)

    assert grid.grid_index(20) == grid.grid_index(21) == (1,0)
    assert grid.grid_index(30) == grid.grid_index(31) == (1,0)
    assert grid.grid_index(22) == grid.grid_index(23) == (1,1)
    assert grid.grid_index(32) == grid.grid_index(33) == (1,1)
    assert grid.grid_index(24) == grid.grid_index(25) == (1,2)
    assert grid.grid_index(34) == grid.grid_index(35) == (1,2)
    assert grid.grid_index(26) == grid.grid_index(27) == (1,3)
    assert grid.grid_index(36) == grid.grid_index(37) == (1,3)
    assert grid.grid_index(28) == grid.grid_index(29) == (1,4)
    assert grid.grid_index(38) == grid.grid_index(39) == (1,4)

    assert grid.grid_index(40) == grid.grid_index(41) == (2,0)
    assert grid.grid_index(50) == grid.grid_index(51) == (2,0)
    assert grid.grid_index(42) == grid.grid_index(43) == (2,1)
    assert grid.grid_index(52) == grid.grid_index(53) == (2,1)
    assert grid.grid_index(44) == grid.grid_index(45) == (2,2)
    assert grid.grid_index(54) == grid.grid_index(55) == (2,2)
    assert grid.grid_index(46) == grid.grid_index(47) == (2,3)
    assert grid.grid_index(56) == grid.grid_index(57) == (2,3)
    assert grid.grid_index(48) == grid.grid_index(49) == (2,4)
    assert grid.grid_index(58) == grid.grid_index(59) == (2,4)

    grid = Grid(XY, cell_size=(5,3), padding=0.5)
    gi, gj = grid.grid_index([0,1,2,3,4,10,11,12,13,14,20,21,22,23,24])
    assert np.all(gi == 0)
    assert np.all(gj == 0)
    gi, gj = grid.grid_index([5,6,7,8,9,15,16,17,18,19,25,26,27,28,29])
    assert np.all(gi == 0)
    assert np.all(gj == 1)
    gi, gj = grid.grid_index([30,31,32,33,34,40,41,42,43,44,50,51,52,53,54])
    assert np.all(gi == 1)
    assert np.all(gj == 0)
    gi, gj = grid.grid_index([35,36,37,38,39,45,46,47,48,49,55,56,57,58,59])
    assert np.all(gi == 1)
    assert np.all(gj == 1)

def test_point_index():
    grid = Grid(XY, cell_size=1)
    grid_inds = np.transpose(grid.grid_index(np.arange(len(XY))))
    assert np.all([grid.point_index(gi) == i for i,gi in enumerate(grid_inds)])

    grid = Grid(XY, cell_size=2, padding=0.5)
    # refer to table at the top of this file...
    assert_array_equal(grid.point_index((0,0)), [0, 1, 10, 11])
    assert_array_equal(grid.point_index((0,1)), [2, 3, 12, 13])
    assert_array_equal(grid.point_index((0,2)), [4, 5, 14, 15])
    assert_array_equal(grid.point_index((0,3)), [6, 7, 16, 17])
    assert_array_equal(grid.point_index((0,4)), [8, 9, 18, 19])

    assert_array_equal(grid.point_index((1,0)), [20, 21, 30, 31])
    assert_array_equal(grid.point_index((1,1)), [22, 23, 32, 33])
    assert_array_equal(grid.point_index((1,2)), [24, 25, 34, 35])
    assert_array_equal(grid.point_index((1,3)), [26, 27, 36, 37])
    assert_array_equal(grid.point_index((1,4)), [28, 29, 38, 39])

    assert_array_equal(grid.point_index((2,0)), [40, 41, 50, 51])
    assert_array_equal(grid.point_index((2,1)), [42, 43, 52, 53])
    assert_array_equal(grid.point_index((2,2)), [44, 45, 54, 55])
    assert_array_equal(grid.point_index((2,3)), [46, 47, 56, 57])
    assert_array_equal(grid.point_index((2,4)), [48, 49, 58, 59])

    grid = Grid(XY, cell_size=(5,3), padding=0.5)
    assert_array_equal(grid.point_index((0,0)), [0,1,2,3,4,10,11,12,13,14,20,21,22,23,24])
    assert_array_equal(grid.point_index((0,1)), [5,6,7,8,9,15,16,17,18,19,25,26,27,28,29])
    assert_array_equal(grid.point_index((1,0)), [30,31,32,33,34,40,41,42,43,44,50,51,52,53,54])
    assert_array_equal(grid.point_index((1,1)), [35,36,37,38,39,45,46,47,48,49,55,56,57,58,59])

def test_map_values():
    grid = Grid(XY, cell_size=1)

    values = np.arange(len(XY))
    mapped = grid.map_values(values)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped.flatten(), values)

    # num values < grid
    values = np.arange(10)
    mapped = grid.map_values(values)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped[0], values)
    assert np.all(mapped[1:] == 0)

    mapped = grid.map_values(values, fill_value=-1)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped[0], values)
    assert np.all(mapped[1:] == -1)

    # mask empty cells
    values = np.arange(10)
    mapped = grid.map_values(values, mask_empty=True)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped[0], values)
    assert np.all(mapped[1:].data == 0)
    assert np.all(mapped.mask[0] == False)
    assert np.all(mapped.mask[1:] == True)

    # multiple values map to same grid cell
    grid = Grid(XY, cell_size=2, padding=0.5)
    values = np.arange(len(XY))
    mapped = grid.map_values(values)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped,
            [[11, 13, 15, 17, 19],
             [31, 33, 35, 37, 39],
             [51, 53, 55, 57, 59]])

    # vector values
    values = YX
    mapped = grid.map_values(values)
    assert mapped.shape == grid.size + (2,)
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped,
            [[[1,1], [1,3], [1,5], [1,7], [1,9]],
             [[3,1], [3,3], [3,5], [3,7], [3,9]],
             [[5,1], [5,3], [5,5], [5,7], [5,9]]])

def test_add_values():
    grid = Grid(XY, cell_size=1)

    values = np.arange(len(XY))
    mapped = grid.add_values(values)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped.flatten(), values)

    # num values < grid
    values = np.arange(10)
    mapped = grid.add_values(values)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped[0], values)
    assert np.all(mapped[1:] == 0)

    mapped = grid.add_values(values, fill_value=-1)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped[0], values-1)
    assert np.all(mapped[1:] == -1)

    # mask empty cells
    values = np.arange(10)
    mapped = grid.add_values(values, mask_empty=True)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    assert_array_equal(mapped[0], values)
    assert np.all(mapped[1:].data == 0)
    assert np.all(mapped.mask[0] == False)
    assert np.all(mapped.mask[1:] == True)

    # multiple values map to same grid cell
    grid = Grid(XY, cell_size=2, padding=0.5)
    values = np.arange(len(XY), dtype=float)
    mapped = grid.add_values(values)
    assert mapped.shape == grid.size
    assert mapped.dtype == values.dtype
    expect = np.array(
            [[0+1+10+11, 2+3+12+13, 4+5+14+15, 6+7+16+17, 8+9+18+19],
             [20+21+30+31, 22+23+32+33, 24+25+34+35, 26+27+36+37, 28+29+38+39],
             [40+41+50+51, 42+43+52+53, 44+45+54+55, 46+47+56+57, 48+49+58+59]],
            )
    assert_array_equal(mapped, expect)

    # mean
    mapped = grid.add_values(values, method='mean')
    assert_array_equal(mapped, expect/4)

    values = [9,3,5]
    mapped = grid.add_values(values, method='mean')
    assert mapped[0,0] == (9+3)/2
    assert mapped[0,1] == 5
    assert_array_equal(mapped.flatten()[2:], 0)

    # vector values
    values = YX
    mapped = grid.add_values(values)
    assert mapped.shape == grid.size + (2,)
    assert mapped.dtype == values.dtype

    assert tuple(mapped[0,0]) == (2,2)
    assert tuple(mapped[0,1]) == (2,10)
    assert tuple(mapped[0,2]) == (2,18)
    assert tuple(mapped[0,3]) == (2,26)
    assert tuple(mapped[0,4]) == (2,34)

    assert tuple(mapped[1,0]) == (10,2)
    assert tuple(mapped[1,1]) == (10,10)
    assert tuple(mapped[1,2]) == (10,18)
    assert tuple(mapped[1,3]) == (10,26)
    assert tuple(mapped[1,4]) == (10,34)

    assert tuple(mapped[2,0]) == (18,2)
    assert tuple(mapped[2,1]) == (18,10)
    assert tuple(mapped[2,2]) == (18,18)
    assert tuple(mapped[2,3]) == (18,26)
    assert tuple(mapped[2,4]) == (18,34)

    values = np.array([[1,2],[3,4],[5,6]])
    mapped = grid.add_values(values, method='mean')
    assert mapped.shape == grid.size + (2,)
    assert mapped.dtype == values.dtype
    assert tuple(mapped[0,0]) == ((1+3)/2, (2+4)/2)
    assert tuple(mapped[0,1]) == (5, 6)
    assert_array_equal(mapped.flatten()[4:], 0)

    # mask empty cells
    mapped = grid.add_values(values, mask_empty=True)
    assert tuple(mapped[0,0]) == (1+3, 2+4)
    assert tuple(mapped[0,1]) == (5, 6)
    assert_array_equal(mapped.flatten()[4:], 0)
    assert mapped.shape == mapped.mask.shape == grid.size + (2,)
    assert mapped.dtype == values.dtype
    assert np.all(mapped.mask[0,0] == False)
    assert np.all(mapped.mask[0,1] == False)
    assert np.all(mapped.mask.flatten()[4:] == True)
