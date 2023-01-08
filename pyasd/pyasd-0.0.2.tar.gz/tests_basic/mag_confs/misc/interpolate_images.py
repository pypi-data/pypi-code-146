#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from scipy.spatial.transform import Rotation as RT

nx=60
ny=40
nz=1

latt,sites,neigh_idx,rotvecs = build_latt('square',nx,ny,nz)
nat=sites.shape[-2]
radius=8

pos1 = np.array([-20,0])
pos2 = np.array([ 20,10])

def make_skyrmion_images(sites,latt,radius,pos1,pos2,nimages=10,winding=1):
    sites_cart = np.dot(sites,latt)
    pos_list = np.zeros((nimages,2))
    for i in range(2): pos_list[:,i] = np.linspace(pos1[i],pos2[i],nimages)
    confs=np.zeros((nimages,nx,ny,nat,3),float)
    tcs=[]
    idx=[]

    for i,pos in enumerate(pos_list):
        sp_lat=np.zeros((nx,ny,nat,3))
        sp_lat[...,2] = 1.
        confs[i] = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,pos=pos,winding=winding)

    tcs = [calc_topo_chg(sites_cart,conf) for conf in confs]

    titles = np.array(['{}Skyrmion on track: Q={:10.5f}'.format({True:'Anti-',False:''}[winding<0],tc) for tc in tcs])
    quiver_kws = dict(units='x',pivot='mid',scale=0.8)
    make_ani(sites_cart,confs,titles=titles,colorful_quiver=True,quier_kws=quiver_kws,colormap='rainbow',colorbar_shrink=0.6)

make_skyrmion_images(sites,latt,radius,pos1,pos2,winding=1,nimages=20)
