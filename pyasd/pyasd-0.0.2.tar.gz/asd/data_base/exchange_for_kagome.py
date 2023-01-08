#!/usr/bin/env python

# DM interactions only exist in NN exchange
# with only non-vanishing out-of-plane component

import numpy as np
from asd.core.shell_exchange import get_exchange_xyz,exchange_shell
from asd.core.geometry import build_latt
from asd.core.constants import muB

ref = '''
# Phys. Rev. Lett. 104, 066403 (2010)
# Phys. Rev. B      94, 174444 (2016)'''

lat_type='kagome'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,1,1,1)

S_values = np.array([1./2,1./2,1./2])
SIA = - np.array([0.,0.,0.])*S_values**2

J1=0.3
J1_iso = np.ones(3)*J1*S_values[0]**2
J2_iso = np.zeros(3)
J3_iso = np.zeros(3)

DM = np.array([0,0,0.045])*S_values[0]*S_values[1]
DM1_xyz = np.tile(np.array([DM,-DM,DM,-DM]).reshape(4,3),(3,1,1))

exch_1 = exchange_shell( neigh_idx[0], J1_iso, DM_xyz = DM1_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, shell_name = '2NN')
exch_3 = exchange_shell( neigh_idx[2], J3_iso, shell_name = '3NN')

H0 = 0.1/(2*S_values[0]*muB)
Bfield=np.array([0,0,H0])
nshell=1
BL_exch=[exch_1,exch_2,exch_3][:nshell]


if __name__ == '__main__':
    print ('exchange interaction for the Kagome lattice\n{}'.format(ref))
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(
    Bfield=Bfield,
    S_values=S_values,
    BL_SIA=[SIA],
    BL_exch=BL_exch)
    #ham.verbose_all_interactions()
    sp_lat = np.zeros((1,1,3,3))
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
