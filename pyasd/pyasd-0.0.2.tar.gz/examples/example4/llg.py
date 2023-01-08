#!/usr/bin/env python

# this script is still under test

import numpy as np
from asd.core.log_general import log_general
from asd.core.topological_charge import *
from asd.core.hamiltonian import spin_hamiltonian
from asd.core.llg_simple import *
from asd.core.spin_configurations import *
from asd.core.geometry import build_latt
from asd.core.shell_exchange import *


nx=6
ny=6
nz=1
lat_type='honeycomb'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
nat=sites.shape[-2]

S_values=np.array([1,2])
SIA=np.array([0.5,0.5])
J1_iso = np.array([1,1])

exch_1 = exchange_shell( neigh_idx[0], J1_iso, shell_name = '1NN')

ham = spin_hamiltonian(
S_values=S_values,
BL_SIA=[SIA],
BL_exch=[exch_1],
iso_only=True)

log_handle = log_general(
n_log_conf=500,
n_log_magn=500,
log_topo_chg=True, 
tri_simplices = get_tri_simplices(np.dot(sites,latt)),
log_force=True,
)

kwargs = dict(
S_values=S_values,
alpha=0.3,
dt=1e-3,
nstep=20000,
lat_type=lat_type,
conv_ener=1e-8,
temperature=0,
log_handle = log_handle,
free_root=False,
)


if __name__=='__main__':
    sp_lat = np.zeros((nx,ny,nat,3))
    sp_lat = init_random(sp_lat)
    LLG = llg_solver(**kwargs)

    #log_time,log_ener,log_conf = LLG.mpi_llg_simulation(ham,sp_lat)
    log_time,log_ener,log_conf = LLG.mpi_llg_simulation_shared_memory(ham,sp_lat)


