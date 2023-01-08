#!/usr/bin/env python

import numpy as np
from asd.core.shell_exchange import get_exchange_xyz,exchange_shell
from asd.core.geometry import build_latt

lat_type='honeycomb'
nx=1
ny=1
nz=1
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)


S_values = np.array([3./2,3./2])

SIA = - np.array([-0.25778, -0.25778])*S_values**2

J1_iso = np.zeros(2)
J2_iso = np.zeros(2)

J1_sym = - np.array([
[   -1.5511 ,    0.0000 ,   -0.3200 ],
[    0.0000 ,   -2.2311 ,   -0.0000 ],
[   -0.3200 ,   -0.0000 ,   -2.0356 ]])

J1_sym = np.array([J1_sym, J1_sym])*S_values[0]*S_values[1]
DM1_rpz = np.zeros((2,3))

# data from changsong xu paper
J2_sym = - np.array([
[-0.669, -0.136,  0.085],
[ 0.079, -0.636,  0.017],
[-0.057, -0.065, -0.609]])

J2_sym = np.array([J2_sym, J2_sym])*S_values[0]*S_values[1]
DM2_rpz = - np.array([0.082, 0, -0.108])*S_values[0]**2
DM2_rpz = np.array([DM2_rpz,-DM2_rpz])

J1_sym_xyz = get_exchange_xyz(J1_sym, rotvecs[0])
DM1_xyz = get_exchange_xyz(DM1_rpz, rotvecs[0])

J2_sym_xyz = get_exchange_xyz(J2_sym, rotvecs[1])
DM2_xyz = get_exchange_xyz(DM2_rpz, rotvecs[1])

exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, DM1_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, DM2_xyz, shell_name = '2NN')


if __name__=='__main__':
    print ('exchange interactions for CrI3')
    sp_lat = np.zeros((1,1,2,3))
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(S_values=S_values,
    BL_SIA=[SIA],BL_exch=[exch_1,exch_2],
    exchange_in_matrix=True)
    ham.verbose_all_interactions()
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
