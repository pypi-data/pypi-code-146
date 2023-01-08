#!/usr/bin/env python

import numpy as np
import glob
import pickle
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from asd.core.spin_configurations import gen_regular_order_on_honeycomb_lattice, init_random

lat_type='honeycomb'
nx=4
ny=4
latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False)

conf_names = ['stripy-AFM','super-Neel-AFM','Neel-AFM','zigzag-AFM','FM']
for conf_name in conf_names:
    sp_lat = np.zeros((nx,ny,2,3))
    magmom = gen_regular_order_on_honeycomb_lattice(conf_name)
    magmom = np.tile(magmom,(nx//2,ny//2,1))
    sp_lat[:,:,:,2] = magmom
    spins = np.swapaxes(sp_lat,0,1).reshape(-1,3)
    params = gen_params_for_ovf(nx,ny,2)
    write_ovf(params,spins,'conf_{}.ovf'.format(conf_name))
    plot_spin_2d(np.dot(sites,latt),sp_lat,show=True,scatter_size=100,
    superlatt=np.dot(np.diag([nx,ny]),latt),colorbar_shrink=0.3,title=conf_name)
    #pickle.dump(sp_lat,open('conf_{}.pickle'.format(conf_name),'wb'))

sp_lat = np.zeros((nx,ny,2,3))
sp_lat = init_random(sp_lat)
spins = np.swapaxes(sp_lat,0,1).reshape(-1,3)
params = gen_params_for_ovf(nx,ny,2)
nn = len(glob.glob('conf_random*ovf'))
fil = 'conf_random_{}.ovf'.format(nn+1)
write_ovf(params,spins,fil)
plot_spin_2d(np.dot(sites,latt),sp_lat,show=True,scatter_size=20,colorbar_shrink=0.3,title='random')
 
