from os import path
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.colors import Normalize, ListedColormap, LinearSegmentedColormap
import matplotlib.cm
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
from matplotlib import backend_bases
from scipy.spatial import cKDTree
from copy import deepcopy

fs_colours= [      [.9, .1, .1],
                    [.9, .9, .1],
                    [.1, .7, .2],
                    [.1, .7, .9],
                    [.1, .1, .9],
                    [.9, .1 , .9],
                    [.9, .1, .1]]
matplotlib.cm.unregister_cmap('flatspin')
matplotlib.cm.register_cmap('flatspin', LinearSegmentedColormap.from_list('flatspin', fs_colours, N=1000))
normalize_rad = Normalize(vmin=0, vmax=2*np.pi)

# Colormap from Li et al., (2019)
clist = list('ckkbbkkggkkrrkkc')
clist = ['#00da00' if c == 'g' else c for c in clist]
clist = ['#0800da' if c == 'b' else c for c in clist]
clist = ['#ed0912' if c == 'r' else c for c in clist]
clist = ['#00ccff' if c == 'c' else c for c in clist]

cmap = ListedColormap(clist)
matplotlib.cm.unregister_cmap('li2019')
matplotlib.cm.register_cmap('li2019', cmap)

# Type 1: green, type 2: blue, type 3: red, type 4: gray
clist = [(.1, .7, .2), (.1, .1, .9), (.9, .1, .1), (.4,.4,.4)]
cmap = ListedColormap(clist)
matplotlib.cm.unregister_cmap('vertex-type')
matplotlib.cm.register_cmap('vertex-type', cmap)

def quadrilaterals(X):
    dX = X[1:]-X[:-1]
    dX = np.pad(dX, 1, mode='edge')
    dX[:-1] *= -1 # subtract dX/2 from all but last element, where we add dX/2
    # quads needs one more value (see pcolormesh)
    quads = np.pad(X, (0,1), mode='edge').astype(float)
    quads += dX/2
    return quads

def format_label(label, format_spec='{:g}'):
    if isinstance(label, tuple):
        lbl = ', '.join(map(format_label, label))
        return f'({lbl})'

    if isinstance(label, list):
        return ', '.join(map(format_label, label))

    try:
        return format_spec.format(label)
    except:
        return str(label)

def format_labels(labels, format_spec='{:g}'):
    return [format_label(l, format_spec) for l in labels]

def heatmap2(X, Y, Z, xlabel='x', ylabel='y', zlabel='z', xlabels=None, ylabels=None, **kwargs):
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    print(X.shape, Y.shape, Z.shape)
    print(X.dtype, Y.dtype, Z.dtype)

    if not xlabels:
        xlabels = format_labels(X)

    #if X.dtype == object:
    #    X = np.arange(len(X))

    if not ylabels:
        ylabels = format_labels(Y)

    #if Y.dtype == object:
    #    Y = np.arange(len(Y))

    Xi = np.arange(len(X))
    Yi = np.arange(len(Y))
    print(Yi)
    qX = quadrilaterals(Xi)
    qY = quadrilaterals(Yi)

    def format_coord(x, y):
        # find nearest x,y
        #idx = np.abs(x-Xi).argmin()
        #idy = np.abs(y-Yi).argmin()
        idx = int(x + 0.5)
        idy = int(y + 0.5)
        x = xlabels[idx]
        y = ylabels[idy]
        z = Z[idy, idx]
        return f'{xlabel}={x}, {ylabel}={y}, {zlabel}={z:g}'

    ax = plt.gca()
    ax.format_coord = format_coord
    ax.xaxis.set_major_locator(ticker.FixedLocator(Xi, nbins=min(len(Xi), 10)))
    ax.yaxis.set_major_locator(ticker.FixedLocator(Yi, nbins=min(len(Yi), 10)))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: xlabels[x])))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: ylabels[y])))
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: (x,pos))))
    #ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: (y,pos))))
    #ax.set_xticklabels(xlabels)
    #ax.set_yticklabels(ylabels)
    return plt.pcolormesh(qX, qY, Z, **kwargs)

