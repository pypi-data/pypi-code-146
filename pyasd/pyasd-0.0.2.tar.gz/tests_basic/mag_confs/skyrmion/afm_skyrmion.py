#!/usr/bin/env python

import numpy as np
from asd.utility.spin_visualize_tools import plot_spin_2d,write_ovf,gen_params_for_ovf
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.core.geometry import build_latt

lat_type='honeycomb'
nx=9
ny=9
nz=1
nat=2
latt,sites = build_latt(lat_type,nx,ny,nz,return_neigh=False)
nat=sites.shape[2]

skyr_radius=4

orig = np.array([nx,ny])/2
center_A = sites[nx//2,ny//2,0] - orig
center_B = sites[nx//2,ny//2,1] - orig

sp_lat = np.zeros((nx,ny,nat,3),float)
sp_lat[:,:,:1] = init_spin_latt_skyrmion(sp_lat[:,:,:1],latt,sites[:,:,:1],skyr_radius,sk_type='Bloch',init_FM='up',center_pos=center_A)
#sp_lat[:,:,1:] = init_spin_latt_skyrmion(sp_lat[:,:,1:],latt,sites[:,:,1:],skyr_radius,sk_type='Bloch',init_FM='dn',center_pos=center_B)
sp_lat[:,:,1] = -sp_lat[:,:,0]


sites_cart = np.dot(sites,latt)
quiver_kws = dict(scale=1.2,units='x',pivot='mid',headwidth=4,headaxislength=4)


spin_plot_kwargs = dict(show=True,
scatter_size=30,
title='honeycomb AFM-skyrmion',
latt=latt,quiver_kws=quiver_kws,
colorbar_shrink=0.3
)

plot_spin_2d(sites_cart,sp_lat,**spin_plot_kwargs)

Q1 = calc_topo_chg(sp_lat[:,:,0],sites_cart[:,:,0])
Q2 = calc_topo_chg(sp_lat[:,:,1],sites_cart[:,:,1])
Q = calc_topo_chg(sp_lat,sites_cart)

print ('Topological charge of sublattice A  = {:8.5f}'.format(Q1))
print ('Topological charge of sublattice B  = {:8.5f}'.format(Q2))
print ('Topological charge of bipartite lat = {:8.5f}'.format(Q))

add_desc = [
'Antiferromagnetic skyrmion',
'nx   = {:4d}'.format(nx),
'ny   = {:4d}'.format(ny),
'nz   = {:4d}'.format(nz),
'nat  = {:4d}'.format(nat)]
params = gen_params_for_ovf(nx,ny,nz,additional_desc=add_desc)

spins = np.swapaxes(sp_lat,0,1).reshape(-1,3)
write_ovf(params,spins,'AFM-SkX.ovf')
