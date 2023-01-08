#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from asd.core.topological_charge import calc_topo_chg

nx=60
ny=40
nz=1

latt,sites, = build_latt('square',nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]

radius_list=np.arange(5,15,2)

def make_skyrmion(sites,latt,radius_list,winding=1):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,3))
    sp_lat[...,2] = 1.
    confs=[]
    tcs=[]
    idx=[]
    for radius in radius_list:
        sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,winding=winding)
        confs.append(sp_lat)
        tcs.append(calc_topo_chg(sp_lat,sites_cart))

    confs = np.array(confs)
    titles = np.array(['{}Skyrmion: Q={:10.5f}'.format({-1:'Anti-',0:'',1:'',2:'Bi-'}[winding],tc) for tc in tcs])
    quiver_kws = dict(units='x',pivot='mid',scale=0.5,headlength=4)
    anim_kws = dict(titles=titles,colorful_quiver=True,colormap='rainbow_r',quiver_kws=quiver_kws,colorbar_shrink=0.3)
    make_ani(sites_cart,confs,**anim_kws)

if __name__=='__main__':
    for winding in [-1,1,2]:
        make_skyrmion(sites,latt,radius_list,winding=winding)
        #make_skyrmion(sites,latt,radius_list[::-1],winding=winding)
