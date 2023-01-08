#!/usr/bin/env python

import numpy as np
import pickle
from asd.core.random_vectors import *
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *


def get_instant_radius(clock,radius,lifetime):
    return np.sqrt(clock/lifetime)*radius


class particle():
    def __init__(self,radius,position,bloom_time,lifetime,winding):
        self._radius = radius
        self._position = position
        self._bloom_time = bloom_time
        self._lifetime = lifetime
        self._winding = winding

    def verbose_particle(self):
        print ('radius = {}'.format(self._radius))
        print ('center position = {}'.format(self._position))
        print ('bloom_time = {}'.format(self._bloom_time))
        print ('lifetime = {}'.format(self._lifetime))
        print ('winding number = {}'.format(self._winding))
 

    def snapshot(self,latt,sites,sp_lat,iframe,nframe,winding=1):
        local_clock = iframe - self._bloom_time
        kwargs = dict(center_pos=self._position,winding=self._winding,init_FM='none',orig=np.zeros(2))
        if 0 <= local_clock < self._lifetime:
            current_r = get_instant_radius(local_clock,self._radius,self._lifetime)
            sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,current_r,**kwargs)
            if local_clock>2:
                pre_r = get_instant_radius(local_clock-2,self._radius,self._lifetime)
                temp,skyr_idx = init_spin_latt_skyrmion(sp_lat,latt,sites,pre_r,return_skyr_idx=True,**kwargs)
                for idx in skyr_idx:  sp_lat[tuple(idx)] = np.array([0,0,1])
        return sp_lat


def gen_firework_params(nframe,n_sk,nx,ny,min_r,max_r,latest_bloom_time,min_lifetime,shift=np.zeros(2),max_winding=1):
    positions = np.random.randint(np.tile(np.array([nx,ny]),(n_sk,1))) + shift
    if n_sk == 1: positions = np.array([positions])[:,:2]
    radii = np.random.random(n_sk)*(max_r-min_r) + min_r
    bloom_times = np.random.randint(latest_bloom_time,size=n_sk)
    lifetimes = np.maximum(np.random.randint(nframe-bloom_times), min_lifetime)
    lifetimes = np.minimum(lifetimes, nframe-bloom_times-1)
    windings = np.random.randint(max_winding,size=n_sk)+1
    idx = np.argsort(bloom_times)
    return [item[idx] for item in (radii,positions,bloom_times,lifetimes,windings)]


def make_skyrmion_firework(sites,latt,radii,positions,windings=None,
    nframe=20,min_lifetime=4,latest_bloom_time=15,
    n_sk=10,dump=True):

    if windings is None: windings = np.ones_like(radii)
    nx,ny,nat = sites.shape[:3]
    bloom_times = np.random.randint(latest_bloom_time,size=n_sk)
    lifetimes = np.maximum(np.random.randint(nframe-bloom_times), min_lifetime)
    confs=np.zeros((nframe,nx,ny,nat,3))
    confs[...,2] = 1
    for ifm,isk in np.ndindex(nframe,n_sk):
        args = [item[isk] for item in (radii,positions,bloom_times,lifetimes,windings)]
        par = particle(*tuple(args))
        confs[ifm] = par.snapshot(latt,sites,confs[ifm],ifm,nframe)
    if dump: pickle.dump(confs,open('Firework_snapshots.pickle','wb'))
    return confs


def display_firework_snapshot(sites_cart,conf,savefig=False,show=True,title=None):
    quiver_kws = dict(units='x',pivot='mid',scale=0.5,headlength=4)
    kwargs = dict(colorful_quiver=True,colormap='rainbow_r',
    quiver_kws=quiver_kws,colorbar=False,title=title)
    fig,ax,scat,qv,tl = plot_spin_2d(sites_cart,conf,**kwargs)
    if savefig: fig.savefig('firework_snapshot',dpi=500)
    if show: plt.show()
    return fig


def collect_all_skrymions(latt,sites,radii,positions):
    nx,ny,nat = sites.shape[:3]
    sp_lat = np.zeros((nx,ny,nat,3))
    for ii,radius in enumerate(radii):
        kwargs = dict(center_pos=positions[ii],winding=1,init_FM='none',orig=np.zeros(2))
        sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,radius,**kwargs)
    plot_spin_2d(sites_cart,sp_lat,show=True,colorful_quiver=True,quiver_kws=quiver_kws,colorbar=False)



def make_firework_animation(sites_cart,confs=None,restart=False,savegif=False,set_title=False):
    if confs is None:
        if restart:  confs = pickle.load(open('Firework_snapshots.pickle','rb'))
        else:        exit('we need confs to generate animation!')
    if set_title==True: titles = ['t = {}'.format(ii) for ii in range(len(confs))]
    else: titles=None
    quiver_kws = dict(units='x',pivot='mid',scale=0.5,headlength=4)
    kwargs = dict(colorful_quiver=True,colormap='rainbow_r',
    quiver_kws=quiver_kws,colorbar=False,interval=2e2,
    savegif=savegif,gif_dpi=100,titles=titles)
    make_ani(sites_cart,confs,**kwargs)


nx=30
ny=int(round(nx/np.sqrt(3)))

latt,sites = rectangular_honeycomb_cell(nx,ny,nz,return_neigh=False)
sites_cart = np.dot(sites,latt)
nat = sites.shape[-2]

nframe=30
latest_bloom_time = 26
n_sk = 30
min_r = 4
max_r = 7
hollow=np.array([3/4,1/2])
hollow=np.zeros(2)
min_lifetime = 4
max_winding=1


restart=False
#restart=True

if __name__=='__main__':
    radii,positions,bloom_times,lifetimes,windings = \
    gen_firework_params(nframe,n_sk,nx,ny,min_r,max_r,latest_bloom_time,min_lifetime,shift=hollow)
    #collect_all_skrymions(latt,sites,radii,positions)
    
    kwargs = dict(nframe=nframe,
    latest_bloom_time=latest_bloom_time,
    n_sk=n_sk,windings=windings,
    dump=True)

    confs = make_skyrmion_firework(sites,latt,radii,positions,**kwargs)
    #for conf in confs: display_firework_snapshot(sites_cart,conf,savefig=False,show=True,title=None)
    make_firework_animation(sites_cart,confs,restart=restart,savegif=False,set_title=False)
