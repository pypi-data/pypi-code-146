#!/usr/bin/env python

import numpy as np
from asd.core.geometry import *
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.shell_exchange import *
from asd.core.hamiltonian import *
from asd.core.llg_simple import *
import matplotlib.pyplot as plt
import asd.mpi.mpi_tools as mt

lat_type='triangular'
nx = 4
ny = 4
data = build_latt(lat_type,nx,ny,1,latt_choice=1)
latt,sites,neigh_idx,rotvecs = data
nat = sites.shape[-2]

sp_lat = np.zeros((nx,ny,nat,3))


J1 = np.ones(1)
J2 =-np.ones(1)*3
J3 = np.ones(1)*3
S_values = np.ones(1)

comm,size,rank,node = mt.get_mpi_handles()

exch_1 = exchange_shell(neigh_idx[0], J1, shell_name='J1')
exch_2 = exchange_shell(neigh_idx[1], J2, shell_name='J2')
exch_3 = exchange_shell(neigh_idx[2], J3, shell_name='J3')
ham = spin_hamiltonian(S_values = S_values, BL_SIA=[np.zeros(1)],
BL_exch = [exch_1,exch_2,exch_3], iso_only=True)

if __name__=='__main__':
    if rank==0:
        sp_lat0 = regular_order(lat_type,'tetrahedra')
        en = ham.calc_total_E(sp_lat0)/np.prod(sp_lat0.shape[:-1])
        print ('En of tetrahedra configuration: {:8.4f} meV/site\n'.format(en))
        print ('Next we will perform LLG simulations to relax a randomly generated configuration')
        print ('We wil show that it robustly converges to the tetrahedra configuration')
        print ('which might differ from the standard tetrahedra config by a rotation')
        print ('but has the same energy\n\n')

    if rank==0: sp_lat = init_random(sp_lat,verbosity=0)
    sp_lat = comm.bcast(sp_lat,root=0)

    LLG = llg_solver(S_values=S_values,alpha=0.1,dt=1e-3,nstep=10000,
    conv_ener = 1e-10,
    n_log_magn = 100, n_log_conf=500, log_topo_chg=True, latt=latt, sites=sites, log_file = 'LLG.out')

    log_time,log_ener,sp_lat= LLG.mpi_llg_simulation(ham,sp_lat)
