#!/usr/bin/env python

#====================================
#
# initialize the spin lattice 
# with specific spin configurations
# 
# Shunhong Zhang
# szhang2@ustc.edu.cn
#
# Jan 24, 2021
#
#====================================

from __future__ import print_function
import numpy as np
from scipy.spatial.transform import Rotation as RT
from asd.core.geometry import find_pbc_shell
from asd.core.random_vectors import *
from asd.utility.head_figlet import *
import copy


def check_sp_lat_norm(sp_lat,verbosity=False,fil='ill_norm_sites.dat'):
    norm = np.linalg.norm(sp_lat,axis=-1)
    if verbosity:
        ill_idx = np.where(abs(norm-1)>1e-2)
        if len(ill_idx[0])>0:
            with open(fil,'w') as fw:
                for ii in range(len(ill_idx[0])):
                    for jj in range(len(ill_idx)):
                        fw.write('{:3d}'.format(ill_idx[jj][ii]))
                    fw.write('\n')
    assert np.max(abs(norm-1)) < 1e-2, '''\n
    Initial sp_lat invalid!
    We require that all sites all spin vector with norm 1
    Did you forget to initialize the spin configuration?
    max deviation of norm = {:10.5f}\n'''.format(np.max(abs(norm-1)))



# create "regular magnetic order" as elaborated in 
# Phys. Rev. B 83, 184401 (2011)
def regular_order(lat_type='triangular',order_name='tetrahedra'):
    from asd.core.geometry import build_latt
    if lat_type=='triangular':
        if order_name=='tetrahedra':
            latt,sites = build_latt(lat_type,2,2,1,return_neigh=False)
            sp_lat = np.zeros((2,2,1,3),float)
            sp_lat[0,0,0] = np.array([1,1,1])
            sp_lat[1,0,0] = np.array([-1,-1,1])
            sp_lat[0,1,0] = np.array([1,-1,-1])
            sp_lat[1,1,0] = np.array([-1,1,-1])
            sp_lat /= np.sqrt(3)

            # rotate so that one of the four spins points to [0,0,1]
            vec = np.array([1,-1,0])*np.arccos(1/np.sqrt(3))/np.sqrt(2)
            mat = RT.from_rotvec(vec).as_matrix()
            sp_lat = np.dot(sp_lat,mat.T)
    return sp_lat


def gen_regular_order_on_honeycomb_lattice(conf_name='FM'):
    magmom = np.zeros((2,2,2),float)
    if conf_name=='FM': 
        magmom[:,:,:] = 1.
    elif conf_name=='Neel-AFM':
        magmom[:,:,0]=1.
        magmom[:,:,1]=-1.
    elif conf_name=='zigzag-AFM':
        magmom[:,0] = 1.
        magmom[:,1] = -1.
    elif conf_name=='stripy-AFM':
        magmom[:,0,0] = 1.
        magmom[:,0,1] = -1.
        magmom[:,1,0] = -1.
        magmom[:,1,1] = 1.
    elif conf_name=='super-Neel-AFM':
        magmom[0,0,0] = 1.
        magmom[0,0,1] = -1.
        magmom[0,1,:] = 1.
        magmom[1,0,:] = -1.
        magmom[1,1,0] = 1.
        magmom[1,1,1] = -1.
    else:
        exit('magmom still under test')
    return magmom


def visualize_spin_conf(latt,sites,sp_lat,title='initial spin'):
    from asd.utility.spin_visualize_tools import plot_spin_2d,quiver_kws
    sites_cart = np.dot(sites,latt)
    nx,ny=sp_lat.shape[:2]
    superlatt=np.dot([[nx,0],[0,ny]],latt)
    quiver_kws.update(scale=1.5)
    kwargs=dict(title=title,
    show=True,scatter_size=20,save=True,
    superlatt=superlatt,quiver_kws=quiver_kws,
    colorbar_orientation='auto',
    colorbar_shrink=0.3)
    fig,ax,scat,qv,tl = plot_spin_2d(sites_cart,sp_lat,**kwargs)
    return fig,ax,scat,qv,tl