def heatmap(X, Y, Z, xlabel='x', ylabel='y', zlabel='z',
        xlim=None, ylim=None, zlim=None, nticks=10,
        xlabel_format='{:g}', ylabel_format='{:g}',
        ax=None,
        **kwargs):

    xlabels = format_labels(X, xlabel_format)
    ylabels = format_labels(Y, ylabel_format)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    Xi = np.arange(len(X))
    Yi = np.arange(len(Y))

    def format_coord(x, y):
        try:
            idx = int(x)
            idy = int(y)
            x = xlabels[idx]
            y = ylabels[idy]
            z = Z[idy, idx]
            return f'{xlabel}={x}, {ylabel}={y}, {zlabel}={z:g}'
        except IndexError:
            return ''

    if ax is None:
        ax = plt.gca()

    ax.format_coord = format_coord
    nbins = min(len(Xi), nticks) if X.dtype != 'object' else None
    ax.xaxis.set_major_locator(ticker.FixedLocator(Xi+.5, nbins=nbins))
    nbins = min(len(Yi), nticks) if Y.dtype != 'object' else None
    ax.yaxis.set_major_locator(ticker.FixedLocator(Yi+.5, nbins=nbins))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: xlabels[int(x)])))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: ylabels[int(y)])))

    if zlim:
        kwargs['vmin'], kwargs['vmax'] = zlim

    pcolor = ax.pcolormesh(Z, **kwargs)

    # We have integer indexes on the axes, so need to map x values to x indexes
    if xlim and X.dtype != 'object':
        xmin, xmax = xlim
        ximin = np.argmax(X >= xmin)
        ximax = np.argmax(X > xmax)
        ax.set_xlim(ximin, ximax)

    if ylim and Y.dtype != 'object':
        ymin, ymax = ylim
        yimin = np.argmax(Y >= ymin)
        yimax = np.argmax(Y > ymax)
        ax.set_ylim(yimin, yimax)

    return pcolor

def vector_colors(U, V):
    C = np.arctan2(V, U) # color
    C[C<0] = 2*np.pi + C[C<0]
    return C

def mask_zero_vectors(UV):
    # mask out zero vectors
    mag = norm(UV, axis=-1)
    mask = np.repeat(mag <= 1e-12, 2).reshape(UV.shape)
    return np.ma.array(UV, mask=mask)

def plot_vectors(XY, UV, C=None, arrows=True, mask_zero=True, replace=False, normalize=False, ax=None, **kwargs):
    XY = np.atleast_2d(XY)
    UV = np.atleast_2d(UV)
    XY = XY.reshape((-1, 2)) # quiver wants 2D XY
    X = XY[...,0] # x components
    Y = XY[...,1] # y components

    if normalize:
        # Normalize vectors to unit length
        nmax = norm(UV.reshape((-1,2)), axis=-1).max()
        if nmax != 0:
            UV = UV / nmax

    if mask_zero:
        UV = mask_zero_vectors(UV)

    U = UV[..., 0] # x components
    V = UV[..., 1] # y components
    if C is None:
        C = vector_colors(U, V)
        kwargs.setdefault('norm', normalize_rad)
    #C = np.arctan2(V, U) # color
    #C[C<0] = 2*np.pi + C[C<0]

    if ax is None:
        ax = plt.gca()

    if replace and len(ax.collections) > 0:
        quiv = ax.collections[0]
        old_XY = quiv.get_offsets()
        if not np.array_equal(old_XY, XY):
            # Positions have changed, create a new quiver
            replace = False
            quiv.remove()

    if replace and len(ax.collections) > 0:
        # Replace current quiver data
        quiv = ax.collections[0]
        quiv.set_UVC(U, V, C)

    else:
        # Make a new quiver

        # Determine scale based on the average distance between nearest neighbors
        tree = cKDTree(XY)
        min_dist = np.mean(tree.query(XY, k=[2])[0])
        scale = 1.15/min_dist if not np.isinf(min_dist) and min_dist != 0 else 1

        kwargs.setdefault('cmap', 'flatspin')
        kwargs.setdefault('scale', scale)
        kwargs.setdefault('pivot', 'middle')
        if arrows:
            kwargs.setdefault('width', 0.2/scale)
            kwargs.setdefault('headwidth', 3)
            kwargs.setdefault('headlength', 2)
            kwargs.setdefault('headaxislength', 2)
        else:
            kwargs.setdefault('width', 0.3/scale)
            kwargs.setdefault('headwidth', 0)
            kwargs.setdefault('headlength', 0)
            kwargs.setdefault('headaxislength', 0)

        if type(kwargs["cmap"]) is str and kwargs["cmap"].startswith("peem"):
            # clever peem colormap
            peem_angle = np.deg2rad(float(kwargs["cmap"].strip("peem")))
            intensity = np.cos(np.linspace(0, 2 * np.pi, 360) - peem_angle)
            intensity = intensity * 0.5 + 0.5  # scale from (-1,1) to (0,1)
            intensity = np.tile(intensity, (3, 1)).T  # [[0],...,[1]] -> [[0,0,0],...,[1,1,1]]
            kwargs["cmap"] = ListedColormap(intensity)
            ax.set_facecolor([0.5] * 3)


        quiv = ax.quiver(X, Y, U, V, C, units='xy',
                angles='xy', scale_units='xy', **kwargs)

        ax.set_aspect('equal')

        # Make space for the whole arrow
        xmin, xmax = np.min(X), np.max(X)
        ymin, ymax = np.min(Y), np.max(Y)
        ax.set_xlim(xmin - 1/scale, xmax + 1/scale)
        ax.set_ylim(ymin - 1/scale, ymax + 1/scale)

    return quiv

