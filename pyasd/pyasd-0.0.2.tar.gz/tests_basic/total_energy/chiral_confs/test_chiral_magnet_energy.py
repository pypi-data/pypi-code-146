#!/usr/bin/env python3


# this example test two ways of calculating total spin energy
# one is symmetric matrix + DMI
# the other is pure matrix exchange
# the results are consistent for all bimeron-containing configurations
#
# Shunhong Zhang 
# szhang2@ustc.edu.cn
# Jan 31, 2021

import numpy as np
from asd.core.hamiltonian import *
from asd.data_base.exchange_for_CrMnI6_rect import *
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.core.shell_exchange import *


# Important Note:
# this function is valid only for bilinear models
# if biquadratic terms exist then this function cannot be applied
def calc_total_energy_from_field(ham,sp_lat):
    assert ham._nshell_BQ==0,'calc_total_energy_from_field: BQ_exch should not be present'
    en=0
    nx,ny,nat = sp_lat.shape[:3]
    for idx0 in np.ndindex(nx,ny,nat):
        B_eff = ham.calc_local_B_eff_from_Jmat(sp_lat,idx0)
        en -= np.dot(sp_lat[tuple(idx0)],B_eff)*ham._S_values[idx0[-1]]
    en = en*muB
    return en

nx=40
ny=24
latt,sites,neigh_idx = rectangular_honeycomb_cell(nx,ny,1)
bm_radius=16

tags = ['radius','E_Jmat','E_sym_mat','E_from_field','consistency']
fmt = '{:16.8f} '*4 + '{:16b}'

ham = ham2_rc
ham._nshell_BQ=0
ham._BQ_exch=[]

if __name__=='__main__':
    sp_lat = np.zeros((nx,ny,nat,3),float)
    neigh_idx_all_1 = calc_neighbors_in_sp_lat(ham._BL_exch[0]._neigh_idx,sp_lat)
    neigh_idx_all_2 = calc_neighbors_in_sp_lat(ham._BL_exch[1]._neigh_idx,sp_lat)

    print (('{:>16s} '*5).format(*tuple(tags)))
    for bm_radius in range(8,16):
        sp_lat = np.zeros((nx,ny,nat,3),float)
        sp_lat = init_spin_latt_bimeron(sp_lat,latt,sites,bm_radius,bm_type='Bloch',display=False)
        en0 = ham.calc_total_E_from_Jmat(sp_lat)
        en1 = ham.calc_total_E_from_sym_mat(sp_lat)
        en2 = calc_total_energy_from_field(ham,sp_lat)
        print (fmt.format(bm_radius,en0,en1,en2,np.allclose(en0,en1)*np.allclose(en0,en2)))
