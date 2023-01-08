#!/usr/bin/env python

import numpy as np
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.utility.Swq import *
import itertools

lat_type = 'triangular'
nx=20
ny=20
latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False)
nat = sites.shape[2]
sp_lat_uc = regular_order(lat_type,'tetrahedra')
sp_lat = np.zeros((nx,ny,nat,3))

rx=range(0,nx,2)
ry=range(0,ny,2)
for i,j in itertools.product(rx,ry):
    sp_lat[i:i+2,j:j+2] = sp_lat_uc

sites_cart = np.dot(sites,latt)
Q=calc_topo_chg(sp_lat,sites_cart)
title = 'Q={:10.5f}'.format(Q)
quiver_kws = dict(scale=1.2,units='x',pivot='mid')
plot_spin_2d(sites_cart,sp_lat,scatter_size=5,show=True,quiver_kws=quiver_kws,title=title)


spins = sp_lat.reshape(-1,3)
nqx=100
nqy=100
qpt_cart = gen_uniform_qmesh(nqx,nqy,bound=4)
S_vector = calc_static_structure_factor(spins,sites_cart.reshape(-1,2),qpt_cart)
plot_struct_factor(qpt_cart,S_vector,scatter_size=2,nqx=nqx,nqy=nqy)
