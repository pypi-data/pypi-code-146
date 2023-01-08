#!/usr/bin/env python3

import os
import numpy as np
from asd.core.hamiltonian import *
from asd.data_base.exchange_for_Gd2C import *
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.core.monte_carlo import *
from asd.utility.spin_visualize_tools import *
import asd.mpi.mpi_tools as mt


# the following two functions function 
# similar to ham.calc_local_energy 
# which can take care of both 2D and 3D cases

def calc_local_energy_2D(ham,sp_lat,ix,iy,iat,spin_coord=None):
    if spin_coord is not None: sp_lat = np.dot(sp_lat,np.linalg.inv(spin_coord))

    shape = sp_lat.shape
    nx,ny = shape[:2]
    n_i = copy.copy(sp_lat[ix,iy,iat])
    E_SIA = 0
    for iaxis in range(ham._naxis_bl):
        E_SIA -= ham._BL_SIA[iaxis][iat] * np.dot(n_i,ham._BL_SIA_axis[iaxis][iat])**2
    for iaxis in range(ham._naxis_bq):
        E_SIA -= ham._BQ_SIA[iaxis][iat] * np.dot(n_i,ham._BQ_SIA_axis[iaxis][iat])**4
    E_zeeman = -np.dot(n_i, ham._Bfield)*2*ham._S_values[iat]*muB
    E_exch = 0.
    for exch in ham._BL_exch:
        for j,(dx,dy,jat) in enumerate(exch._neigh_idx[iat]):
            jx = (ix+dx)%nx
            jy = (iy+dy)%ny
            n_j = sp_lat[jx,jy,jat]
            if exch._Jmat is not None: E_exch -= np.dot(np.dot(n_i,exch._Jmat[iat,j]),n_j)
            else: E_exch -= exch._J_iso[iat]*np.dot(n_i,n_j)

    E_local = E_SIA + E_zeeman + E_exch
    return E_local


def calc_local_energy_3D(ham,sp_lat,ix,iy,iz,iat,spin_coord=None):
    if spin_coord is not None: sp_lat = np.dot(sp_lat,np.linalg.inv(spin_coord))

    shape = sp_lat.shape
    nx,ny,nz = shape[:-2]
    n_i = copy.copy(sp_lat[ix,iy,iz,iat])
    E_SIA = 0
    for iaxis in range(ham._naxis_bl):
        E_SIA -= ham._BL_SIA[iaxis][iat] * np.dot(n_i,ham._BL_SIA_axis[iaxis][iat])**2
    for iaxis in range(ham._naxis_bq):
        E_SIA -= ham._BQ_SIA[iaxis][iat] * np.dot(n_i,ham._BQ_SIA_axis[iaxis][iat])**4
    E_zeeman = -np.dot(n_i, ham._Bfield)*2*ham._S_values[iat]*muB
    E_exch = 0.

    for exch in ham._BL_exch:
        for j,(dx,dy,dz,jat) in enumerate(exch._neigh_idx[iat]):
            jx = (ix+dx)%nx
            jy = (iy+dy)%ny
            jz = (iz+dz)%nz
            n_j = sp_lat[jx,jy,jz,jat]
            if exch._Jmat is not None: E_exch -= np.dot(np.dot(n_i,exch._Jmat[iat,j]),n_j)
            else: E_exch -= exch._J_iso[iat]*np.dot(n_i,n_j)

    E_local = E_SIA + E_zeeman + E_exch
    return E_local



def test_2d_latt(nx=8,ny=8,lat_type='honeycomb',ntest=10):
    latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1)
    nat=sites.shape[2]
    Bfield=np.array([2,1,3])

    sp_lat = np.zeros((nx,ny,nat,3),float)
    sp_lat = init_random(sp_lat,verbosity=0)

    ham = spin_hamiltonian(
    Bfield=Bfield,S_values=S_values,
    BL_SIA=[SIA],
    BL_exch = [exch_1,exch_2,exch_3],
    iso_only=True)

    print ('\nTest local energy in 2D lattice')
    for i in range(ntest):
        idx = np.random.randint((nx,ny,nat))
        e1 = ham.calc_local_energy(sp_lat,idx)
        e2 = calc_local_energy_2D(ham,sp_lat,*tuple(idx))
        print (('{:4d} '*len(idx)+'{:12.5f} '*2).format(*tuple(idx),e1,e2),np.allclose(e1,e2))



def test_3d_latt(nx=5,ny=5,nz=5,lat_type='simple cubic',ntest=10):
    latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
    nat=sites.shape[-2]
    Bfield=np.array([1,1,2])

    S_values = np.ones(1)
    SIA = np.zeros(1)
    exch_1 = exchange_shell(neigh_idx[0], np.ones(1), shell_name='1NN')

    ham = spin_hamiltonian(
    Bfield=Bfield,S_values=S_values,BL_SIA=[SIA],
    BL_exch = [exch_1],
    iso_only=True)

    sp_lat = np.zeros((nx,ny,nz,nat,3),float)
    sp_lat = init_random(sp_lat,verbosity=0)

    print ('\nTest local energy in 3D lattice')
    for i in range(ntest):
        idx = np.random.randint((nx,ny,nz,nat))
        e1 = ham.calc_local_energy(sp_lat,idx)
        e2 = calc_local_energy_3D(ham,sp_lat,*tuple(idx))
        print (('{:4d} '*len(idx)+'{:12.5f} '*2).format(*tuple(idx),e1,e2),np.allclose(e1,e2))


if __name__ == '__main__':
    test_3d_latt()
    test_2d_latt()
