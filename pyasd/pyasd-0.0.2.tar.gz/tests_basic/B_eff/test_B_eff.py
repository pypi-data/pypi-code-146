#!/usr/bin/env python3

import numpy as np
from asd.core.hamiltonian import *
from asd.data_base.exchange_for_CrMnI6_rect import *
from asd.core.spin_configurations import init_random


fmt_head = '{:>5s} {:>18s} {:>18s} {:>15s} {:>15s} {:>25s}'
fmt='{:5d} {:18.8f} {:18.8f}       {}           [{:2d},{:2d},{:2d}]             {}'


def test_one_set(nx,ny,nat):
    sp_lat = np.zeros((nx,ny,nat,3),float)
    sp_lat = init_random(sp_lat,verbosity=0)
    ix=np.random.randint(nx)
    iy=np.random.randint(ny)
    iat=np.random.randint(nat)
    site_idx = (ix,iy,iat)
    en0 = ham.calc_total_E_from_Jmat(sp_lat)
    en1 = ham.calc_total_E_from_sym_mat(sp_lat)
    b0 = ham.calc_local_B_eff_from_Jmat(sp_lat,site_idx)
    b1 = ham.calc_local_B_eff_from_sym_mat(sp_lat,site_idx)
    print (fmt.format(i,en0,en1,np.allclose(en0,en1),ix,iy,iat,np.allclose(b0,b1)))


nx=40
ny=24
Bfield=np.array([0,0,0])

ham = spin_hamiltonian(
Bfield=Bfield,
S_values=S_values,
BL_SIA=[SIA],
BL_exch=[exch_1,exch_2],
BQ_exch=[bq_exch_2],
exchange_in_matrix = True)

ham = ham4_rc

if __name__=='__main__':
    print (fmt_head.format('case','E_Jmat','E_symmat','E_consistency','site index','B_eff_consistency'))
    for i in range(10): test_one_set(nx,ny,nat)