def plot_vector_image(XY, UV, mask_zero=True, replace=False, cmap='flatspin', ax=None):
    if mask_zero:
        UV = mask_zero_vectors(UV)

    U = UV[...,0] # x components
    V = UV[...,1] # y components
    C = vector_colors(U, V)

    cmap = plt.get_cmap(cmap)
    mag = norm(UV, axis=-1)
    alpha = mag

    # print(f'alpha {np.min(alpha)} {np.max(alpha)}')
    im = cmap(normalize_rad(C))
    im[:,:,-1] = alpha
    # print(f'im {im.shape} {im}')

    if ax is None:
        ax = plt.gca()

    if replace and len(ax.images) > 0:
        # Replace current image data
        ax.images[0].set_data(im)
        return ax.images[0]

    X = np.unique(XY[..., 0]) # x components
    Y = np.unique(XY[..., 1]) # y components
    Xi = np.arange(len(X))
    Yi = np.arange(len(Y))

    xmin, xmax = X.min(), X.max()
    ymin, ymax = Y.min(), Y.max()

    def format_coord(x, y):
        x = xmin + (xmax-xmin) * x / (im.shape[1] - 1)
        y = ymin + (ymax-ymin) * y / (im.shape[0] - 1)
        return f'x={x:g}, y={y:g}'

    ax.format_coord = format_coord
    nbins = min(len(Xi), 10)
    ax.xaxis.set_major_locator(ticker.FixedLocator(Xi, nbins=nbins))
    nbins = min(len(Yi), 10)
    ax.yaxis.set_major_locator(ticker.FixedLocator(Yi, nbins=nbins))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: "{:g}".format(X[int(x)]))))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: "{:g}".format(Y[int(y)]))))

    return ax.imshow(im, origin='lower')

def montage_fig(n_axes, title=False):
    """ Create a figure with n_axes subplots on a grid """
    n_rows = int(np.ceil(np.sqrt(n_axes)))
    n_cols = int(np.ceil(n_axes / n_rows))
    gs = dict(wspace=0.05, hspace=0.25, left=0.05, right=0.95, top=0.95, bottom=0.05)
    figsize = [6.4, 6.4]

    if title:
        gs.update(top=0.85) # todo: fixme

    fig, axes = plt.subplots(n_rows, n_cols, gridspec_kw=gs, figsize=figsize, squeeze=False)
    axes = axes.flatten()

    for ax in axes:
        ax.tick_params(
            top=False, bottom=False, left=False, right=False,
            labeltop=False, labelbottom=False, labelleft=False, labelright=False)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.grid(False)

    # hide unused axes
    for ax in axes[n_axes:]:
        ax.set_visible(False)

    return fig, axes

def vector_montage(axes, positions, vectors, labels=None, arrows=False, **kwargs):
    for i, (XY, UV, ax) in enumerate(zip(positions, vectors, axes)):
        if arrows:
            plot_vectors(XY, UV, arrows=arrows, replace=True, ax=ax, **kwargs)
        else:
            plot_vector_image(XY, UV, replace=True, ax=ax, **kwargs)

        if labels:
            ax.set_title(labels[i], size='x-small', pad=2)