# here "center_pos" is the position of the skyrmion center relative to "origin", in fractional coordinate of latt, the unit cell lattice
def init_spin_latt_skyrmion(sp_lat,latt,sites,skyr_radius,sk_type="Neel",center_pos=np.zeros(3),orig=None,
    return_skyr_idx=False,use_pbc=True,display=False,ellipticity=1.0,
    winding=1.,vorticity=1,helicity=0,theta_power=1,theta_cycle=1,title='skyrmion',
    init_FM='up'):
    nx,ny,nat=sp_lat.shape[:3]
    if init_FM == 'up':
        sp_lat[...,:2]=0.
        sp_lat[...,2]=1.
    elif init_FM == 'dn':
        sp_lat[...,:2]=0.
        sp_lat[...,2]=-1.

    if orig is None: orig = np.array([nx,ny])/2
    rvec = np.dot(sites - orig - center_pos[:2], latt)
    if ellipticity<0: exit ('{}init_spin_latt_skyrmion: ellipticity should be positive'.format(err_text))
    rvec[...,1] *= ellipticity

    dist = np.linalg.norm(rvec,axis=-1)
    skyr_idx=np.array(np.where(dist<=skyr_radius)).T
    if use_pbc: skyr_idx,rvec = find_pbc_shell(sites,latt,skyr_radius,center_pos=center_pos,ellipticity=ellipticity,orig=orig)
    dist = np.linalg.norm(rvec,axis=-1)

    for (ix,iy,iat) in skyr_idx:
        theta = 1-np.power(dist[ix,iy,iat]/skyr_radius,theta_power)
        theta*= np.pi*theta_cycle
        phi = np.angle(rvec[ix,iy,iat,0] + 1.j*rvec[ix,iy,iat,1])
        if sk_type=='Bloch': helicity=1.
        psi = (phi*vorticity+helicity*np.pi/2)*winding
        sp_lat[ix,iy,iat,0] = np.sin(theta)*np.cos(psi)
        sp_lat[ix,iy,iat,1] = np.sin(theta)*np.sin(psi)
        sp_lat[ix,iy,iat,2] = np.cos(theta) 
        if init_FM in ['up','dn']: sp_lat[ix,iy,iat] *= {'up':1,'dn':-1}[init_FM]
    if display: visualize_spin_conf(latt,sites,sp_lat,title=title)
    if return_skyr_idx: return copy.copy(sp_lat),skyr_idx
    else: return copy.copy(sp_lat)


# here "center_pos" is the position of the bimeron center (mid point of vortex and anti-vortex) relative to "origin", in fractional coordinate
# "bm" represents bimeron
# "phi0" is the angle between the background in-plane FM and the x axis
def init_spin_latt_bimeron(sp_lat,latt,sites,bm_radius,bm_type="Neel",center_pos=np.zeros(3),orig=None,
    return_bm_idx=False,use_pbc=True,display=False,ellipticity=1.0,polarity=np.array([1,0,0]),winding=1.,vorticity=1.,helicity=0.,title='bimeron'):

    sp_lat,bm_idx = init_spin_latt_skyrmion(sp_lat,latt,sites,bm_radius,bm_type, center_pos, ellipticity = ellipticity,
    return_skyr_idx=True, use_pbc=use_pbc, winding=winding, vorticity=vorticity, helicity = helicity, orig=orig)

    rot = np.cross(np.array([0,0,1.]),polarity)
    rot*= np.linalg.norm(rot)*np.pi/2
    mat = RT.from_rotvec(rot).as_matrix()
    sp_lat = np.dot(sp_lat,mat.T)
    if display: visualize_spin_conf(latt,sites,sp_lat,title=title)
    if return_bm_idx: return copy.copy(sp_lat),bm_idx
    return copy.copy(sp_lat)


