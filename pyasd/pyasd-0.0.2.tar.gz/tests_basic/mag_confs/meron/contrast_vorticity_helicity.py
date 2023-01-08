#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from asd.utility.colormaps_new import parula

nx=20
ny=20
nz=1

latt,sites = build_latt('square',nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]
radius=8
sites_cart = np.dot(sites,latt).reshape(-1,sites.shape[-1])

def make_skyrmion(sites,latt,radius_list,winding=1,vorticity=-1,helicity=0):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,3))
    sp_lat[...,2] = 1.
    sp_lat,sk_idx = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,sk_type='Neel',return_skyr_idx=True,winding=winding,vorticity=vorticity,helicity=helicity)
    return sp_lat


vorticity_list=[-1,1]
helicity_list=range(-1,3)
colormap='rainbow'

for winding in [-1,1]:
    conf = []
    titles = []
    fig,ax=plt.subplots(2,4,figsize=(10,5),sharex=True,sharey=True)
    ax0 = fig.add_subplot(1,1,1)
    #ax0.set_title('$Skyrmion\ defined\ by\ [Q, Q_v, Q_h]$')
    ax0.axis('off')
    #fig.subplots_adjust(top=0.8)

    for i,j in np.ndindex(2,4):
        vorticity=vorticity_list[i]
        helicity=helicity_list[j]
        sp_lat = make_skyrmion(sites,latt,radius,winding=winding,vorticity=vorticity,helicity=helicity)
        Q=calc_topo_chg(sp_lat,sites_cart)
        title = '[{:3.0f}, {:3.0f},{:3.0f}]'.format(Q,vorticity,helicity)
        titles.append(title)
        spins = sp_lat.reshape(-1,3)
        quiver_kws = dict(units='x',pivot='mid',scale=0.8,headwidth=8,cmap=colormap)
        ax_plot_quiver(ax[i,j],sites_cart,spins,quiver_kws=quiver_kws,colorful_quiver=False)
        ax[i,j].scatter(sites_cart[:,0],sites_cart[:,1],c=spins[:,2],cmap=colormap,marker='o',zorder=-1,s=20)
        ax_plot_framework(ax[i,j],sites,latt=latt)
        ax[i,j].set_title(title)
        ax[i,j].set_aspect('equal')
    ax[0,0].set_ylabel('Skyrmion: Q=-1')
    ax[1,0].set_ylabel('anti-skyrmion: Q=1')
    fig.tight_layout()
    plt.show()
    exit()
