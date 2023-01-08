#!/usr/bin/env python

# linear interpolation between to images (spin configurations)
# a test script of gneb
# not physical, just for fun

import numpy as np
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from scipy.spatial.transform import Rotation as RT

nx=20
ny=20
nz=1
latt,sites, = build_latt('square',nx,ny,nz,return_neigh=False)
nat=sites.shape[-2]

def interpolate_images(sites,latt,radius=8,winding=1,nimage=10):
    sites_cart = np.dot(sites,latt)
    sp_lat_init=np.zeros((nx,ny,nat,3))
    sp_lat_finl=np.zeros((nx,ny,nat,3))
    sp_lat_init[...,2] = 1.
    sp_lat_finl[...,2] = 1.
    sp_lat_init = init_spin_latt_skyrmion(sp_lat_init,latt,sites,radius,winding=winding)

    confs = np.zeros((nimage+1,nx,ny,nat,3))
    for ix,iy,iat in np.ndindex(nx,ny,nat):
        n1 = sp_lat_init[ix,iy,iat]
        n2 = sp_lat_finl[ix,iy,iat]
        vec = np.cross(n1,n2)
        norm = np.linalg.norm(vec)
        if norm: vec /= norm
        angle = np.arccos(np.dot(n1,n2))
        for ii in range(nimage+1):
            mat = RT.from_rotvec(vec*angle*ii/nimage).as_matrix()
            if abs(angle)<1e-2: confs[ii,ix,iy,iat] = n1
            else: confs[ii,ix,iy,iat] = np.dot(mat,n1)

    titles = ['Image {}/{}'.format(ii+1,nimage+1) for ii in range(nimage+1)]
    quiver_kws = dict(units='x',pivot='mid',scale=1,headlength=4)
    make_ani(sites_cart,confs,titles=titles,scatter_size=30,quiver_kws=quiver_kws)

if __name__=='__main__':
    interpolate_images(sites,latt)
