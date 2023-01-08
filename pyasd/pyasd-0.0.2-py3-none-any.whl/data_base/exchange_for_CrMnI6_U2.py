#!/usr/bin/env python

import numpy as np
import sys
from asd.core.shell_exchange import *
from asd.core.geometry import build_latt

lat_type='honeycomb'
nx=1
ny=1
nz=1

S1=3./2
S2=4./2
S_values=np.array([S1,S2])

# single ion part
Bfield=np.array([0,0,0])  # in Tesla
SIA = np.array([0.1422,0.6425])*S_values**2

# nearest neighbor
J1_sym=np.array([
[    0.3317 ,    0.0000  ,   0.4417 ],
[    0.0000 ,    0.8333  ,   0.0000 ],
[    0.4417 ,    0.0000  ,   0.3825 ]])

J1_sym = np.array([J1_sym,J1_sym])*S1*S2

# second nearest neighbor
J2a_sym= - np.array([
[   -0.4467 ,    0.0006  ,  -0.0656 ],
[    0.0006 ,   -0.4833  ,  -0.0006 ],
[   -0.0656 ,   -0.0006  ,  -0.4556 ]])


J2a_sym *= S1**2

J2b_sym = - np.array([
[   -1.1612 ,    0.0003  ,   0.5759 ],
[    0.0003 ,    0.3619  ,  -0.0006 ],
[    0.5759 ,   -0.0006  ,  -0.3562 ]])


J2b_sym *= S2**2

J2_sym = np.array([J2a_sym,J2b_sym])


J1_alpha = 0.833333
J1_beta  = 0.799481
J1_iso = np.array([(J1_alpha+J1_beta)/2, (J1_alpha+J1_beta)/2])*S1*S2

#DM1_rpz = np.array([0.2538,-0.1600,0])*S1*S2   # from DFT
DM1_rpz = np.array([0,0.28,0])*S1*S2 # symmetrized

DM1_rpz = np.array([DM1_rpz,-DM1_rpz])

J2a_trace=np.array([0.5089, 0.4700, 0.3722])
J2b_trace=np.array([1.4452, 0.1685,-0.3588])
J2a=np.average(J2a_trace)
J2b=np.average(J2b_trace)

# a simplified version, average the trace
#J2_iso = np.array([J2a,J2b]) * S_values**2

# a complex version, work with the Kitaev2 terms
J2_iso = np.array([(J2a_trace[0]+J2a_trace[1])/2,(J2b_trace[1]+J2b_trace[2])/2]) * S_values**2

DM2_rpz_1 = - np.array([0.0961  ,   0.0000  ,  -0.0506])*S1**2
DM2_rpz_2 = - np.array([0.0856  ,   0.0003  ,  -0.3416])*S2**2
DM2_rpz=np.array([DM2_rpz_1,DM2_rpz_2])


J3_sym = - np.array([
[   -0.0892 ,    0.0000  ,  -0.0400 ],
[    0.0000 ,   -0.0483  ,   0.0000 ],
[   -0.0400 ,    0.0000  ,  -0.1250 ]])

J3_sym = np.array([J3_sym,J3_sym])*S1*S2

J3_iso = np.zeros(2)*S1*S2
DM3_rpz = np.zeros((2,3))*S1*S2

latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
nat=sites.shape[2]

J1_sym_xyz = get_exchange_xyz(J1_sym, rotvecs[0])
DM1_xyz = get_exchange_xyz(DM1_rpz,rotvecs[0])

J2_sym_xyz = get_exchange_xyz(J2_sym, rotvecs[1])
DM2_xyz = get_exchange_xyz(DM2_rpz,rotvecs[1])

J3_sym_xyz = get_exchange_xyz(J3_sym, rotvecs[2])
DM3_xyz = get_exchange_xyz(DM3_rpz,rotvecs[2])


exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, DM1_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, DM2_xyz, shell_name = '2NN')
exch_3 = exchange_shell( neigh_idx[2], J3_iso, J3_sym_xyz, DM3_xyz, shell_name = '3NN')

BQ = np.array([ 0.0894, -0.4111])
bq_exch_2 = biquadratic_exchange_shell(neigh_idx[1],BQ,'BQ_2NN')



def build_ham(Bfield=np.zeros(3)):
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(Bfield=Bfield,
    S_values=S_values,
    BL_SIA=[SIA],
    BL_exch=[exch_1,exch_2,exch_3],
    BQ_exch = [bq_exch_2],
    exchange_in_matrix=True)
    return ham


if __name__=='__main__':
    print ('exchange interactions for CrMnI6, U_eff=2')
    sp_lat = np.zeros((1,1,2,3))
    ham = build_ham()
    ham.verbose_all_interactions()
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)
