#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *

nx=15
ny=15
nz=1
radius1=4
radius2=4

latt,sites = build_latt('honeycomb',nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]
sites_cart = np.dot(sites,latt)

orig = np.array([nx,ny,0])/2.

radius_list=np.arange(5,15)
sp_lat=np.zeros((nx,ny,nat,3),float)
sp_lat[...,2] = 1.
sp_lat = create_meron(sp_lat,latt,sites,radius1,meron_type='Bloch',core_direction='dn',pos=np.array([1./3,2./3,0]))
#sp_lat = create_meron(sp_lat,latt,sites,radius1,meron_type='Bloch',core_direction='dn',pos=np.array([2./3,1./3,0])+orig)


pos_list = np.array( [[-nx/2.,-ny/2.],[-nx/2.,ny/2.],[nx/2.,-ny/2.],[nx/2.,ny/2.]] )
pos_list[:,0] -= nx/6
pos_list[:,1] += ny/6
#for pos in pos_list:
#    sp_lat = create_meron(sp_lat,latt,sites,radius2,bm_type='Bloch',pos=pos,core_direction='up',achiral=False)

sites_repeat = get_repeated_sites(sites,2,2)
sites_cart_repeat = np.dot(sites_repeat,latt)
sp_lat_repeat = get_repeated_conf(sp_lat,2,2)
sites_cart_repeat=np.swapaxes(sites_cart_repeat,0,1)
sp_lat_repeat=np.swapaxes(sp_lat_repeat,0,1)
quiver_kws = dict(scale=0.8,units='x',pivot='mid')

plot_spin_2d(sites_cart_repeat,sp_lat_repeat,show=True,scatter_size=30,quiver_kws=quiver_kws,color_mapping='Sy')
Q = calc_topo_chg(sp_lat,sites_cart)
print ('calculated Q = {:10.5f}'.format(Q))
