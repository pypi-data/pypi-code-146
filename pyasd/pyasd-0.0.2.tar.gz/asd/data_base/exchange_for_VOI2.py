#!/usr/bin/env python

# exchange parameters for VOI2 monolayer 
# see Xu et al. Phys. Rev. Lett. 125, 037203 (2020), table I
# still under construction
# Jan 17, 2021

import numpy as np
from asd.core.shell_exchange import get_exchange_xyz,exchange_shell
from asd.core.geometry import build_latt

lat_type='square'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,1,1,1)

S_values = np.array([1./2])

# single ion part
SIA = - np.array([-0.01])*S_values**2

# NN exchange along I
J1_iso = np.zeros(1)

J1_sym = - np.array([
[8.20, 0.00, 0.00],
[0.00, 8.66, 0.00],
[0.00, 0.00, 8.59]])

J1_sym = np.array([J1_sym])*S_values[0]**2
DM1_rpz = - np.array([[0,0,1.76],[0,0,-1.76]])

# NN exchange along O
J2_iso = np.zeros(2)

J2_sym = - np.array([
[5.35, 0.00, 0.00],
[0.00, 5.29, 0.00],
[0.00, 0.00, 5.20]])

J2_sym = np.array([J2_sym])*S_values[0]**2
DM2_rpz = np.zeros((1,3))

# NNN exchange along IO
J3_iso = np.zeros(1)

J3_sym = - np.array([
[0.76, 0.00, 0.00],
[0.00, 0.75, 0.00],
[0.00, 0.00, 0.72]])

J3_sym = np.array([J3_sym])*S_values[0]*S_values[0]**2
DM3_rpz = np.zeros((1,3))

J1_sym_xyz = get_exchange_xyz(J1_sym, rotvecs[0][:,::2])
DM1_xyz = get_exchange_xyz(DM1_rpz, rotvecs[0][:,::2])

J2_sym_xyz = get_exchange_xyz(J2_sym, rotvecs[0][:,1::2])
DM2_xyz = get_exchange_xyz(DM2_rpz, rotvecs[0][:,1::2])

J3_sym_xyz = get_exchange_xyz(J3_sym, rotvecs[1])
DM3_xyz = get_exchange_xyz(DM3_rpz, rotvecs[1])

exch_1 = exchange_shell( neigh_idx[0][:,::2], J1_iso, J1_sym_xyz, DM1_xyz, shell_name = '1NN_via_I')
exch_2 = exchange_shell( neigh_idx[0][:,1::2],J2_iso, J2_sym_xyz, DM2_xyz, shell_name = '1NN_via_O')
exch_3 = exchange_shell( neigh_idx[1], J3_iso, J3_sym_xyz, DM3_xyz, shell_name = '2NN_IO')

def build_ham(Bfield=np.zeros(3)):
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,
    BL_SIA=[SIA],BL_exch=[exch_1,exch_2,exch_3],
    exchange_in_matrix=True)
    return ham


if __name__=='__main__':
    print ('exchange parameters for VOI2')
    sp_lat = np.zeros((1,1,1,3))
    ham = build_ham()
    ham.verbose_all_interactions()
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
