"""
Grid
"""
import numpy as np
from numba import jit

@jit(nopython=True)
def add_values_fast(grid_values, grid_inds, values):
    # add values to the grid
    for i in range(len(grid_inds)):
        gi, gj = grid_inds[i]
        grid_values[gi, gj] += values[i]

class Grid:
    def __init__(self, points, cell_size=None, padding=None):
        """ Create a regular grid over points

        Allows quick lookup of point index -> grid index

        Parameters:
        -----------
        points : array
            List of points to place on the grid
        cell_size : tuple
            Size og each cell on the grid
            If not provided, attempts to auto-detect a suitable cell_size such
            that each cell contains at most one point.
        padding : tuple
            Offset each point by a padding to ensure they don't fall exactly on
            a cell edge
        """
        if cell_size is None:
            # auto-detect
            X = np.around(points[...,0], 12) # 12 seems to work...
            Y = np.around(points[...,1], 12)

            X = np.unique(X)
            Y = np.unique(Y)

            # determine smallest spacing
            dX = np.min(X[1:] - X[:-1]) if len(X) > 1 else 1
            dY = np.min(Y[1:] - Y[:-1]) if len(Y) > 1 else 1

            cell_size = (dX, dY)

        if np.isscalar(cell_size):
            cell_size = (cell_size, cell_size)

        self.cell_size = cell_size

        if padding is None:
            padding = (cell_size[0]/2, cell_size[1]/2)

        if np.isscalar(padding):
            padding = (padding, padding)

        self.padding = padding

        cell_size = np.array(cell_size)
        padding = np.array(padding)

        # In case of negative points
        pos = points - np.min(points, axis=0)

        # Lookup table of point index to grid index
        self._grid_index = ((pos + padding) / cell_size).astype(int)

        # Flip x,y -> y,x to get (row, col)
        self._grid_index = np.flip(self._grid_index, axis=-1)

        # Calculate size of grid (nrows, ncols)
        flatindex = self._grid_index.reshape((-1, self._grid_index.shape[-1]))
        self.size = tuple(np.max(flatindex, axis=0) + 1)

        # Calculate the extent (bounding box)
        xmin = np.min(points[...,0])
        ymin = np.min(points[...,1])
        width = (self.size[1] * cell_size[0])
        height = (self.size[0] * cell_size[1])
        x0 = xmin - padding[0]
        y0 = ymin - padding[1]

        self.extent = (x0, y0, x0 + width, y0 + height)

    def centers(self):
        """ Return the centers of the grid cells """
        x0, y0, width, height = self.extent
        x = np.arange(x0 + self.cell_size[0] / 2, width, self.cell_size[0])
        y = np.arange(y0 + self.cell_size[1] / 2, height, self.cell_size[1])
        return x, y

    def edges(self):
        """ Return the edges of the grid cells """
        x0, y0, width, height = self.extent
        x = np.linspace(x0, width, self.size[1]+1)
        y = np.linspace(y0, height, self.size[0]+1)
        return x, y

    def center_grid(self):
        """ Make a grid with the cell centers """
        x, y = self.centers()
        xx, yy = np.meshgrid(x, y)
        return np.stack((xx, yy), axis=-1)

    @classmethod
    def fixed_grid(cls, pos, grid_size):
        """ Make a grid with a fixed size """
        X = np.unique(np.round(pos[...,0], 12))
        Y = np.unique(np.round(pos[...,1], 12))

        # Determine padding based on smallest spacing
        dX = np.min(X[1:] - X[:-1]) if len(X) > 1 else 1
        dY = np.min(Y[1:] - Y[:-1]) if len(Y) > 1 else 1
        padding = (dX/2, dY/2)

        width = (np.max(X) - np.min(X)) + 2 * padding[0]
        height = (np.max(Y) - np.min(Y)) + 2 * padding[1]
        cell_size = (width / grid_size[0]), (height / grid_size[1])

        padx = min(padding[0], cell_size[0]/2)
        pady = min(padding[1], cell_size[1]/2)
        padding = (padx, pady)

        return cls(pos, cell_size, padding)

    def grid_index(self, point_inds):
        """ Map point index to grid index

        If point_inds is a single index i, a single grid index (gi, gj) is
        returned.

        If point_inds is a list of indices, it should take the form of an
        integer array index: ([i0, i1, i2, ...], [j0, j1, j2, ...])
        The corresponding grid indices are returned in the same format.

        See https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#integer-array-indexing
        """
        gi = self._grid_index[point_inds].T
        return tuple(gi)

    def point_index(self, grid_index):
        """ Map one grid index to zero or more point indices """
        return np.flatnonzero(np.all(self._grid_index == grid_index, axis=-1))

    def map_values(self, values, fill_value=0, mask_empty=False):
        """ Map values onto the grid

        Returns a 2D array with the values mapped onto the grid
        """
        values = np.array(values)
        indices = np.arange(len(values))
        grid_inds = self.grid_index(indices)

        # start with an empty grid
        grid_size = self.size
        if len(values.shape) > 1:
            # e.g. for vectors
            grid_size = grid_size + values.shape[1:]

        grid_values = np.full(grid_size, fill_value, dtype=values.dtype)

        # map values onto the grid
        grid_values[grid_inds] = values

        if mask_empty:
            mask = np.ones(grid_size, dtype=bool)
            mask[grid_inds] = False
            grid_values = np.ma.array(grid_values, mask=mask)

        return grid_values

    def add_values(self, values, fill_value=0, mask_empty=False, method='sum'):
        """ Add values to the grid

        Returns a 2D array with the values summed to the grid

        Parameters:
        -----------
        values : array or list
            Values to map onto the grid cells
        fill_value : scalar
            Fill value for empty cells
        method : {'sum', 'mean'}
            How to aggregate multiple values which map to the same cell
        """
        values = np.array(values)
        indices = np.arange(len(values))
        grid_inds = self.grid_index(indices)

        # start with an empty grid
        grid_size = self.size
        if len(values.shape) > 1:
            # e.g. for vectors
            grid_size = grid_size + values.shape[1:]

        grid_values = np.full(grid_size, fill_value, dtype=values.dtype)

        # add values to the grid
        add_values_fast(grid_values, np.transpose(grid_inds), values)

        if method == 'mean':
            # calculate number of values added to each cell
            unique, num_values = np.unique(np.transpose(grid_inds), return_counts=True, axis=0)
            u = tuple(unique.T)
            if len(num_values.shape) < len(grid_values[u].shape):
                num_values.shape += (1,)

            grid_values[u] = grid_values[u] / num_values

        if mask_empty:
            mask = np.ones(grid_size, dtype=bool)
            mask[grid_inds] = False
            grid_values = np.ma.array(grid_values, mask=mask)

        return grid_values
