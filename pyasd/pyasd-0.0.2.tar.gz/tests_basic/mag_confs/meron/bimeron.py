#!/usr/bin/env python

import numpy as np
from asd.core.spin_configurations import *
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *


def skyrmion_to_bimeron(nx=20,ny=20,radius=8,nn=10):
    from scipy.spatial.transform import Rotation as RT
    latt,sites = build_latt('square',nx,ny,1,return_neigh=False)
    sp_lat = np.zeros((nx,ny,1,3),float)
    sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,radius)
    confs = np.zeros((nn,nx,ny,1,3))
    for i,theta in enumerate(np.linspace(0,np.pi/2,nn)):
        mat = RT.from_rotvec([0,theta,0]).as_matrix()
        confs[i] = np.dot(sp_lat,mat.T)
    sites_cart = np.dot(sites,latt)
    quiver_kws = dict(units='x',pivot='mid',scale=1,headlength=4,width=0.1)
    make_ani(sites_cart,confs,quiver_kws=quiver_kws,scatter_size=40,savegif=True,gif_name='Sk2Bm',colorbar_shrink=0.4)
    return confs
    


def build_bimeron_latt(sites,latt,radius,winding=1,vorticity=1,helicity=0):
    sites_cart = np.dot(sites,latt)
    sp_lat=np.zeros((nx,ny,nat,3))
    sp_lat[...,2] = 1.

    #sp_lat = init_spin_latt_bimeron(sp_lat,latt,sites,radius,bm_type='Neel',winding=winding,vorticity=vorticity,helicity=helicity)
    sp_lat = init_spin_latt_bimeron_2(sp_lat,latt,sites,radius,bm_type='Neel',winding=winding,vorticity=vorticity,helicity=helicity)

    return sp_lat


def show_bimeron(latt,sites,winding_list,vorticity_list,helicity_list):
    for winding in winding_list:
        conf = []
        titles = []
        fig,ax=plt.subplots(2,4,figsize=(10,5),sharex=True,sharey=True)

        for i,j in np.ndindex(2,4):
            vorticity=vorticity_list[i]
            helicity=helicity_list[j]
            sp_lat = build_bimeron_latt(sites,latt,radius,winding=winding,vorticity=vorticity,helicity=helicity)

            params = gen_params_for_ovf(nx,ny,1)
            spins = np.swapaxes(sp_lat,0,1).reshape(-1,3)
            write_ovf(params,spins,'bimeron_{}_{}_{}.ovf'.format(winding,vorticity,helicity))

            Q=calc_topo_chg(sp_lat,sites_cart)
            title = '[{:3.0f}, {:3.0f},{:3.0f}]'.format(Q,vorticity,helicity)
            titles.append(title)
            spins = sp_lat.reshape(-1,3)
            quiver_kws = dict(units='x',pivot='mid',scale=0.8,headwidth=8,cmap=colormap)
            ax_plot_quiver(ax[i,j],sites_cart,spins,colorful_quiver=False,quiver_kws=quiver_kws)
            ax[i,j].scatter(sites_cart[:,0],sites_cart[:,1],c=spins[:,2],cmap=colormap,marker='o',zorder=-1,s=20)
            ax_plot_framework(ax[i,j],sites,latt=latt)
            ax[i,j].set_title(title)
            ax[i,j].set_aspect('equal')
        ax[0,0].set_ylabel('bimeron: Q=-1')
        ax[1,0].set_ylabel('anti-bimeron: Q=1')
        fig.tight_layout()
        plt.show()


skyrmion_to_bimeron()
exit()

nx=12
ny=12
nz=1


winding_list=[-1,1]
vorticity_list = [-1,1]
helicity_list = range(-1,3)
colormap='rainbow'

lat_type='honeycomb'
lat_type='square'
latt,sites = build_latt(lat_type,nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]
radius=5
sites_cart = np.dot(sites,latt).reshape(-1,sites.shape[-1])

show_bimeron(latt,sites,winding_list,vorticity_list,helicity_list)
