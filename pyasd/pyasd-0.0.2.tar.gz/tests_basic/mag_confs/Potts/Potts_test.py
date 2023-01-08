#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *

nx=20
ny=20
nz=1

latt,sites, = build_latt('square',nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]

def make_random_Potts_config(q=4):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,2))
    sp_lat = initialize_spin_lattice(sp_lat,'Potts_random',q)

    quiver_kws = dict(units='x',pivot='mid',scale=1,headlength=4,width=0.1)
    kws = dict(
    superlatt = np.dot(np.diag([nx,ny]),latt),
    title='Potts random spin with q = {}'.format(q),
    color_mapping='phi_full',
    colormap='rainbow_r',
    quiver_kws=quiver_kws,
    colorbar_shrink=0.3,
    scatter_size=30,
    show=True,
    )
    plot_spin_2d(sites_cart,sp_lat,**kws)

if __name__=='__main__':
    make_random_Potts_config(q=6)
