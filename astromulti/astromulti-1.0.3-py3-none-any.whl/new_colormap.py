import matplotlib.pyplot as plt, numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from colorspacious import cspace_converter

def make( colors=None, nodes=None, palette="fire", lightnessplotfile=None ):
    '''
    Best to use colormaps from colorcet: https://github.com/holoviz/colorcet
    Use this tool only if you know very well what you are plotting.
    ---
    Makes a new colormap and optionally plots the lightness profile
    Default values of colors and nodes are for "fire" colors
    - "colors" must be a list of names of colors known to matplotlib.
    - "nodes" must be from 0. to 1. and correspond to colors.
    - "palette" must be either "fire"/"hubble"/"kindlmann".
    - give only colors+nodes or palette.
      If both are given, colors+nodes takes precedence.
    Important things to keep in mind while designing colormaps:
    - grayscale conversion (printing B&W)
    - lightness and perception
    - sequential or diverging or cyclic
    - 'hubble' palette is not recommended for single data images
    '''
    if colors is None:
        # only palette name is given
        if palette=='fire':
            colors = ["black","maroon","yellow","white"]
            nodes  = [  0.0,    0.1,     0.5,    1.0]
        elif palette=='hubble':
            colors = ["black","orange","skyblue","white"]
            nodes  = [  0.0,    0.2,     0.5,    1.0]
        elif palette=='kindlmann':
            colors = ["black","navy","limegreen","yellow","white"]
            nodes  = [  0.0,    0.2,    0.4,        0.7,    1.0]
        else:
            raise RuntimeError('Palette name not recognized.')
    newcmap1 = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
    if lightnessplotfile:
        rgb = cm.get_cmap(newcmap1)(np.linspace(0.,1.,100))[np.newaxis,:,:3]
        lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
        if palette is not None:
            plt.plot(lab[0,:,0],label=palette)
            plt.legend()
        else:
            plt.plot(lab[0,:,0])
        plt.xlabel('position on cmap in %')
        plt.ylabel('lightness')
        plt.savefig(lightnessplotfile)
    return newcmap1


def plot_all_lightness(plotfilepath='lightnessplots.png'):
    _=make(palette='fire',lightnessplotfile=plotfilepath)
    _=make(palette='hubble',lightnessplotfile=plotfilepath)
    _=make(palette='kindlmann',lightnessplotfile=plotfilepath)

