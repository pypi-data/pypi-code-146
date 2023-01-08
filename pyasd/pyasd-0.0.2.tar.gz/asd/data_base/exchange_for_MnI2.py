#!/usr/bin/env python

import numpy as np
from asd.core.shell_exchange import get_exchange_xyz,exchange_shell
from asd.core.geometry import build_latt,show_neighbors
from scipy.spatial.transform import Rotation as RT

lat_type='triangular'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,1,1,1)


S_values = np.array([5./2])

SIA = - np.array([-0.0032])*S_values**2

J1_iso = np.zeros(1)
J2_iso = np.zeros(1)
J3_iso = np.zeros(1)


J1_sym = - np.array([
[   -0.0432 ,    0.0000 ,    0.0000 ],
[    0.0000 ,   -0.0544 ,    0.0104 ],
[    0.0000 ,    0.0104 ,   -0.0528 ]])

J2_sym = -np.array([
[   0.0172, -0.0008, 0.0000],
[  -0.0008,  0.0180, 0.0000],
[   0.0000,  0.0000, 0.0196]])

J3_sym = -np.array([
[   0.0376,  0.0000, 0.0000],
[   0.0000,  0.0369, 0.0008],
[   0.0000,  0.0008, 0.0368]])

J1_sym = np.array([J1_sym])*S_values[0]**2
J2_sym = np.array([J2_sym])*S_values[0]**2
J3_sym = np.array([J3_sym])*S_values[0]**2

# important change: the adjacent bonds subject to a mirror symmetry
# not a 180 degree rotation, so rotvecs[0] (see above) is wrong here
mat1 = RT.from_rotvec(np.array([0,0,2/3.])*np.pi).as_matrix()
mat2 = RT.from_rotvec(np.array([0,0,4/3.])*np.pi).as_matrix()

J1_sym_xyz = np.zeros((1,6,3,3),float)
J1_sym_xyz[0,0] = J1_sym[0]
J1_sym_xyz[0,2] = np.dot(np.dot(mat1,J1_sym[0]) , mat1.T)
J1_sym_xyz[0,4] = np.dot(np.dot(mat2,J1_sym[0]) , mat2.T)
J1_sym_xyz[0,3] = J1_sym[0]
J1_sym_xyz[0,3,0] *= -1
J1_sym_xyz[0,3,:,0] *= -1
J1_sym_xyz[0,1] = np.dot(np.dot(mat2,J1_sym[0]) , mat2.T)
J1_sym_xyz[0,5] = np.dot(np.dot(mat1,J1_sym[0]) , mat1.T)

J2_sym_xyz = get_exchange_xyz(J2_sym, rotvecs[1])

J3_sym_xyz = np.zeros((1,6,3,3),float)
J3_sym_xyz[0,0] = J3_sym[0]
J3_sym_xyz[0,2] = np.dot(np.dot(mat1,J3_sym[0]) , mat1.T)
J3_sym_xyz[0,4] = np.dot(np.dot(mat2,J3_sym[0]) , mat2.T)
J3_sym_xyz[0,3] = J3_sym[0]
J3_sym_xyz[0,3,0]   *= -1
J3_sym_xyz[0,3,:,0] *= -1
J3_sym_xyz[0,1] = np.dot(np.dot(mat2,J3_sym[0]) , mat2.T)
J3_sym_xyz[0,5] = np.dot(np.dot(mat1,J3_sym[0]) , mat1.T)


exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, shell_name = '2NN')
exch_3 = exchange_shell( neigh_idx[2], J3_iso, J3_sym_xyz, shell_name = '3NN')


def build_ham(Bfield=np.zeros(3)):
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,BL_SIA=[SIA],
    BL_exch=[exch_1,exch_2,exch_3],
    exchange_in_matrix=True)
    return ham


def build_modified_ham(exch_1,exch_2,exch_3,Bfield=np.zeros(3),iso_shell=[1,2,3]):

    if set(iso_shell)=={1,2,3}: 
        iso_only=True; mat = False
        J1_iso = np.array([J1_sym[0].trace()])
        exch_1 = exchange_shell( neigh_idx[0], J1_iso, shell_name = '1NN')
        J2_iso = np.array([J2_sym[0].trace()])
        exch_2 = exchange_shell( neigh_idx[1], J2_iso, shell_name = '2NN')
        J3_iso = np.array([J3_sym[0].trace()])
        exch_3 = exchange_shell( neigh_idx[2], J3_iso, shell_name = '3NN')

    else:
        iso_only=False; mat = True
        mm = np.tile(np.eye(3),(1,6,1,1))
        if 1 in iso_shell:
            J1_iso = np.zeros(1)
            J1_sym_xyz = J1_sym[0].trace()/3 * mm
            exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, shell_name = '1NN')
        if 2 in iso_shell:
            J2_iso = np.zeros(1)
            J2_sym_xyz = J2_sym[0].trace()/3 * mm
            exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, shell_name = '2NN')
        if 3 in iso_shell:
            J3_iso = np.zeros(1)
            J3_sym_xyz = J3_sym[0].trace()/3 * mm
            exch_3 = exchange_shell( neigh_idx[2], J3_iso, J3_sym_xyz, shell_name = '3NN')


    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,BL_SIA=[SIA],
    BL_exch=[exch_1,exch_2,exch_3],
    iso_only=iso_only,exchange_in_matrix=mat)
    return ham



if __name__=='__main__':

    latt,sites,neigh_idx,rotvecs = build_latt(lat_type,5,5,nz)
    show_neighbors(latt,sites,neigh_idx)

    print ('exchange interactions for MnI2')
    sp_lat = np.zeros((1,1,1,3))
    #ham = build_ham()
    ham = build_modified_ham(exch_1,exch_2,exch_3,iso_shell=[2,3])
    ham.verbose_all_interactions()
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
    #ham.map_MAE_3d(sp_lat,show=True,display_mode='3D')
