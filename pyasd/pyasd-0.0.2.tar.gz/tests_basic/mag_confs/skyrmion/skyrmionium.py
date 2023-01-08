#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *

nx=30
ny=15
nz=1
nat=4

latt,sites = rectangular_honeycomb_cell(nx,ny,nz,return_neigh=False)
radius_list=np.arange(5,15)

def make_skyrmion(sites,latt,radius_list,winding=1):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,3))
    sp_lat[...,2] = 1.
    confs=[]
    tcs=[]
    idx=[]
    for radius in radius_list:
        sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,winding=winding,theta_cycle=2)
        confs.append(copy.copy(sp_lat))
        tcs.append(calc_topo_chg(sp_lat,sites_cart))

    confs = np.array(confs)
    titles = np.array(['{}{}Skyrmionium: Q={:10.5f}'.format({True:'Anti-',False:''}[winding<0],{-1:'',1:'',2:'Bi-'}[winding],tc) for tc in tcs])
    #titles=None

    anim_kws = dict(titles=titles,colorful_quiver=True,colormap='rainbow_r',colorbar_shrink=0.3)
    #anim_kws.update(savegif=True,gif_name='ani_{}'.format(winding),gif_dpi=100)
    make_ani(sites_cart,confs,**anim_kws)


for winding in [-1,1,2]:
    make_skyrmion(sites,latt,radius_list,winding=winding)
