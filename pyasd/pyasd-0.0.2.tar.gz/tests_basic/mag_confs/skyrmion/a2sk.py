#!/usr/bin/env python

#=================================
# This example demonstrates
# how to create multiple
# topological magnetic solitons
# in a single supercell
# some tricky use of function
# init_spin_latt_skyrmion
# is shown by the plots
# MIND the overlape of two 
# anti-biskyrmions (a2sk)
#==================================

import numpy as np
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.core.geometry import *
from asd.utility.spin_visualize_tools import *


nx=8
ny=8
radius=2.8


def build_multi_a2sk(nx,ny,radius,show=False):
    latt,sites = build_latt('triangular',nx,ny,1,return_neigh=False)
    nat = sites.shape[2]
    sites_cart = np.dot(sites,latt)

    sp_lat0 = np.zeros((nx,ny,nat,3))
    sp_lat1,idx1 = init_spin_latt_skyrmion(sp_lat0,latt,sites,radius,winding=-2,vorticity=1,helicity=1,center_pos=[-1.5,1.5],return_skyr_idx=True)
    sp_lat2,idx2 = init_spin_latt_skyrmion(sp_lat0,latt,sites,radius,winding=-2,vorticity=1,helicity=1,center_pos=[1.5,-1.5],return_skyr_idx=True)

    sp_lat = np.zeros((nx,ny,nat,3))
    sp_lat[...,2] = 1.
    for ii in idx1: sp_lat[tuple(ii)] = sp_lat1[tuple(ii)]
    for ii in idx2: sp_lat[tuple(ii)] = sp_lat2[tuple(ii)]

    Q=calc_topo_chg(sp_lat,sites_cart)
    print ('Q={:4.2f}'.format(Q))

    kwargs = dict(
    superlatt = np.dot(np.diag([nx,ny]),latt),
    show=False,
    scatter_size=30,
    quiver_kws=quiver_kws,
    colorbar_shrink=0.3,
    colorbar_axes_position=[0.1,0.2,0.02,0.25],
    colorbar_orientation='vertical')
    

    plot_spin_2d(sites_cart,sp_lat1,title='sp_lat: 1'  , **kwargs)
    plot_spin_2d(sites_cart,sp_lat2,title='sp_lat: 2'  , **kwargs)
    plot_spin_2d(sites_cart,sp_lat ,title='sp_lat: 1+2', **kwargs)

    if show: plt.show()
    return sp_lat

quiver_kws = dict(scale=1.2,units='x',pivot='mid')

if __name__=='__main__':
    build_multi_a2sk(nx,ny,radius,show=True)
