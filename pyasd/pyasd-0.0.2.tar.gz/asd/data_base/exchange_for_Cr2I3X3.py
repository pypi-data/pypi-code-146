#!/usr/bin/env python

#====================================================
# exchange parameters for Janus Cr2X3I3 monolayers
# use parameters from
# Xu et al. Phys. Rev. B
# 101, 060404 (R) 2020
#=====================================================

from __future__ import print_function
import numpy as np
from asd.core.geometry import build_latt
from asd.core.hamiltonian import *
from asd.core.shell_exchange import get_exchange_xyz,exchange_shell


def calc_MAE(SIA,J1_mat,J2_mat,DM1_rpz,DM2_rpz,system):
    print ('\nSystem: {0}'.format(system))
    H = np.zeros(3)
    S1 = 3/2
    S2 = 3/2
    S_values = np.array([S1,S2])
    SIA *= S_values**2

    J1_sym = (J1_mat + J1_mat.T)/2
    J2_sym = (J2_mat + J2_mat.T)/2

    evals1,evec1=np.linalg.eigh(J1_sym)
    J1_iso = (evals1[1]+evals1[2])/2
    Kitaev1_mag = evals1[0] - J1_iso
    Kitaev1_mag = np.repeat(Kitaev1_mag,2)*S1*S2
    Kitaev1_vec = np.tile(evec1[:,0],(2,1))
    J1_iso = np.repeat(J1_iso,2)*S1*S2

    evals2,evec2=np.linalg.eigh(J2_sym)
    J2_iso = (evals2[1]+evals2[2])/2
    Kitaev2_mag = evals2[0] - J2_iso
    Kitaev2_mag = np.repeat(Kitaev2_mag,2)*S1**2
    Kitaev2_vec = np.tile(evec2[:,0],(2,1))
    J2_iso = np.repeat(J2_iso,2)*S1**2

    print ('\nK1 = {:10.5f}, K2 = {:10.5f}'.format(Kitaev1_mag[0]/S1/S2,Kitaev2_mag[0]/S1**2))
    print ('Kitaev energy for FM along z: ', -(Kitaev1_mag[0]*Kitaev1_vec[0,2]**2*6 + Kitaev2_mag[0]*Kitaev2_vec[0,2]**2*12)/2/2)

    J1_sym = np.array([J1_sym,J1_sym])*S1*S2
    J2_sym = np.array([J2_sym,J2_sym])*S1**2
    J3_sym = np.zeros_like(J1_sym)

    latt,sites,neigh_idx,rotvecs = build_latt('honeycomb',1,1,2)

    J1_sym_xyz = get_exchange_xyz(J1_sym, rotvecs[0])
    J2_sym_xyz = get_exchange_xyz(J2_sym, rotvecs[1])
    J3_sym_xyz = np.zeros_like(J1_sym_xyz)

    Kitaev1_xyz = get_exchange_xyz(Kitaev1_vec,rotvecs[0])
    Kitaev2_xyz = get_exchange_xyz(Kitaev2_vec,rotvecs[1])

    DM1_xyz = get_exchange_xyz(DM1_rpz,rotvecs[0])
    DM2_xyz = get_exchange_xyz(DM2_rpz,rotvecs[1])

    exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, DM1_xyz, Kitaev1_mag, Kitaev1_xyz, shell_name='1NN')
    exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, DM2_xyz, Kitaev2_mag, Kitaev2_xyz, shell_name='2NN')

    ham = spin_hamiltonian(
    S_values=S_values,BL_SIA=[SIA],
    BL_exch = [exch_1,exch_2],
    exchange_in_matrix=True)

    sp_lat  = np.zeros((1,1,2,3))
    ham.verbose_all_interactions(verbose_file='ham_{}.dat'.format(system))
    ham.verbose_reference_energy(sp_lat)
    ham.map_MAE(sp_lat,show=True)

    return ham


def test_CrI3():
    J1_mat = np.array([
    [ 2.354, -0.305, -0.167],
    [-0.305,  2.002, -0.289],
    [-0.167, -0.289,  2.297]])

    J2_mat = np.array([
    [ 0.669,  0.136, -0.085],
    [-0.079,  0.636, -0.017],
    [ 0.057,  0.065,  0.609]])

    DM1_rpz = np.zeros((2,3))
    DM2_rpz = np.array([[-0.041,0.071,0.108],[0.041,-0.071,-0.108]])
    SIA = np.array([0.262,0.262])

    calc_MAE(SIA,J1_mat,J2_mat,DM1_rpz,DM2_rpz,'CrI3')


def test_Cr2I3Br3():
    J1_mat = np.array([
    [ 1.874, -0.024, -0.301],
    [-0.317,  1.678, -0.069],
    [ 0.091, -0.296,  1.848]])

    J2_mat = np.array([
    [ 0.701,  0.087, -0.100],
    [-0.056,  0.676,  0.022],
    [ 0.078,  0.033,  0.643]])

    DM1_rpz = np.array([[0.113,0.196,0.147],[-0.113,-0.196,-0.147]])
    DM2_rpz = np.array([[-0.006,0.089,0.071],[0.006,-0.089,-0.071]])
    SIA = np.array([0.124,0.124])

    calc_MAE(SIA,J1_mat,J2_mat,DM1_rpz,DM2_rpz,'Cr2I3Br3')


def test_Cr2I3Cl3():
    J1_mat = np.array([
    [ 1.041, -0.028, -0.221],
    [-0.252,  0.877, -0.075],
    [ 0.046, -0.228,  1.032]])

    J2_mat = np.array([
    [ 0.789,  0.099, -0.121],
    [-0.071,  0.761,  0.033],
    [ 0.097,  0.034,  0.712]])

    DM1_rpz = np.array([[0.077,0.133,0.113],[-0.077,-0.133,-0.113]])
    DM2_rpz = np.array([[-0.001,0.109,0.085],[0.001,-0.109,-0.085]])
    SIA = np.array([0.029,0.029])

    calc_MAE(SIA,J1_mat,J2_mat,DM1_rpz,DM2_rpz,'Cr2I3Cl3')


if __name__=='__main__':
    print ('exchange interactions for Cr2I3X3')
    ham_CrI3 = test_CrI3()
    ham_Cr2I3Br3 = test_Cr2I3Br3()
    ham_Cr2I3Cl3 = test_Cr2I3Cl3()