# here "center_pos" is the position of the skyrmion center relative to "origin", in fractional coordinate
def init_spin_latt_bimeron_2(sp_lat,latt,sites,bm_radius,bm_type="Neel",center_pos=np.zeros(3),orig=None,
    return_bm_idx=False,display=False,ellipticity=1.0,winding=1.,vorticity=1,helicity=0,theta_power=1,theta_cycle=1,title='bimeron',background=np.array([1,0,0])):
    nx,ny,nat=sp_lat.shape[:3]
    sp_lat = np.zeros_like(sp_lat)
    for i in range(3): sp_lat[...,i]=background[i]
    if orig is None: orig = np.array([nx,ny])/2
    rvec = np.dot(sites - orig - center_pos[:2], latt)
    if ellipticity<0: exit ('{}init_spin_latt_bimeron: ellipticity should be positive'.format(err_text))
    rvec[...,1] *= ellipticity

    dist = np.linalg.norm(rvec,axis=-1)
    bm_idx=np.array(np.where(dist<=bm_radius)).T
    phi0= np.angle(background[0] + 1.j*background[1])
    for (ix,iy,iat) in bm_idx:
        theta = 1-np.power(dist[ix,iy,iat]/bm_radius,theta_power)
        theta*= np.pi*theta_cycle
        phi = np.angle(rvec[ix,iy,iat,0] + 1.j*rvec[ix,iy,iat,1])
        if bm_type=='Bloch': helicity=1.
        psi = (phi*vorticity+helicity*np.pi/2)*winding
        sp_lat[ix,iy,iat,2] = -np.sin(theta)*np.cos(psi)
        sp_lat[ix,iy,iat,1] = -np.sin(theta)*np.sin(psi)
        sp_lat[ix,iy,iat,0] =  np.cos(theta)
    if display: visualize_spin_conf(latt,sites,sp_lat,title=title)
    if return_bm_idx: return copy.copy(sp_lat),bm_idx
    else: return copy.copy(sp_lat)


# the pbc implementation is still under test
def create_meron(sp_lat,latt,sites,meron_radius,meron_type="Neel",center_pos=np.zeros(3),orig=None,
    return_meron_idx=False,display=False,ellipticity=1.0,polarity=np.array([1,0,0]),
    core_direction='up',use_pbc=True,winding=1.,vorticity=1,helicity=0,theta_power=1,title='meron'):

    nx,ny,nat=sp_lat.shape[:3]
    orig = np.array([nx,ny])/2
    rvec = np.dot(sites - orig - center_pos[:2], latt)

    if ellipticity<0: exit ('{}meron generation: ellipticity should be positive'.format(err_text))
    rvec[...,1] *= ellipticity
    dist = np.linalg.norm(rvec,axis=-1)
    meron_idx=np.array(np.where(dist<=meron_radius)).T
    if use_pbc: meron_idx,rvec = find_pbc_shell(sites,latt,meron_radius,center_pos=center_pos,ellipticity=ellipticity,orig=orig)
    dist = np.linalg.norm(rvec,axis=-1)

    for (ix,iy,iat) in meron_idx:
        if core_direction=='up': theta = np.power(dist[ix,iy,iat]/meron_radius,theta_power)/2
        if core_direction=='dn': theta = (1-np.power(dist[ix,iy,iat]/meron_radius,theta_power)/2)
        theta *= np.pi

        phi = np.angle(rvec[ix,iy,iat,0] + 1.j*rvec[ix,iy,iat,1])
        if meron_type=='Bloch': helicity=1.
        psi = (phi*vorticity+helicity*np.pi/2)*winding
        sp_lat[ix,iy,iat,0] = np.sin(theta)*np.cos(psi)
        sp_lat[ix,iy,iat,1] = np.sin(theta)*np.sin(psi)
        sp_lat[ix,iy,iat,2] = np.cos(theta)

    if display: visualize_spin_conf(latt,sites,sp_lat,title=title)
    if return_meron_idx: return sp_lat,meron_idx
    else: return sp_lat


def show_vortex_latt(sites,latt,sp_lat,repeat_x=2,repeat_y=2,calc_Q=True):
    from asd.utility.spin_visualize_tools import plot_spin_2d,get_repeated_sites,get_repeated_conf,quiver_kws
    from asd.core.topological_charge import calc_topo_chg
    sites_cart = np.dot(sites,latt)
    sites_repeat = get_repeated_sites(sites,repeat_x,repeat_y)
    sites_cart_repeat = np.dot(sites_repeat,latt)
    sp_lat_repeat = get_repeated_conf(sp_lat,repeat_x,repeat_y)
    title = 'vortex-antivortex lattice'
    if calc_Q: title += ': Q ={:6.3f}'.format(calc_topo_chg(sp_lat,sites_cart))
    quiver_kws.update(width=0.1)
    plot_spin_2d(sites_cart_repeat,sp_lat_repeat,title=title,show=True,scatter_size=30,latt=latt,superlatt=None)


