#!/usr/bin/env python3
import sys
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from joblib import delayed

from flatspin.data import *
from flatspin.utils import *
from flatspin.cmdline import *
from flatspin.grid import Grid
from flatspin.plotting import montage_fig, vector_montage, save_animation, gridless_crop

def load_vector_data(dataset, args):
    quantity = args.quantity
    t = parse_time(args.t, numeric_dict(dataset.params))
    grid_size = args.grid
    crop_width = args.crop
    win_shape, win_step = args.window if args.window else (None, None)

    time, UV = read_vectors(dataset.tablefiles(), quantity, t)
    pos, angle = read_geometry(dataset.tablefile('geometry'))

    if UV.shape[1:] != pos.shape:
        # global field
        assert UV.shape[1:] == (1,2)
        UV = np.repeat(UV, len(pos), axis=1)

    if grid_size == (0, 0):
        # Grid disabled
        if args.crop:
            in_crop = gridless_crop(pos, args.crop)

            pos = pos[in_crop]
            UV = UV[:,in_crop]
        return time, pos, UV

    XY, UV = vector_grid(pos, UV, grid_size, crop_width, win_shape, win_step, normalize=False)

    return time, XY, UV




def main_load_data(dataset, args):
    # Do it in parallell
    progress_bar = ProgressBar(desc="Loading data", total=len(dataset))
    parallel = ParallelProgress(progress_bar, n_jobs=-1)

    data = parallel(
        delayed(load_vector_data)(ds, args)
        for ds in dataset)

    progress_bar.close()

    times, positions, vectors = tuple(zip(*data)) # unzip
    # TODO: assumes runs have the same number of timesteps
    times = np.array(times)

    # Normalize vectors to unit length
    nmax = np.max([norm(v.reshape((-1,2)), axis=-1).max() for v in vectors])
    if nmax != 0:
        vectors = [v / nmax for v in vectors]

    if args.compress:
        # Filter out states/timesteps where none of the runs change state
        print(f"Compressed {times.shape[1]} -> ", end="")

        # For each run, compare all vectors over time
        mask = [v[1:] == v[:-1] for v in vectors]

        # For each run, find states with no changes
        mask = [m.reshape((m.shape[0], -1)) for m in mask]
        mask = [~np.all(m, axis=-1) for m in mask]

        # Combine above information across runs:
        # keep time steps where any of the runs have changed state
        mask = np.any(mask, axis=0)

        # Always show first state
        mask = np.concatenate(([True], mask))

        # Filter out times/vectors where nothing has changed
        times = times[:, mask]
        vectors = [v[mask] for v in vectors]

        print(f"{times.shape[1]} frames")

    return times, positions, vectors

def main_vectors_anim_time(dataset, args):
    """ Animate over time, montage over dataset """
    param = args.param if args.param else dataset.index.columns[0]

    dataset = dataset.sort_values(param)

    times, positions, vectors = main_load_data(dataset, args)
    n_images = len(times)
    n_frames = len(times[0])

    label = args.label
    if label is None:
        if np.issubdtype(dataset.index[param].dtype, np.number):
            label = param + "={" + param + ":g}"
        else:
            label = param + "={" + param + "}"

    labels = None
    if label:
        labels = [label.format(**dict(row, i=i)) for i, row in dataset.index.iterrows()]

    title = args.title if args.title is not None else "t={t:g}"

    fig, axes = montage_fig(n_images, title or label)

    def init():
        pass

    def step(i):
        t = times[0][i]
        vec = [v[i] for v in vectors]

        if title:
            kw = {'name': dataset.name, 'basepath': dataset.basepath, 't': t}
            kw.update(dataset.params)
            kw.update(dataset.index.iloc[0])
            fig.suptitle(title.format(**kw))

        vector_montage(axes, positions, vec, labels, args.arrows, cmap=args.cmap)

    repeat = n_frames > 1
    ani = animation.FuncAnimation(fig, step, n_frames, init_func=init,
            interval=1000/args.fps, blit=False, save_count=sys.maxsize,
            repeat=repeat)

    return ani

def main_vectors_anim_dataset(dataset, args):
    """ Animate over dataset, montage over time """
    param = args.param if args.param else dataset.index.columns[0]

    dataset = dataset.sort_values(param)

    times, positions, vectors = main_load_data(dataset, args)

    n_images = len(vectors[0])
    n_frames = len(times)

    label = args.label if args.label is not None else "t={t:g}"
    title = args.title if args.title is not None else param + "={" + param + "}"

    fig, axes = montage_fig(n_images, title)

    def init():
        pass

    def step(i):
        time = times[i]
        XY = positions[i]
        UV = vectors[i]

        assert len(UV) == n_images

        if title:
            kw = {'name': dataset.name, 'basepath': dataset.basepath,
                  'index': dataset.index.index[i]}
            kw.update(dataset.params)
            kw.update(dataset.index.iloc[i])
            fig.suptitle(title.format(**kw))

        if label:
            labels = [label.format(t=t) for t in time]
        else:
            labels = None

        vector_montage(axes, [XY]*n_images, UV, labels, args.arrows, cmap=args.cmap)

    repeat = n_frames > 1
    ani = animation.FuncAnimation(fig, step, n_frames, init_func=init,
            interval=1000/args.fps, blit=False, save_count=sys.maxsize,
            repeat=repeat)

    return ani

def main_vectors(dataset, args):
    if args.dark:
        plt.style.use("dark_background")
    if args.grid == (0, 0):
        # Grid disabled
        if not args.arrows:
            raise ValueError("Image-based visualization not possible without a grid, try --arrows?")
        #if args.crop:
        #    raise ValueError("Can't --crop without a grid")
        if args.window:
            raise ValueError("Can't --window without a grid")

    if args.animate_dataset:
        ani = main_vectors_anim_dataset(dataset, args)
    else:
        ani = main_vectors_anim_time(dataset, args)

    if args.output:
        save_animation(ani, args.output, args.fps, args.dpi)
    else:
        plt.show()
    return 0


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_grid_argparser("Plot vector data.")

parser.add_argument('-p', '--param', help='montage over given parameter')
parser.add_argument('-a', '--animate-dataset', action='store_true',
        help='animate over dataset (instead of time)')
parser.add_argument('-q', '--quantity', default='mag',
        help='quantity to view (default: %(default)s)')
parser.add_argument('--fps', type=float, default=30,
        help='frames per second (default: %(default)s)')
parser.add_argument('--dpi', type=int, default=100,
        help='dots per inch (default: %(default)s)')
parser.add_argument('--title', help='title format string', nargs='?', const="",)
parser.add_argument('--dark', action='store_true', help='dark mode')
parser.add_argument('--label', help='label format', nargs='?', const="",)
parser.add_argument('--arrows', action='store_true', help='draw arrows')
parser.add_argument('--cmap', default='flatspin', help='set colormap')
parser.add_argument('--compress', action='store_true',
        help='filter time steps where there is no change in state')

def main():
    args = parser.parse_args()
    ds = main_dataset(args)
    return main_vectors(ds, args)

if __name__ == '__main__':
    main()
