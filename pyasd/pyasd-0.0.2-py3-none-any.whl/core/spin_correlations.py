#!/usr/bin/env python

#=============================================
#
# structure factors of spin configs
# Shunhong Zhang
# Last modified: Nov 27, 2021
#
#=============================================

from __future__ import print_function
import sys
import numpy as np
import time
import pickle
from asd.core.shell_exchange import get_latt_idx
from asd.core.constants import *
from asd.core.geometry import calc_space_disp

meV_to_THz = 1e-3/(Hbar*1e12*2*np.pi)


def gen_uniform_qmesh(nqx=100,nqy=100,bound=1):
    qpt_cart=np.mgrid[-bound:bound:1.j*nqx,-bound:bound:1.j*nqy]
    qpt_cart = np.transpose(qpt_cart,(1,2,0)).reshape(-1,2)
    return qpt_cart


def calc_static_structure_factor(spins,sites_cart,qpt_cart,dump=True):
    phase_factor = np.einsum('qi,ri->qr',qpt_cart,sites_cart)
    phase = np.exp(-1.j*phase_factor)
    S_vector = abs(np.dot(phase,spins))**2/spins.shape[0]
    if dump:  pickle.dump(S_vector,open('S_vector.pickle','wb'))
    return S_vector


def mpi_calc_static_structure_factor(spins,sites_cart,qpt_cart,dump=True):
    import asd.mpi.mpi_tools as mt
    comm,size,rank,node = mt.get_mpi_handles()
    start,last = mt.assign_task(len(qpt_cart),size,rank)
    S_vector = calc_static_structure_factor(spins,sites_cart,qpt_cart[start:last],dump=False)
    S_vector = comm.allgather(S_vector)
    S_vector = np.concatenate(S_vector,axis=0)
    if dump and rank==0: pickle.dump(S_vector,open('S_vector.pickle','wb'))
    return S_vector


# According to 
# Phys. Rev. B 87, 144401 (2013)
# Nat. Commun. 5, 4815 (2014)
# the space- and time-displaced correlation function 
# is necessary to calculate the
# dynamic structure factor and the magnon spectra
# Here
# confs_0 contain configurations at moment 0
# confs_t contain configurations at moment t
# from different ensembles
# 
# periodic boundary condition is assumed
#
# Note: in some references, e.g. Phys. Rev. Mater. 4, 024409 (2020)
# Eq. (5): the term <m(R_i,t)> * <m(R_j,0> is not subtracted
# here we follow this convention Jan 02, 2022