def build_square_meron_latt(nx=21,ny=21,nz=1,radius_vortex=8,radius_anti_vortex=4,repeat_x=2,repeat_y=2,show=False,calc_Q=False,theta_power=1):
    from asd.core.geometry import build_latt
    latt,sites = build_latt('square',nx,ny,nz,return_neigh=False)
    nat=sites.shape[-2]
    sp_lat=np.zeros((nx,ny,nat,3),float)
    sp_lat = create_meron(sp_lat,latt,sites,radius_anti_vortex,meron_type='Bloch',center_pos=np.array([nx/2,0]),core_direction='up',vorticity=-1,helicity=1,theta_power=theta_power)
    sp_lat = create_meron(sp_lat,latt,sites,radius_anti_vortex,meron_type='Bloch',center_pos=np.array([0,ny/2]),core_direction='up',winding=-1,helicity=1,theta_power=theta_power)
    sp_lat = create_meron(sp_lat,latt,sites,radius_vortex,meron_type='Bloch',core_direction='dn',center_pos=np.array([0,0,0]),vorticity=-1,winding=-1,theta_power=theta_power)
    sp_lat = create_meron(sp_lat,latt,sites,radius_vortex,meron_type='Bloch',center_pos=np.array([-nx,-ny,0])/2,core_direction='up',theta_power=theta_power)
    if show: show_vortex_latt(sites,latt,sp_lat,repeat_x,repeat_y,calc_Q=calc_Q)
    return sp_lat


def build_honeycomb_meron_latt(nx=15,ny=15,nz=1,radius_vortex=4.5,radius_anti_vortex=6,repeat_x=2,repeat_y=2,show=False,calc_Q=False,theta_power=1):
    from asd.core.geometry import build_latt
    latt,sites = build_latt('honeycomb',nx,ny,nz,return_neigh=False)
    nat=sites.shape[-2]
    sp_lat=np.zeros((nx,ny,nat,3),float)
    sp_lat = create_meron(sp_lat,latt,sites,radius_anti_vortex,meron_type='Bloch',center_pos=np.array([nx,ny])/2.,core_direction='up',winding=2,vorticity=-1,theta_power=theta_power)
    sp_lat = create_meron(sp_lat,latt,sites,radius_vortex,meron_type='Bloch',core_direction='dn',center_pos=np.array([-nx/6.,ny/6.]),theta_power=theta_power)
    sp_lat = create_meron(sp_lat,latt,sites,radius_vortex,meron_type='Bloch',center_pos=np.array([nx/6.,-ny/6.]),core_direction='up',vorticity=-1,winding=-1,theta_power=theta_power)
    if show: show_vortex_latt(sites,latt,sp_lat,repeat_x,repeat_y,calc_Q=calc_Q)
    return sp_lat


# here "center_pos" is the position of the skyrmion center relative to "origin", in fractional coordinate
def init_spin_latt_skyrmion_bubble(sp_lat,latt,sites,radius,dw_thickness,sk_type="Neel",center_pos=np.zeros(3),orig=None,
    return_skyr_idx=False,display=False,ellipticity=1.0,winding=1.,vorticity=1,helicity=0,theta_power=1,theta_cycle=1,title='skyrmion'):
    nx,ny,nat=sp_lat.shape[:3]
    sp_lat[...,:2]=0.
    sp_lat[...,2]=1.
    if orig is None: orig = np.array([nx,ny])/2
    rvec = np.dot(sites - orig - center_pos[:2], latt)
    assert ellipticity>0,'{}init_spin_latt_skyrmion: ellipticity should be positive'.format(err_text)
    assert radius>=dw_thickness, '{}radius should not be smaller than DW thickness!'.format(err_text)
    rvec[...,1] *= ellipticity

    dist = np.linalg.norm(rvec,axis=-1)
    dw_idx=np.array(np.where(np.logical_and(dist<=radius,dist>radius-dw_thickness))).T
    domain_idx = np.array(np.where(dist<=radius-dw_thickness)).T
    for (ix,iy,iat) in dw_idx:
        theta = 1-np.power((dist[ix,iy,iat]-(radius-dw_thickness))/dw_thickness,theta_power)
        theta*= np.pi*theta_cycle
        phi = np.angle(rvec[ix,iy,iat,0] + 1.j*rvec[ix,iy,iat,1])
        if sk_type=='Bloch': helicity=1.
        psi = (phi*vorticity+helicity*np.pi/2)*winding
        sp_lat[ix,iy,iat,0] = np.sin(theta)*np.cos(psi)
        sp_lat[ix,iy,iat,1] = np.sin(theta)*np.sin(psi)
        sp_lat[ix,iy,iat,2] = np.cos(theta)
    for (ix,iy,iat) in domain_idx: sp_lat[ix,iy,iat,2] = -1.
    if display: visualize_spin_conf(latt,sites,sp_lat,title=title)
    if return_skyr_idx: return copy.copy(sp_lat),skyr_idx
    else: return copy.copy(sp_lat)


