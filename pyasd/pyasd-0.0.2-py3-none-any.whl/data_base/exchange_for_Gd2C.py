#!/usr/bin/env python

# A simple spin Hamiltonian with only NN exchange
# on a honeycomb lattice
# which can produce skyrmion lattice under small B field
# only isotropic Heisenberg and DM interactions are included
# A small Single-ion anisotropy is also added

from asd.core.geometry import *
from asd.core.shell_exchange import *
import numpy as np

lat_type='honeycomb'
nx=1
ny=1
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1)

S_values = np.array([7/2,7/2])
SIA = np.array([0.605,0.605])

J1_iso = np.ones(2)*0.333*4*S_values[0]*S_values[1]
J2_iso = np.ones(2)*0.243*4*S_values[0]*S_values[0]
J3_iso = np.ones(2)*0.195*4*S_values[0]*S_values[1]

exch_1 = exchange_shell( neigh_idx[0], J1_iso, shell_name='1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, shell_name='2NN')
exch_3 = exchange_shell( neigh_idx[2], J3_iso, shell_name='3NN')


if __name__=='__main__':
    print ('exchange interactions for Cd2C')
    sp_lat = np.zeros((1,1,2,3))
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(S_values=S_values,
    BL_SIA=[SIA],BL_exch=[exch_1,exch_2,exch_3],
    iso_only=True)
    ham.verbose_all_interactions()
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
    ham.map_MAE_3d(sp_lat,show=True,map_shape=False)
