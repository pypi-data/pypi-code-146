#!/usr/bin/env python

import numpy as np
from asd.core.hamiltonian import spin_hamiltonian
from asd.core.shell_exchange import *
from asd.data_base.exchange_for_CrMnI6_U4 import *
from asd.core.geometry import build_latt, rectangular_honeycomb_cell, display_latt

# comparison between hexagonal and rectangular cells
def hex_vs_rec(ham_uc,ham_rc):
    sp_lat = np.zeros((1,1,2,3),float)
    #print ('{0}\nResults from hexagonal   cell\n{0}'.format('*'*50))
    #en_ref_uc = ham_uc.verbose_reference_energy(sp_lat)
    angles, MAE_uc = ham_uc.calculate_MAE(sp_lat)
 
    sp_lat = np.zeros((1,1,4,3),float)
    #print ('{0}\nResults from rectangular cell\n{0}'.format('*'*50))
    #en_ref_rc = ham_rc.verbose_reference_energy(sp_lat)
    angles, MAE_rc = ham_rc.calculate_MAE(sp_lat)
    np.testing.assert_allclose(MAE_uc, MAE_rc)
    print ('passed!\n\n')
 


# the primitive cell of  honeycomb lattice
prim_latt,prim_sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
nat=4

ham_uc = spin_hamiltonian(
S_values=S_values,
BL_SIA=[SIA],
BL_exch = [exch_1,exch_2,exch_3][:2],
BQ_exch = [bq_exch_1,bq_exch_2],
exchange_in_matrix = True,
)


latt,sites,neigh_idx = rectangular_honeycomb_cell(1,1,1)

S_values = np.repeat(S_values,2)
SIA = np.repeat(SIA,2)

J1_sym_xyz = np.tile(J1_sym_xyz,(2,1,1,1))
J2_sym_xyz = np.tile(J2_sym_xyz,(2,1,1,1))
J3_sym_xyz = np.tile(J3_sym_xyz,(2,1,1,1))

DM1_xyz = np.tile(DM1_xyz,(1,2,1)).reshape(nat,3,3)
DM2_xyz = np.tile(DM2_xyz,(1,2,1)).reshape(nat,6,3)
DM3_xyz = np.tile(DM3_xyz,(1,2,1)).reshape(nat,3,3)

exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, DM1_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, DM2_xyz, shell_name = '2NN')
exch_3 = exchange_shell( neigh_idx[2], J3_iso, J3_sym_xyz, DM3_xyz, shell_name = '3NN')

ham0_rc = spin_hamiltonian(
S_values=S_values,
BL_SIA=[SIA],
BL_exch = [exch_1,exch_2,exch_3][:2],
exchange_in_matrix = True,
)

ham0_rc_3NN = spin_hamiltonian(
S_values=S_values,
BL_SIA=[SIA],
BL_exch = [exch_1,exch_2,exch_3],
exchange_in_matrix = True,
)



BQ1 = np.repeat(BQ1,2)
bq_exch_1 = biquadratic_exchange_shell(neigh_idx[0],BQ1,'BQ_1NN')

BQ2 = np.repeat(BQ2,2)
bq_exch_2 = biquadratic_exchange_shell(neigh_idx[1],BQ2,'BQ_2NN')

BL_exch = [exch_1,exch_2,exch_3]
BQ_exch = [bq_exch_1,bq_exch_2]

ham_rc = build_ham(S_values,SIA,BL_exch,BQ_exch,nshell_bl=2,name='2_BL+scalar_BQ')

ham1_rc = build_ham(S_values,SIA,BL_exch,BQ_exch,nshell_bl=2,name='2NN_BL+scalar_BQ')

BQ_exch_a = copy.deepcopy(BQ_exch)
BQ_exch_a[1]._BQ *= 1.5
ham2_rc = build_ham(S_values,SIA,BL_exch,BQ_exch_a,nshell_bl=3,name='3NN_BL+scalar_BQ')
 
# a revised version of biquadratic exchange
# in form of (BQ_xy*S_ix*S_jx+BQ_xy*S_iy*S_jy+BQ_zz*S_iz*S_jz)**2
BQ_mat_1 = np.tile(BQ_mat_1,(2,1,1,1,1))
BQ_mat_1 = np.swapaxes(BQ_mat_1,0,1).reshape(4,6,3,3)
bq_exch_2_generic = biquadratic_exchange_shell_general(neigh_idx[1],BQ_mat_1,shell_name='BQ_matrix_2NN')
ham3_rc = build_ham(S_values,SIA,BL_exch,[bq_exch_2_generic],nshell_bl=2,name='BL_2NN+tensorial_BQ')

BQ_mat_2 = np.tile(BQ_mat_2,(2,1,1,1,1))
BQ_mat_2 = np.swapaxes(BQ_mat_2,0,1).reshape(4,6,3,3)
bq_exch_2_generic = biquadratic_exchange_shell_general(neigh_idx[1],BQ_mat_2,shell_name='BQ_matrix_2NN')
ham4_rc = build_ham(S_values,SIA,BL_exch,[bq_exch_2_generic],nshell_bl=3,name='BL_3NN+tensorial_BQ')


if __name__=='__main__':
    latt,sites,neigh_idx = rectangular_honeycomb_cell(3,2,1)
    #display_latt(latt,sites)
    hex_vs_rec(ham_uc,ham_rc)
    sp_lat = np.zeros((1,1,4,3))
    hams_rc = [ham4_rc,ham3_rc,ham2_rc,ham1_rc,ham0_rc,ham0_rc_3NN]
    for ii in range(6):
        print ('Comparing {} on hexagonal and rectangular lattices'.format(labels[ii]))
        hex_vs_rec(hams[ii],hams_rc[ii])
    #compare_hams_MAE(hams_rc,labels,MAE_dft=MAE_dft)
    #ham3_rc.map_MAE(sp_lat)
    #ham4_rc.map_MAE(sp_lat,show=True)
