#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.utility.Swq import *
from asd.core.geometry import *
import matplotlib.pyplot as plt
import asd.mpi.mpi_tools as mt

r3h=np.sqrt(3)/2

def make_conf(sites,latt,radius,winding=1,name='skyrmion'):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,3))
    if name == 'skyrmion':
        sp_lat[...,2] = 1.
        sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,winding=winding,helicity=1,display=False)
    elif name == 'bimeron':
        sp_lat[...,0] = 1.
        sp_lat = init_spin_latt_bimeron(sp_lat,latt,sites,radius,winding=winding,helicity=1,display=False)
    return sp_lat


def calc_struct_factor(sites,latt,sp_lat,repeat_x=8,repeat_y=8,nqx=60,nqy=60):
    spins = get_repeated_conf(sp_lat,repeat_x,repeat_y).reshape(-1,3)
    sites_repeat = get_repeated_sites(sites,repeat_x,repeat_y)
    sites_cart_repeat = np.dot(sites_repeat,latt).reshape(-1,2)
    qpt_cart = gen_uniform_qmesh(nqx,nqy,bound=1)
    S_vector = mpi_calc_static_structure_factor(spins,sites_cart_repeat,qpt_cart)
    if not rank: fig,ax = plot_struct_factor(qpt_cart,S_vector,scatter_size=2,align='horizontal',nqx=nqx,nqy=nqy)



nx=15
ny=15
nz=1
lat_type='square'
lat_type='honeycomb'
latt,sites= build_latt(lat_type,nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]
radius=7
sp_lat = np.zeros((nx,ny,nat,3))

conf_name = 'skyrmion'
#conf_name = 'bimeron'

comm,size,rank,node = mt.get_mpi_handles()
if not rank: sp_lat = make_conf(sites,latt,radius,name = conf_name)
sp_lat = comm.bcast(sp_lat)
calc_struct_factor(sites,latt,sp_lat)
