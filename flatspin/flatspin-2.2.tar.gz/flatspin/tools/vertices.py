#!/usr/bin/env python3
import sys
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.util import view_as_windows
from joblib import delayed

from flatspin.data import *
from flatspin.utils import *
from flatspin.cmdline import *
from flatspin.grid import Grid
from flatspin.vertices import find_vertices, vertex_pos, vertex_mag

from . import vectors

def load_vertex_data(dataset, args):

    quantity = args.quantity
    t = parse_time(args.t, numeric_dict(dataset.params))
    # Not sure we need grid/crop/win for vertices, but can comment out the
    # lines below to enable it later
    #grid_size = args.grid
    #crop_width = args.crop
    #win_shape, win_step = args.window if args.window else (None, None)
    vertex_size = tuple(args.vertex_size)

    time, UV = read_vectors(dataset.tablefiles(), quantity, t)
    pos, angle = read_geometry(dataset.tablefile('geometry'))

    if UV.shape[1:] != pos.shape:
        # global field
        assert UV.shape[1:] == (1,2)
        UV = np.repeat(UV, len(pos), axis=1)

    # Map the vectors on the native grid
    grid = Grid(pos)

    vi, vj, vertices = find_vertices(grid, pos, angle, vertex_size)

    XY = vertex_pos(pos, vertices)
    UV = np.array([vertex_mag(UVi, vertices) for UVi in UV])

    # Apply vector grid on the vertices
    #XY, UV = vector_grid(XY, UV, grid_size, crop_width, win_step, normalize=False)

    return time, XY, UV


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser("Plot vertices.")
#parser = main_dataset_grid_argparser("Plot vertices")

parser.add_argument('-t', default='::spp',
        help='time range start:stop:step (default: %(default)s)')
parser.add_argument('--vertex-size', nargs=2, type=int, default=(3, 3),
        help='Size of vertex window')
parser.add_argument('--what', choices=('type', 'mag'), default='mag')
parser.add_argument('-p', '--param', help='montage over given parameter')
parser.add_argument('-a', '--animate-dataset', action='store_true',
        help='animate over dataset (instead of time)')
parser.add_argument('-q', '--quantity', default='mag',
        help='quantity to view (default: %(default)s)')
parser.add_argument('--fps', type=float, default=30,
        help='frames per second (default: %(default)s)')
parser.add_argument('--title', help='title format string')
parser.add_argument('--dark', action='store_true', help='dark mode')
parser.add_argument('--label', help='label format')
#parser.add_argument('--arrows', action='store_true', help='draw arrows')
parser.add_argument('--cmap', default='flatspin', help='set colormap')
parser.add_argument('--compress', action='store_true',
        help='filter time steps where there is no change in state')

def main():
    args = parser.parse_args()

    # Monkey patch vectors to load vertices :)
    vectors.load_vector_data = load_vertex_data
    # Always draw arrows
    args.arrows = True
    # Grid, crop and window not supported (for now)
    args.grid = (0, 0)
    args.crop = None
    args.window = None

    ds = main_dataset(args)

    vectors.main_vectors(ds, args)

if __name__ == '__main__':
    main()
