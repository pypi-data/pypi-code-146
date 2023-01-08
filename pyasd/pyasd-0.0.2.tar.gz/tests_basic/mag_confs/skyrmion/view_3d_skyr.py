#!/usr/bin/env python

# we are still looking for a good tool
# to visualize skyrmions and other chial magnetic structures
# in 3D within the framework of python


import numpy as np
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *

nx=10
ny=10
nz=1

latt,sites = build_latt('square',nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]



def make_skyrmion(sites,latt,radius,winding=1):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,3))
    sp_lat[...,2] = 1.
    sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,winding=winding)

    #titles = np.array(['{}Skyrmion: Q={:10.5f}'.format({True:'Anti-',False:''}[winding<0],tc) for tc in tcs])
    plot_spin_3d(sites_cart,sp_lat)

radius=3
make_skyrmion(sites,latt,radius,winding=1)