alert_cutoff='''
Warning from calc_correlation_function:
The cutoff you set along some direction exceeds
half the size of supercell:
cutoff = {}, supercell size = {}
This might lead to some unphysical "correlation"
originated from the periodic boundary condition
If you want to investigate long-range correlation,
use open boundary condition or larger supercell.
'''
def calc_correlation_function_1(confs_t,confs_0,cutoff_x=3,cutoff_y=3,verbosity=0):
    ave_confs_0 = np.average(confs_0,axis=0)  # ensemble average of confs_0
    ave_confs_t = np.average(confs_t,axis=0)
    nsample,nx,ny,nat = confs_t.shape[:4]
    nnx = 2*cutoff_x+1
    nny = 2*cutoff_y+1
    assert nnx<nx, alert_cutoff.format(cutoff_x,nx)
    assert nny<ny, alert_cutoff.format(cutoff_y,ny)
    Corr = np.zeros((nnx,nny,nat,nat,3),float)
    stime = time.time()
    if verbosity: print ('Calculate spin-spin correlation functions.')
    for ix,iy in np.ndindex(nx,ny):
        if (ix+1)%(nx//5)==0 and (iy+1)%(ny//5)==0 and verbosity:
            print ('ix = {:4d}, iy = {:4d}'.format(ix+1,iy+1))

        for ii,dx in enumerate(range(-cutoff_x,cutoff_x+1)):
            jx = (ix+dx)%nx
            for jj,dy in enumerate(range(-cutoff_y,cutoff_y+1)):
                jy = (iy+dy)%ny
                for iat,jat in np.ndindex(nat,nat):
                    cc = confs_t[:,ix,iy,iat] * confs_0[:,jx,jy,jat]
                    Corr[ii,jj,iat,jat] += np.average(cc, axis=0)
                    if nsample>1: Corr[ii,jj,iat,jat] -= ave_confs_t[ix,iy,iat] * ave_confs_0[jx,jy,jat]
    if verbosity: print ('Finished. Time used: {:8.3f} s'.format(time.time()-stime))
    return Corr/(nx*ny)


def calculate_correlation_function_dR(confs_t,confs_0,dx,dy,ave_on_confs=True):
    confs_tmp = np.roll(confs_0,(-dy,-dx),axis=(2,1))
    cc = np.einsum('sxyad,sxybd->sxyabd',confs_t,confs_tmp)
    if ave_on_confs: return np.average(cc,axis=(0,1,2))
    else: return np.average(cc,axis=(1,2))


def mpi_calculate_correlation_function_dR(confs_t,confs_0,dx,dy,ave_on_confs=True):
    import asd.mpi.mpi_tools as mt
    import mpi4py.MPI as MPI
    comm,size,rank,node = mt.get_mpi_handles()

    stime = time.time()
    if rank==0: shape = confs_t.shape
    else: shape=None
    shape = comm.bcast(shape)
    nsample,nx,ny,nat = shape[:4]

    itemsize = MPI.DOUBLE.Get_size()
    nbytes = itemsize*np.prod(shape)
    win1 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
    buf1, itemsize0 = win1.Shared_query(0)
    assert itemsize0 == itemsize
    confs_0_shared = np.ndarray(buffer=buf1, dtype='float', shape=shape)
    if rank==0: confs_0_shared[:] = confs_0

    win2 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
    buf2, itemsize0 = win2.Shared_query(0)
    assert itemsize0 == itemsize
    confs_t_shared = np.ndarray(buffer=buf2, dtype='float', shape=shape)
    if rank==0: confs_t_shared[:] = confs_t

    comm.barrier()
    start,last = mt.assign_task(nsample,size,rank)
    corr = np.zeros((nat,nat,3))
    for isample in range(start,last):
        confs_tmp = np.roll(confs_0_shared[isample],(-dy,-dx),axis=(1,0))
        cc = np.einsum('xyad,xybd->xyabd',confs_t_shared[isample],confs_tmp)
        corr += np.average(cc,axis=(0,1))
    corr = comm.allreduce(corr)
    corr = corr/nsample
    if rank==0: print('Time used: {:8.3f} s'.format(time.time()-stime)); sys.stdout.flush()
    win1.Free()
    win2.Free()
    return corr



# This new function runs much faster than calc_correlation_function_1 (an early verion)
# thanks to the numpy.roll function of Numpy lib
# Currently it is only tested for static (time-independent) spin correlations
# For time-dependent cases further tests are required
def calc_correlation_function(confs_t,confs_0,cutoff_x=3,cutoff_y=3,verbosity=0,substract_background=True):
    ave_confs_0 = np.average(confs_0,axis=0)  # ensemble average of confs_0
    ave_confs_t = np.average(confs_t,axis=0)
    nsample,nx,ny,nat = confs_t.shape[:4]
    nnx = 2*cutoff_x+1
    nny = 2*cutoff_y+1
    assert nnx<nx, alert_cutoff.format(cutoff_x,nx)
    assert nny<ny, alert_cutoff.format(cutoff_y,ny)
    Corr = np.zeros((nnx,nny,nat,nat,3),float)
    stime = time.time()
    gg = (cutoff_x*2+1)*(cutoff_y*2+1)
    prog = '{:4d} of {} ({:5.1f} %) finished, time used: {:8.3f} s'
    if verbosity: print ('Calculate spin-spin correlation functions.')
    dR_grids = np.mgrid[-cutoff_x:cutoff_x+1,-cutoff_y:cutoff_y+1]
    for ii,jj in np.ndindex(nnx,nny):
        dx,dy = dR_grids[:,ii,jj]
        ig = jj + ii*(cutoff_y*2+1)
        if verbosity and ig%(gg//20)==0: print (prog.format(ig,gg,100.*ig/gg,time.time()-stime))
        confs_tmp = np.roll(confs_0,(-dy,-dx),axis=(2,1))
        for iat,jat in np.ndindex(nat,nat):
            cc = confs_t[:,:,:,iat] * confs_tmp[:,:,:,jat]
            Corr[ii,jj,iat,jat] = np.average(cc, axis=(0,1,2))
            if nsample>1 and substract_background:
                ave_confs_tmp = np.average(confs_tmp[:,:,:,jat],axis=0)
                Corr[ii,jj,iat,jat] -= np.average(ave_confs_t[:,:,iat] * ave_confs_tmp, axis=(0,1))
    if verbosity: print ('Finished. Time used: {:8.3f} s'.format(time.time()-stime))
    return Corr


def mpi_get_confs_t(nx,ny,nat,prefix='Ensemble',fil_key='spin_confs.ovf',start_conf=0):
    import asd.mpi.mpi_tools as mt
    import glob
    from asd.utility.ovf_tools import parse_ovf
    comm,size,rank,node = mt.get_mpi_handles()
    if prefix=='': dirs=['.']
    else: dirs = sorted(glob.glob('{}_*'.format(prefix)))
    if dirs==[]: 
        if rank==0: print ('Cannot find ovf files at directories with prefix "{}"!'.format(prefix))
        exit()
    nsample = len(dirs)
    start,last = mt.assign_task(nsample,size,rank)
    confs_t = []
    for i in range(start,last):
        fil = glob.glob('{}/{}'.format(dirs[i],fil_key))[0]
        spins = parse_ovf(fil)[1]
        confs = np.swapaxes(spins.reshape(spins.shape[0],ny,nx,nat,3),1,2)
        confs_t.append(confs[start_conf:])
    confs_t = comm.gather(confs_t)
    if rank==0: confs_t = np.array([conf for confs in confs_t for conf in confs if len(confs)>0])
    else: confs_t = None
    return confs_t


def verbose_Swq_setup(nsample,nconf,nsite,idx0,time_spacing,nq,nomega,max_omega,cutoff_x,cutoff_y,ncore):
    print ('\nCalculating correlation functions of snapshots\n')
    print ('Parallel on {} cores'.format(ncore))
    print ('No. of samples for ensemble average: {}'.format(nsample))
    if nsample==1: print ('Ensemble average not applied')
    print ('No. of spin sites: {}'.format(nsite))
    print ('No. of data points on the time axis: {}'.format(nconf))
    print ('Index for the t=0 snapshot: {}'.format(idx0))
    print ('Time spacing for Fourier transformation: {} ps'.format(time_spacing))
    print ('No. of q-points: {}'.format(nq))
    print ('No. of frequency points: {}'.format(nomega))
    print ('Max frequency = {:.3f} THz'.format(max_omega))
    print ('Max magnon energy = {:.3f} meV'.format(max_omega/meV_to_THz))
    print ('Real space cutoff for correlation function:')
    print ('Rcut_x = {}, Rcut_y = {}\n'.format(cutoff_x,cutoff_y))
    print ('\nStarted at {}\n'.format(time.ctime()))


# shape of confs: nsample, nconf, nx, ny, nat, ndir
# nsample is the number of samples for ensemble averaging
# nconf is the number of components for time-frequency Fourier transformation
def calc_dyn_structure_factor(confs,latt,sites,qpt_cart,time_spacing,omegas,
    cutoff_x=3,cutoff_y=3,cutoff_z=0,
    dump=True,pickle_name='Swq.pickle',verbosity=1):

    nx,ny = sites.shape[:2]
    nat,ndim = sites.shape[-2:]
    nsite = np.prod(sites.shape[:-1])
    nq = len(qpt_cart)
    nomega = len(omegas)
    shape = confs.shape
    nsample,nconf = shape[:2]

    times = (np.arange(nconf)-nconf//2)*time_spacing
    time_phases = np.exp(2.j*np.pi * np.einsum('w,t->wt',omegas,times) )

    space_disp = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z,ndim)
    space_phases = np.exp(2.j*np.pi * np.einsum('qi,xyabi-> qxyab',qpt_cart, space_disp) )

    stime = time.time()
    Swq = np.zeros((nq,nomega,3),complex)

    confs_t = np.zeros((nsample,nconf,*tuple(shape[2:])))
    idx0 = np.where(times==0)[0][0]
    confs_0 = confs[:,idx0]
    if verbosity: verbose_Swq_setup(nsample,nconf,nsite,idx0,time_spacing,nq,nomega,np.max(omegas),cutoff_x,cutoff_y,1)
    confs_t = confs
    
    mm = max(1,nconf//10)
    prog = 'Progress {:2d} / {}: Conf {:4d} of {}, time = {:10.3f} s'
    for iconf in range(nconf):
        if iconf%mm==0 and verbosity>1: 
            print (prog.format(iconf//mm,min(max(10,nconf//mm),nconf),iconf,nconf,time.time()-stime))
            sys.stdout.flush()
        Corr = calc_correlation_function(confs_t[:,iconf],confs_0,cutoff_x=cutoff_x,cutoff_y=cutoff_y)
        Swq0 = np.einsum('w,qxyab,xyabi->qwi',time_phases[:,iconf],space_phases,Corr)/np.prod(Corr.shape[:2])
        Swq += Swq0

    Swq *= time_spacing/(2*np.pi)
    if dump:  
        pickle.dump(Swq,open(pickle_name,'wb'))
        print ('\nFinished at {}\nTime used: {:8.2f} s'.format(time.ctime(),time.time()-stime))
    return Swq


# a parallel version
def mpi_calc_dyn_structure_factor(confs,latt,sites,qpt_cart,time_spacing,omegas,
    cutoff_x=3,cutoff_y=3,cutoff_z=0,
    dump=True,pickle_name='Swq.pickle',verbosity=1):
    import asd.mpi.mpi_tools as mt
    comm,size,rank,node = mt.get_mpi_handles()
    nx,ny = sites.shape[:2]
    nat,ndim = sites.shape[-2:]
    nsite = np.prod(sites.shape[:-1])
    nq = len(qpt_cart)
    nomega = len(omegas)
    if not rank: shape = confs.shape
    else: shape = None
    shape = comm.bcast(shape)
    nsample,nconf = shape[:2]

    times = (np.arange(nconf)-nconf//2)*time_spacing
    time_phases = np.exp(2.j*np.pi * np.einsum('w,t->wt',omegas,times) )

    if not rank: space_disp = calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z,ndim)
    else: space_disp = None
    space_disp = comm.bcast(space_disp)
    space_phases = np.exp(2.j*np.pi * np.einsum('qi,xyabi-> qxyab',qpt_cart, space_disp) )

    stime = time.time()
    Swq = np.zeros((nq,nomega,3),complex)

    start,last = mt.assign_task(nconf,size,rank)

    confs_t = np.zeros((nsample,last-start,*tuple(shape[2:])))
    if rank==0:
        idx0 = np.where(times==0)[0][0]
        confs_0 = confs[:,idx0]
        if verbosity: verbose_Swq_setup(nsample,nconf,nsite,idx0,time_spacing,nq,nomega,np.max(omegas),cutoff_x,cutoff_y,size)
        confs_t = confs[:,start:last]
        for irank in range(1,size):
            start0,last0 = mt.assign_task(nconf,size,irank)
            comm.send(confs[:,start0:last0],dest=irank,tag=irank)
    else:
        confs_0 = None
        confs_t = comm.recv(source=0,tag=rank)
    confs_0 = comm.bcast(confs_0)
    
    mm = max(1,(last-start)//10)
    prog = 'Progress {:2d} / {}: Conf {:4d} of {}, time = {:10.3f} s'
    for iconf in range(last-start):
        if iconf%mm==0 and not rank and verbosity>1: 
            print (prog.format(iconf//mm,min(max(10,(last-start)//mm),last-start),iconf,last-start,time.time()-stime))
            sys.stdout.flush()
        Corr = calc_correlation_function(confs_t[:,iconf],confs_0,cutoff_x=cutoff_x,cutoff_y=cutoff_y)
        Swq0 = np.einsum('w,qxyab,xyabi->qwi',time_phases[:,iconf+start],space_phases,Corr)/np.prod(Corr.shape[:2])
        Swq += Swq0

    Swq = comm.allreduce(Swq)
    Swq *= time_spacing/(2*np.pi)
    if not rank and dump:  
        pickle.dump(Swq,open(pickle_name,'wb'))
        print ('\nFinished at {}\nTime used: {:8.2f} s'.format(time.ctime(),time.time()-stime))
    return Swq


if __name__=='__main__':
    print ('Running {}'.format(__file__.split('/')[-1]))