def save_animation(ani, outfile, fps=30, dpi=100):
    base, ext = path.splitext(outfile)
    ext = ext.lstrip('.')

    if ext == 'mp4':
        print(f"Saving video {outfile}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, codec='h264', extra_args=['-crf', '0', '-g', '1'])
        ani.save(outfile, writer=writer, dpi=dpi)
        return

    if ext in animation.writers['imagemagick_file'].supported_formats:
        print(f"Saving image(s) {outfile}...")
        Writer = animation.writers['imagemagick_file']
        writer = Writer(fps=fps, extra_args=['-trim', '+repage'])
        ani.save(outfile, writer=writer, dpi=dpi)
        return

    if ext == 'gif':
        print(f"Saving GIF {outfile}...")
        Writer = animation.writers['imagemagick']
        writer = Writer(fps=fps)
        ani.save(outfile, writer=writer, dpi=dpi)
        return

    raise ValueError(f"Don't know how to write '{ext}', sorry")

def plot_h_ext(h_ext):
    h_ext = np.array(h_ext)

    # (time, 2): a global vector signal
    # (time, H, W, 2): a local vector signal on a grid
    assert h_ext.ndim == 2 or h_ext.ndim == 4

    if h_ext.ndim == 2:
        # (time, 2): a global vector signal
        plt.plot(h_ext[:,0], label="x")
        plt.plot(h_ext[:,1], label="y")
        plt.xlabel('t')
        plt.ylabel('h_ext')
        plt.legend()

    elif h_ext.ndim == 4:
        # (time, H, W, 2): a local vector signal on a grid
        nrows = h_ext.shape[1]
        ncols = h_ext.shape[2]
        fig = plt.gcf()
        axes = fig.subplots(nrows, ncols, squeeze=False, sharex=True, sharey=True)
        for row, col in np.ndindex((nrows, ncols)):
            ax = axes[row, col]
            j = nrows - row - 1
            i = col
            ax.text(.95, .95, f"({j},{i})", horizontalalignment='right',
                    verticalalignment='top', transform=ax.transAxes,
                    zorder=0)
            ax.plot(h_ext[:,j,i,0], label="x")
            ax.plot(h_ext[:,j,i,1], label="y")
            if i == 0:
                ax.set_ylabel('h_ext')
            else:
                ax.tick_params('y', labelleft=False)
            if j == 0:
                ax.set_xlabel('t')
            else:
                ax.tick_params('x', labelbottom=False)
            if (j, i) == (nrows - 1, ncols - 1):
                ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.05))
        plt.subplots_adjust(wspace=0, hspace=0)

def gridless_crop(x, crop_percent):
    """ Return the indices of x that are inside the crop """
    minx, maxx = np.min(x[:,0]), np.max(x[:,0])
    miny, maxy = np.min(x[:,1]), np.max(x[:,1])
    crop_width = ((np.array(crop_percent)/100).T * [maxy - miny, maxx - minx]).T
    return np.logical_and(
                np.logical_and(
                    x[:,0] >= minx + crop_width[1][0],
                    x[:,0] <= maxx - crop_width[1][1]
                ),
                np.logical_and(
                    x[:,1] >= miny + crop_width[0][0],
                    x[:,1] <= maxy - crop_width[0][1]
                )
    )

def rotate_points(x, y, theta):
    return x * np.cos(theta) - y * np.sin(theta), x * np.sin(theta) + y * np.cos(theta)

def plot_astroid(b=1, c=1, beta=3, gamma=3, hc=1, rotation=0, resolution=361,
        angle_range=(0, 2*np.pi), ax=None, **kwargs):

    thetas = np.linspace(angle_range[0], angle_range[1], resolution)

    h_par = b * np.cos(thetas)
    h_perp = c * (1 - ((h_par/b)**2)**(1/gamma))**(beta/2)
    h_perp[thetas>np.pi] *= -1

    h_par, h_perp = rotate_points(h_par, h_perp, np.deg2rad(rotation))

    if ax is None:
        ax = plt.gca()

    ax.axis('equal')

    return ax.plot(hc * h_par, hc * h_perp, **kwargs)