random_conf_warning='''
Generating random spin configuration
Important Note: if you use parallel mode
Please make sure that the initial configuration is only generated
by one process and broadcast to all other processes
otherwise some unexpected disorder might occur
'''
 
def init_random(sp_lat,method='MultivarNormal',verbosity=1,q_for_Potts=3):
    if verbosity: print (random_conf_warning)
    shape = sp_lat.shape
    nn = np.prod(shape[:-1])
    spins = gen_random_spins_misc(nn,method,q_for_Potts)
    sp_lat = spins.reshape(shape)
    return sp_lat


# theta and phi0 in degree
# q_vector in reciprocal lattice (with the factor 2pi)
# ellipticity is only used for elliptic cones
# when it is 1 (default) the perfect circular cone is applied
def init_spin_spiral(sp_lat,latt,sites,q_vector,theta,phi0=0,axis=[0,0,1],ellipticity=1.0, display=False,title='spiral'):
    theta = np.deg2rad(theta)
    phi0  = np.deg2rad(phi0)
    nx,ny,nat=sp_lat.shape[:3]
    spins = np.zeros_like(sp_lat)

    for (ix,iy,iat) in np.ndindex(nx,ny,nat):
        q_phase = np.dot(sites[ix,iy,iat],q_vector[:sites.shape[-1]])
        spins[ix,iy,iat,0] = np.sin(theta)*np.cos(phi0 + q_phase)
        spins[ix,iy,iat,1] = np.sin(theta)*np.sin(phi0 + q_phase)
        spins[ix,iy,iat,2] = np.cos(theta)

    if np.allclose(axis,[0,0,1]): 
        sp_lat  = spins
    else:
        if np.allclose(axis,[1,0,0]):
            vv = np.array([[0,1,0],[0,0,1],[1,0,0]])
        elif np.allclose(axis,[0,1,0]):
            vv = np.array([[0,0,1],[1,0,0],[0,1,0]])
        else:
            vv = np.zeros((3,3))
            vv[2] = axis/np.linalg.norm(axis)
            if axis[2]>=0:   v = np.array([1,0,0])
            else:            v = np.array([0,1,0])
            vv[0] = v - np.dot(v,vv[2])*vv[2]
            vv[0]/= np.linalg.norm(vv[0])
            vv[1] = np.cross(vv[2],vv[0])

        for (ix,iy,iat) in np.ndindex(nx,ny,nat):
            sp_lat[ix,iy,iat] = np.dot(spins[ix,iy,iat],vv)
    if display: visualize_spin_conf(latt,sites,sp_lat,title=title)
    return sp_lat


def init_domain_wall(latt,sites,normal_vec=[1,0,0],width=4,center=[0.5,0.5,0],helicity=0,dw_type='',return_dw_idx=False):
    normal_vec /= np.linalg.norm(normal_vec)
    shape = sites.shape
    sp_lat = np.zeros((*tuple(shape[:-1]),3),float)
    ndim = latt.shape[1]
    superlatt = np.dot(np.diag(shape[:ndim]),latt)
    center = np.dot([0.5,0.5],superlatt)
    sites_cart = np.dot(sites,latt)
    dw_sites = []
    projs = np.dot(sites_cart-center,normal_vec[:ndim])
    dw_idx = np.where(abs(projs)<width/2)

    thetas = np.zeros(shape[:-1])
    thetas[projs>0]=0
    thetas[projs<0]=np.pi
    thetas[dw_idx] = (1-projs[dw_idx]/(width/2))*np.pi/2

    phi0 = helicity*np.pi/2
    if dw_type.lower()=='neel':  phi0 = 0
    if dw_type.lower()=='bloch': phi0 = np.pi/2
    phis = np.zeros(shape[:-1])
    phis[dw_idx] = np.angle(normal_vec[0]+1.j*normal_vec[1]) + phi0

    sp_lat[...,0] = np.sin(thetas)*np.cos(phis)
    sp_lat[...,1] = np.sin(thetas)*np.sin(phis)
    sp_lat[...,2] = np.cos(thetas)
    if return_dw_idx: return dw_idx,sp_lat
    else: return sp_lat


