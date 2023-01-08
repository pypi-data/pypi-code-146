#!/usr/bin/env python

from __future__ import print_function
import numpy as np
from spirit import chain,state,geometry,configuration,hamiltonian,system,quantities,io
from asd.utility.ovf_tools import parse_ovf,gen_params_for_ovf,write_ovf
from asd.utility.spin_visualize_tools import make_ani
from asd.core.hamiltonian import *
from asd.core.geometry import *
from asd.core.spin_configurations import init_random
from asd.core.shell_exchange import get_exchange_xyz, exchange_shell, four_site_biquadratic_exchange_shell
from asd.core.llg_simple import *
from asd.core.log_general import *
import asd.mpi.mpi_tools as mt
import os


def get_Spirit_dataset(nx,ny,outdir,nimage=10,quiet=True):
    en_spirit=[]
    mgs=[]
    bounds = np.zeros((nimage,3),int)
    bound_cond = np.random.randint(2,size=(nimage,2))
    bounds[:,:2] = bound_cond
    with state.State('input.cfg',quiet) as p_state:
       chain.set_length(p_state,nimage)
       for idx in range(nimage):
            chain.jump_to_image(p_state,idx_image=idx)
            geometry.set_n_cells(p_state,[nx,ny,1])
            ix,iy = bound_cond[idx] 
            hamiltonian.set_boundary_conditions(p_state,[ix,iy,0])
            configuration.plus_z(p_state)
            if idx<10: configuration.skyrmion(p_state,radius=idx)
            else:      configuration.random(p_state)
            system.update_data(p_state)
            en0 = system.get_energy(p_state)
            mg0 = quantities.get_magnetization(p_state)
            en_spirit.append(en0)
            mgs.append(mg0)
            io.image_write(p_state,'confs/spin_{0}.ovf'.format(str(idx).zfill(2)))
            pos = geometry.get_positions(p_state)
    en_spirit = np.array(en_spirit)
    return en_spirit,mgs,bounds,pos



def test_one_lattice(outdir='honeycomb',nimage=30,nx=30,ny=30):
    lat_type=outdir
    latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1,latt_choice=1)
    nat=sites.shape[-2]

    if rank==0:
        print ('='*60)
        print ('Entering the following directory for testing:')
        print (outdir)
        print ('='*60+'\n\n')
    os.chdir(outdir)
    four_site = np.loadtxt('quadruplet',skiprows=2)

    S_values = np.ones(nat)*2
    SIA = [np.array([0.2]*nat),np.array([0.2]*nat),np.array([0.4]*nat)]
    SIA_axis = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]

    BQ = four_site[:,-1]
    BQs = np.array([BQ]*nat)
    neigh_idx = [ [[item[2+jj*4],item[3+jj*4],item[1+jj*4]] for jj in range(3)] for item in four_site]
    neigh_idx = [np.array(neigh_idx, int), [] ]
    bq_four_site = four_site_biquadratic_exchange_shell(neigh_idx, BQs, 'four-site-BQ')
     
    ham = spin_hamiltonian(S_values=S_values,
    BL_SIA=SIA,BL_SIA_axis=SIA_axis
    )
    ham.add_shell_exchange(bq_four_site,'general')

    sp_lat = np.zeros((nx,ny,nat,3))
    if rank==0:
        if os.path.isdir('confs'): os.system('rm -rf confs')
        os.mkdir('confs')

    log_handle = log_general(
    n_log_conf=1000,
    n_log_magn=1000,
    log_topo_chg=False,
    log_file='LLG.out',
    )

    llg_kws = dict(
    S_values=S_values,
    alpha=0.1,
    dt=1e-3,
    nstep=100000,
    temperature=0,
    lat_type=lat_type,
    conv_ener=1e-8,
    log_handle = log_handle,
    start_conf='random')

    LLG = llg_solver(**llg_kws)
    log_time,log_ener,log_conf = LLG.mpi_llg_simulation_shared_memory(ham,sp_lat)

    os.chdir('..')


nx=2
ny=2
lat_type='triangular'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1,latt_choice=1)
nat=sites.shape[-2]


if __name__=='__main__':
    test_one_lattice('triangular',nx=2,ny=2)
    #test_one_lattice('honeycomb')
