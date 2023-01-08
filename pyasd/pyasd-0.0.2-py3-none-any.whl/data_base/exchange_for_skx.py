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
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,1,1,1)

S_values = np.array([3/2,3/2])
SIA = np.ones(2)*0.09
J1_iso = np.ones(2)*4.5
DM1_rpz = np.array([[2.25,0,0],[-2.25,0,0]])
DM1_xyz = get_exchange_xyz(DM1_rpz,rotvecs[0])
exch_1 = exchange_shell( neigh_idx[0], J1_iso, DM_xyz = DM1_xyz, shell_name = '1NN')

if __name__=='__main__':
    print ('exchange interactions for skyrmion lattice in a honeycomb lattice')
    sp_lat = np.zeros((1,1,2,3))
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(S_values=S_values,BL_SIA=[SIA],BL_exch=[exch_1])
    ham.verbose_all_interactions()
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