def initialize_spin_lattice(sp_lat,start_conf='as_input',q_for_Potts=3):
    ndim = sp_lat.shape[-1]
    if start_conf.lower() == 'random':  
        if ndim==3: sp_lat = init_random(sp_lat,verbosity=0)
        if ndim==2: sp_lat = init_random(sp_lat,method='XY_random',verbosity=0)
    if start_conf.lower() == 'potts_random':
        assert ndim==2, 'Potts random initialization requires ndim = 2! Now: ndim = {}'.format(ndim)
        sp_lat = init_random(sp_lat,method='Potts_random',q_for_Potts=q_for_Potts,verbosity=0)
    if start_conf.lower() == 'xfm':  sp_lat[...,:]= [1,0,0]
    if start_conf.lower() == 'yfm':  sp_lat[...,:]= [0,1,0]
    if start_conf.lower() == 'zfm':  sp_lat[...,:]= [0,0,1]
    return sp_lat


def load_conf_from_ovf(sp_lat,fil_ovf='final_spin_confs.ovf'):
    shape = sp_lat.shape
    from asd.core.shell_exchange import get_latt_idx
    from asd.utility.ovf_tools import parse_ovf
    nx,ny,nz,nat,idx = get_latt_idx(shape)
    params,spins = parse_ovf(fil_ovf,parse_params=False)
    if len(shape)==4: sp_lat = spins.reshape(ny,nx,nat,3)
    if len(shape)==5: sp_lat = spins.reshape(nz,ny,nx,nat,3)
    moveaxis = np.arange(len(shape)-2)
    sp_lat = np.moveaxis(sp_lat, moveaxis, moveaxis[::-1])
    return sp_lat


def display_chiral_magnetism_misc(nx=90,ny=24):
    from asd.core.geometry import build_latt, rectangular_honeycomb_cell
    from asd.utility.spin_visualize_tools import plot_spin_2d,quiver_kws
    #latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False)
    latt,sites = rectangular_honeycomb_cell(nx,ny,1,return_neigh=False)
    nat = sites.shape[-2]
    sites_cart = np.dot(sites,latt)

    hf = nx//2
    latt_hf,sites_hf = rectangular_honeycomb_cell(hf,ny,1,return_neigh=False)
    part1 =  init_domain_wall(latt_hf,sites_hf,width=8,normal_vec=np.array([ np.sqrt(3)/2,0.5]),center=[0.25,0.5])
    part2 = -init_domain_wall(latt_hf,sites_hf,width=8,normal_vec=np.array([ np.sqrt(3)/2,0.5]),center=[0.75,0.5],helicity=1)
 
    sp_lat = np.zeros((nx,ny,nat,3))
    sp_lat[:hf] = part1
    sp_lat[hf:] = part2

    mask_latt = np.array([[hf,0],[-hf/2,np.sqrt(3)*ny/2]])
    superlatt = np.dot(np.diag([nx,ny]),latt)
    centers = np.mgrid[-0.2:0.22:0.4,-0.3:0.35:0.6].reshape(2,-1).T
    centers = np.dot(centers,mask_latt)
    centers = np.dot(centers,np.linalg.inv(superlatt))
    centers = centers * np.array([nx,ny])
    sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,6,center_pos=centers[0],init_FM='none')
    sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,6,center_pos=centers[1],init_FM='none',helicity=1)
    sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,6,center_pos=centers[2],init_FM='none',vorticity=-1)
    sp_lat = init_spin_latt_skyrmion(sp_lat,latt,sites,6,center_pos=centers[3],init_FM='none',helicity=1,vorticity=-1)


    quiver_kws.update(scale=1)
    kwargs=dict(title='chiral magnetic structures',
    show=True,
    scatter_size=6,
    superlatt=np.dot([[nx,0],[0,ny]],latt),
    save=False,
    quiver_kws=quiver_kws,
    colorbar_orientation='vertical',
    colorbar_shrink=0.3,
    #colorful_quiver=True,
    figsize=(12,7))

    fig,ax,scat,qv,tl = plot_spin_2d(sites_cart,sp_lat,**kwargs)



if __name__=='__main__':
    print ('A script to generate spin configurations') 
    print ('Focus on topological magnetic structures such as skyrmions')
    display_chiral_magnetism_misc()
