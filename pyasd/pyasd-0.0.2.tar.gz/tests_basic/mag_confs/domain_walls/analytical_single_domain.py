#!/usr/bin/env python

# From Supplementary Information of
# Chang et al. Nat. Mater. (2020)

import numpy as np
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from asd.core.llg_simple import check_sp_lat_norm

nx=40
ny=40
nz=1
nat=1

d_in  = 30
d_out = 60
d_w = d_out - d_in

latt,sites,neigh_idx,rotvecs = build_latt('square',nx,ny,nz)
sites_cart = np.dot(sites,latt)
sp_lat = np.zeros((nx,ny,nat,3),float)

center = np.array([nx,ny])/2.

for ix,iy,iat in np.ndindex(nx,ny,nat):
    pos =  np.dot(sites[ix,iy,iat] - center,latt)
    rho = np.linalg.norm(pos)
    theta = np.pi*np.tanh((rho-d_in)/d_w)
    phi = np.angle(pos[0]+1.j*pos[1])
    s1 = np.sin(theta)
    c1 = np.cos(theta)
    s2 = np.sin(phi)
    c2 = np.cos(phi)
    sp_lat[ix,iy,iat] = np.array([s1*c2, s1*s2, c1])

plot_spin_2d(sites_cart,sp_lat,scatter_size=40,show=True)
