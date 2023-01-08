#!/usr/bin/env python3

from timeit import default_timer as timer
import numpy as np
from asd.core.llg_simple import *
from asd.core.geometry import build_latt
from asd.core.hamiltonian import *
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.shell_exchange import *

nx=120
ny=120
lat_type='square'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1)
Bfield=np.array([0,0,0])
S_values = np.array([1])
SIA = np.array([0.1])
nat = sites.shape[-2]

J1_iso = np.zeros((1,4))
J1_sym_xyz = np.random.random((1,4,3,3))
exch_1 = exchange_shell(neigh_idx[0], J1_iso, J1_sym_xyz, shell_name='BL_1NN')

J2_iso = np.zeros((1,4))
J2_sym_xyz = np.random.random((1,4,3,3))
exch_2 = exchange_shell(neigh_idx[1], J2_iso, J2_sym_xyz, shell_name='BL_2NN')

B1_sym_xyz = np.random.random((1,4,3,3))
bq_exch_1 = biquadratic_exchange_shell_general(neigh_idx[0], B1_sym_xyz, shell_name='BQ_1NN')


fmt_head='{:>12s} ' *2+'|'+'{:>12s} ' *2
fmt_log ='{:12.5f} '*2+'|'+'{:12.5f} '*2

if __name__=='__main__':
    sp_lat = np.zeros((nx,ny,nat,3))
    sp_lat = init_random(sp_lat)
    nsites = np.prod(sp_lat.shape[:-1])


    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,BL_SIA=[SIA],
    BL_exch = [exch_1,exch_2],
    BQ_exch = [bq_exch_1],
    exchange_in_matrix = True)

    print ('\n'+'='*60)
    print ('Energy (mev/site)'.center(24), ' | ','Used time (s)'.center(24))
    print ('{}'.format('-'*60))
    print (fmt_head.format(*tuple(['method_1','method_2']*2)))
    print ('{}'.format('-'*60))

    for i in range(10):
        sp_lat = init_random(sp_lat,verbosity=0)

        stime = timer()
        en_p1 = ham.calc_total_E_from_Jmat(sp_lat)/nsites
        t1 = timer()-stime

        stime = timer() 
        en_p2 = ham.calc_total_E_from_Jmat(sp_lat,use_new_method=True)/nsites
        t2 = timer()-stime

        np.testing.assert_allclose(en_p1, en_p2)
        print (fmt_log.format(en_p1,en_p2,t1,t2))
            
    print ('='*60)
