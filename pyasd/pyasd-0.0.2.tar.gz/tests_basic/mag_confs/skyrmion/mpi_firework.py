#!/usr/bin/env python

import numpy as np
import pickle
from asd.core.geometry import *
import asd.mpi.mpi_tools as mt
from firework import *


def mpi_make_skyrmion_firework(sites,latt,radii,positions,bloom_times,life_times,windings=None,
    nframe=20,
    n_sk=10,
    dump=True):

    if windings is None: windings = np.ones_like(radii)
    comm,size,rank,node = mt.get_mpi_handles()
    nx,ny,nat = sites.shape[:3]
    start, last = mt.assign_task(nframe,size,rank)
    confs=np.zeros((last-start,nx,ny,nat,3))
    confs[...,2] = 1
    for isk in range(n_sk):
        par = particle(radii[isk],positions[isk],bloom_times[isk],lifetimes[isk],windings[isk])
        for ifm in range(start,last): confs[ifm-start] = par.snapshot(latt,sites,confs[ifm-start],ifm,nframe)
    confs = comm.allgather(confs)
    confs = np.concatenate(confs,axis=0)
    if not rank and dump: pickle.dump(confs,open('Firework_snapshots.pickle','wb'))
    return confs

nx=60
ny=int(round(nx/np.sqrt(3)))
nframe=40
latest_bloom_time = 35

latt,sites = rectangular_honeycomb_cell(nx,ny,nz,return_neigh=False)
#latt,sites = build_latt('square',80,80,1,return_neigh=False)
sites_cart = np.dot(sites,latt)

min_r = 3
max_r = 12
n_sk = 50
min_lifetime=4

comm,size,rank,node = mt.get_mpi_handles()
if not rank:
    positions,radii,bloom_times,lifetimes,windings = gen_firework_params(nframe,n_sk,
    nx,ny,min_r,max_r,latest_bloom_time,min_lifetime,
    shift=hollow)
else:
    positions = np.zeros((n_sk,2),float)
    radii = np.zeros(n_sk,float)
    bloom_times = np.zeros(n_sk,float)
    lifetimes = np.zeros(n_sk,float)
    windings = np.zeros(n_sk,int)

positions = comm.bcast(positions)
radii = comm.bcast(radii)
bloom_times = comm.bcast(bloom_times)
lifetimes = comm.bcast(lifetimes)
windings = comm.bcast(windings)


if __name__=='__main__':
    kwargs = dict(nframe=nframe,
    n_sk=n_sk,
    windings=None,
    dump=True)

    confs = mpi_make_skyrmion_firework(sites,latt,radii,positions,bloom_times,lifetimes,**kwargs)
    kws = dict(
    restart=False,
    savegif=False,
    )
    if not rank:  make_firework_animation(sites_cart,confs,**kws)
    #if not rank: display_firework_snapshot(sites_cart,confs[8])
