#!/usr/bin/env python3

import time
import numpy as np
from asd.core.llg_simple import *
from asd.data_base.rectangular_cell_U4 import *
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *

nx=100
ny=36
latt,sites,neigh_idx[0],neigh_idx[1],neigh_idx[2] = rectangular_honeycomb_cell(nx,ny,1)
Bfield=np.array([0,0,0])
temp=0.5
dt=5e-4
n_log_conf=500
n_log_magn=100
nstep=400000
bm_radius=8
alpha=0.1


fmt_head='{:>12s} ' *3+'|'+'{:>12s} ' *3
fmt_log ='{:12.5f} '*3+'|'+'{:12.5f} '*3

if __name__=='__main__':
    comm,size,rank,node = mt.get_mpi_handles()
    sp_lat = np.zeros((nx,ny,nat,3))
    if not rank: sp_lat = init_random(sp_lat)
    sp_lat = comm.bcast(sp_lat)
    nsites = np.prod(sp_lat.shape[:-1])

    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,BL_SIA=[SIA],
    BL_exch = [exch_1,exch_2],
    BQ_exch = [bq_exch_2],
    exchange_in_matrix = True)

    
    if not rank: 
        print ('\n'+'='*80)
        print ('Energy (mev/site)'.center(36), '  | ','Used time (s)'.center(36))
        print ('{}'.format('-'*80))
        print (fmt_head.format(*tuple(['parallel_1','parallel_2','serial']*2)))
        print ('{}'.format('-'*80))

    for i in range(10):
        if not rank: sp_lat = init_random(sp_lat,verbosity=0)
        sp_lat = comm.bcast(sp_lat)

        stime = time.time()
        en_p1 = ham.mpi_calc_total_E_from_Jmat_1(sp_lat)/nsites
        t1 = time.time()-stime

        stime = time.time() 
        en_p2 = ham.mpi_calc_total_E_from_Jmat(sp_lat)/nsites
        t2 = time.time()-stime
        if not rank:
            stime = time.time()
            en_s = ham.calc_total_E(sp_lat)/nsites
            t3 = time.time()-stime
            print (fmt_log.format(en_p1,en_p2,en_s,t1,t2,t3))
            
    if not rank: print ('='*80)
