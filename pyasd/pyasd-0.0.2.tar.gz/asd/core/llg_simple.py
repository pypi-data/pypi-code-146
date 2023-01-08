#!/usr/bin/env python

#========================================================
#
# Self-developed code for LLG simulation
# use Depondt modified Heun method for
# numerical integration of the LLG equation
# Ref. Depondt and Mertens, J. Phys. 2009, 21, 336005
# See also: Phys. Rev. B 2019, 99, 224414
#
# Shunhong Zhang <szhang2@ustc.edu.cn>
# May 18 2021
#
#=========================================================
#
#=========================================================
# TODO: use max change of local magnetic field 
# as convergence criteria
#=========================================================

from __future__ import print_function
import os
import sys
import copy
import numpy as np
import time
import asd.mpi.mpi_tools as mt
from scipy.spatial.transform import Rotation as RT
from asd.utility.ovf_tools import gen_params_for_ovf, write_ovf
from asd.utility.head_figlet import *
from asd.core.hamiltonian import log_spin_hamiltonian
from asd.core.constants import kB,gamma_e,muB
from asd.core.random_vectors import gen_normal_random_spin
from asd.core.shell_exchange import get_latt_idx
from asd.core.log_general import log_general
from asd.core.topological_charge import calc_topo_chg, mpi_calc_topo_chg_one_conf
from asd.core.spin_configurations import check_sp_lat_norm,initialize_spin_lattice


fmt_log = '# {:7d} {:12.3f} {:14.3f} {:16.9f} {:16.6e} '+'{:10.4f}'*3+'{:14.6f}'


log_handle = log_general(
outdir='.',
prefix='',
n_log_conf=100,
n_log_magn=100,
log_ham_file='Hamiltonian.dat',
log_conf_file='spin_confs.ovf',
archive_file='M.dat',
log_file=None,
)


def get_nodes_root(comm,size,rank,node):
    nodes_root = [0]
    nodes = comm.gather(node)
    if rank==0:
        for irank in range(size-1):
            if nodes[irank]==nodes[irank+1]: continue
            nodes_root.append(irank+1)
    nodes_root = comm.bcast(nodes_root)
    return nodes_root


def print_oversize_warning(size,ntask,func='mpi_llg_simulation'):
    if size<=ntask: return 0
    print ('\nWarning from {}'.format(func))
    print ('You are invoking more cores than ')
    print ('number of spin sites involved in the dynamics')
    print ('This might lead to waste of computational resources')
    print ('No of cores = {}, No of sites for dynamics = {}'.format(size,ntask))
    print ('Duck bu bi')
    print ('Try setting number of cores no more than number of sites\n')


shared_memory_warning = '''
Warning from mpi_llg_simulation_shared_memory:
You are using the shared memory functionality
It is still under extensive tests
Currently only single-node calculations have been tested
If you invoke multi nodes, inter-node communication is important
If you are not sure whether it works correctly on your platform
It is recommended to use the routine parallel version: 
mpi_llg_simulation
Some inter-node communication problem may be solved by adding
export I_MPI_FABRICS=shm:tcp
to your job-submission script or .bashrc file\n'''


Note_therml_field_method = ''' 
We currently support two fields to generate random fields for modeling the thermal effect.
You set thermal_field_method to {}
We recommand setting thermal_field_method to 1

Here are some detailed description on the two methods
Method 1: this old implementation (not normalized) is incorrect, modified: Sep 13, 2021
we used to thought this method incorrect, but it yields results consistent with MC simulatins
so we resume to use it from Dec 28, 2021
Created from three Independent normally distributed numbers, see PRB 99, 224414 (2019)

Method 2: this method generate the white noise thermal field in a more reasonable way
but we found it inconsistent with MC simulations, and the Spirit code,
the mechanism remains elusive. We therefore temporarily discard it
'''

def print_thermal_field_method_warning(thermal_field_method=1):
    if thermal_field_method == 2: print (Note_thermal_field_method.format(thermal_field_method))



# log_mode can be 'w' or 'a'
def log_llg_data(log_time,log_ener,log_conf,log_conf_file='spin_confs.ovf',archive_file='M.dat',log_mode='w',topo_chg=[],dE=0):
    # loop x first and then y and finally z (if 3D), to be consistent with Spirit
    log_conf = np.array(log_conf)
    shape = log_conf.shape
    nx,ny,nz,nat,idx = get_latt_idx(shape[1:])
    move_axis = np.arange(1,len(shape)-2)
    log_conf = np.moveaxis(log_conf,move_axis,move_axis[::-1])

    if log_conf_file is not None:
        with open(log_conf_file,log_mode) as fw:
            if log_mode == 'w': 
                fw.write('# OOMMF OVF 2.0\n#\n')
                if 'initial' in log_conf_file or 'final' in log_conf_file:  fw.write('# Segment count: 1\n')
                else: fw.write('# Segment count: unknown\n')
        for tt,en,conf in zip(log_time,log_ener,log_conf):
            add_desc = [
            'LLG simulation (Depondt\'s solver)',
            'time = {:12.5f} ps'.format(tt),
            'ener = {:16.8f} meV'.format(en),
            'nx   = {:4d}'.format(nx),
            'ny   = {:4d}'.format(ny),
            'nz   = {:4d}'.format(nz),
            'nat  = {:4d}'.format(nat)]
            params = gen_params_for_ovf(nx,ny,nz,additional_desc=add_desc)
            write_ovf(params,conf.reshape(-1,3),log_conf_file,'a')

    if archive_file is not None:
        head  = '{:>12s} {:>16s} {:>20s}'.format('# time (ps)','E (meV/site)','dE (meV/site)')
        head += ('{:>14s} '*3).format('Mx','My','Mz')
        fmt = '{:12.4f} {:16.10f} {:20.10e}'
        mm=np.average(log_conf,axis=tuple(range(1,len(log_conf.shape)-1)))
        dump_Q = (len(topo_chg)==len(log_time))
        if dump_Q: head += ' {:>14s}'.format('Q/cell')
        with open(archive_file,log_mode) as fw:
            if log_mode=='w': fw.write(head+'\n')
            for i in range(len(log_time)):
                fw.write(fmt.format(log_time[i],log_ener[i],dE))
                fw.write(('{:14.7f} '*3).format(*tuple(mm[i])))
                if dump_Q: fw.write('{:14.7f}'.format(topo_chg[i]))
                fw.write('\n')




class llg_solver():
    def __init__(self,
        alpha=0.1,dt=1e-3,nstep=20000,
        S_values=np.array([1/2]),
        g_factor=2,
        temperature=0.,
        lat_type='unknown',
        name = 'simple LLG simulation',
        prefix = None,
        start_conf = 'as_input',
        fix_boundary_spin=False,
        conv_forc=1e-8,conv_ener=1e-7,conv_ener_count=2,
        damping_only=False,
        thermal_field_method=1,
        rank_root = 0,
        log_handle = log_handle,
        free_root = False):

        self._name = name
        self._alpha = alpha  # the Gilbert damping parameter
        self._dt = dt        # time step in ps
        self._nstep = nstep  # max step number for iteration

        self._S_values = S_values   # spin quantum number, S=1/2 corresponds to 1 mu_B
        self._g_factor = g_factor

        self._lat_type = lat_type              # lattice type, useless indeed
        self._fix_boundary_spin = fix_boundary_spin    # fix spins at the boundary
        self._start_conf = start_conf

        self._damping_only = damping_only

        self._conv_forc = conv_forc
        self._conv_ener = conv_ener
        self._conv_ener_count = conv_ener_count   # to avoid "accidental convergence"
        self._llg_time = np.arange(0,self._dt*(self._nstep+1),self._dt)
        self._temperature = temperature
        self._thermal_factor = 2*self._alpha*kB*self._temperature*muB/gamma_e/self._dt
        self._factor = gamma_e/(1+self._alpha**2)
        self._thermal_field_method = thermal_field_method

        self.set_log_handle(log_handle)
        self._rank_root = rank_root
        self._free_root = free_root  # if True, root process only servers as communicator

        print_thermal_field_method_warning(self._thermal_field_method)


    def __copy__(self):  return copy(self)


    def __deepcopy__(self, memo):   return copy.deepcopy(self)


    def set_verbosity(self,verbosity):
        err = 'LLG_solver: You try to set verbosity = {}, it should be an non-negative integer!'.format(verbosity)
        assert type(verbosity)==int and verbosity>=0, err
        self._verbosity = verbosity


    def set_log_handle(self,log_handle):
        self._log_handle = log_handle
        self.__dict__.update(log_handle.__dict__)
 

    def prepare_thermal_field(self,sp_lat):
        shape = sp_lat.shape

        if self._thermal_field_method == 1:  B_th = np.random.normal(size=shape) 
        if self._thermal_field_method == 2:  B_th = gen_normal_random_spin(n=np.prod(shape[:-1])).reshape(shape)

        for iat in range(shape[-2]):
            B_th[...,iat,:] *= np.sqrt(self._thermal_factor*self._g_factor*self._S_values[iat])  # in unit of meV
            B_th[...,iat,:] /= self._g_factor*self._S_values[iat]*muB  # in unit of Tesla
        return B_th


    def calc_A_vec(self,ham,sp_lat,dyn_idx,damping_only=False):
        shape = sp_lat.shape
        ntask = len(dyn_idx)

        B_th = np.zeros_like(sp_lat)
        if self._temperature: B_th = self.prepare_thermal_field(sp_lat)

        A_vec_predict = np.zeros((ntask,3),float)
        sp_lat_predict_full = copy.copy(sp_lat)  # all sites, either fixed or dyanmic

        for nn,idx0 in enumerate(dyn_idx):
            n_i = sp_lat_predict_full[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat,idx0) + B_th[tuple(idx0)]
            if damping_only: A_vec_predict[nn] = self._alpha*self._factor*np.cross(n_i,B_eff)
            else:            A_vec_predict[nn] = self._factor* (B_eff + self._alpha*np.cross(n_i,B_eff))
            mat = RT.from_rotvec(A_vec_predict[nn]*self._dt).as_matrix()
            sp_lat_predict_full[tuple(idx0)] = np.dot(mat,n_i)

        for nn,idx0 in enumerate(dyn_idx):
            n_i = sp_lat_predict_full[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat_predict_full,idx0) + B_th[tuple(idx0)]
            if damping_only: A_vec_predict[nn] += self._alpha*self._factor*np.cross(n_i,B_eff)
            else:            A_vec_predict[nn] += self._factor* (B_eff + self._alpha*np.cross(n_i,B_eff))

        A_vec_all = A_vec_predict/2
        return A_vec_all


    def mpi_calc_A_vec(self,ham,sp_lat,dyn_idx,gather=True,damping_only=False):
        shape = sp_lat.shape
        ntask = len(dyn_idx)
        comm,size,rank,node = mt.get_mpi_handles()

        B_th = np.zeros_like(sp_lat)
        if self._temperature and rank==self._rank_root: B_th = self.prepare_thermal_field(sp_lat)
        B_th = comm.bcast(B_th,root=self._rank_root)

        start,last = mt.assign_task(ntask,size,rank, self._free_root)
        A_vec_predict = np.zeros((last-start,3))
        sp_lat_predict = np.zeros((last-start,3))

        sp_lat_predict_full = copy.copy(sp_lat)  # all sites, either fixed or dyanmic

        for nn,idx0 in enumerate(dyn_idx[start:last]):
            n_i = sp_lat_predict_full[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat,idx0) + B_th[tuple(idx0)]
            if damping_only: A_vec_predict[nn] = self._alpha*self._factor*np.cross(n_i,B_eff)
            else:            A_vec_predict[nn] = self._factor* (B_eff + self._alpha*np.cross(n_i,B_eff))
            mat = RT.from_rotvec(A_vec_predict[nn]*self._dt).as_matrix()
            sp_lat_predict[nn] = np.dot(mat,n_i)

        comm.barrier()
        sp_lat_predict = comm.gather(sp_lat_predict,root=self._rank_root)
        if rank==self._rank_root: 
            sp_lat_predict = np.concatenate(sp_lat_predict,axis=0)
            for ii,idx0 in enumerate(dyn_idx): sp_lat_predict_full[tuple(idx0)] = sp_lat_predict[ii]
        sp_lat_predict_full = comm.bcast(sp_lat_predict_full,root=self._rank_root)
        for nn,idx0 in enumerate(dyn_idx[start:last]):
            n_i = sp_lat_predict_full[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat_predict_full,idx0) + B_th[tuple(idx0)]
            if damping_only: A_vec_predict[nn] += self._alpha*self._factor*np.cross(n_i,B_eff)
            else:            A_vec_predict[nn] += self._factor* (B_eff + self._alpha*np.cross(n_i,B_eff))

        A_vec_all = A_vec_predict/2
        if gather:
            A_vec_all = comm.allgather(A_vec_all)
            A_vec_all = np.concatenate(A_vec_all,axis=0)
        return A_vec_all


    def mpi_calc_A_vec_shared_memory(self,ham,A_vec_all,sp_lat,sp_lat_predict,B_th,dyn_idx,gather=True,damping_only=False):
        import mpi4py.MPI as MPI
        shape = sp_lat.shape
        ntask = len(dyn_idx)
        comm,size,rank,node = mt.get_mpi_handles()
        nodes_root = get_nodes_root(comm,size,rank,node)
        start,last = mt.assign_task(ntask,size,rank, self._free_root)
        #itemsize = MPI.DOUBLE.Get_size()
        #nbytes = itemsize*np.prod(shape)

        if self._temperature and rank==self._rank_root: B_th[:] = self.prepare_thermal_field(sp_lat)
        B_th = comm.bcast(B_th,root=self._rank_root)

        if rank==self._rank_root: sp_lat_predict[:] = sp_lat
        sp_lat_predict = comm.bcast(sp_lat_predict,root=self._rank_root)

        comm.barrier()
        for nn,idx0 in enumerate(dyn_idx[start:last]):
            n_i = sp_lat[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat,idx0) + B_th[tuple(idx0)]
            if damping_only: A_vec_all[tuple(idx0)] = self._alpha*self._factor*np.cross(n_i,B_eff)
            else:            A_vec_all[tuple(idx0)] = self._factor* (B_eff + self._alpha*np.cross(n_i,B_eff))
            mat = RT.from_rotvec(A_vec_all[tuple(idx0)]*self._dt).as_matrix()
            sp_lat_predict[tuple(idx0)] = np.dot(mat,n_i)

        comm.barrier()
        for nn,idx0 in enumerate(dyn_idx[start:last]):
            n_i = sp_lat_predict[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat_predict,idx0) + B_th[tuple(idx0)]
            if damping_only: A_vec_all[tuple(idx0)] += self._alpha*self._factor*np.cross(n_i,B_eff)
            else:            A_vec_all[tuple(idx0)] += self._factor* (B_eff + self._alpha*np.cross(n_i,B_eff))

        A_vec_all = A_vec_all/2
        return A_vec_all


    def llg_one_step(self,ham,sp_lat,dyn_idx):
        new_sp_lat=np.zeros_like(sp_lat)
        A_vec_all = self.calc_A_vec(ham,sp_lat,dyn_idx,damping_only=self._damping_only)
        force=None
        if self._log_force:
            if self._damping_only: force = A_vec_all
            else: force = self.calc_A_vec(ham,sp_lat,dyn_idx,damping_only=True)
        for nn,idx0 in enumerate(dyn_idx):
            rot_mat = RT.from_rotvec(A_vec_all[nn]*self._dt).as_matrix()
            new_sp_lat[tuple(idx0)] = np.dot(rot_mat,sp_lat[tuple(idx0)])
        return A_vec_all,force,copy.copy(new_sp_lat)


    def verbose_llg_setup(self,nx,ny,nz,nat,nsites_dyn,ncore=None,verbose_alpha=True,verbose_end=True):
        print ('\n{0}\nLLG simulation setup: start\n{0}\n'.format('*'*60))
        print ('{0} lattice'.format(self._lat_type))
        if self._fix_boundary_spin: print ('Spins at the boundary are fixed')
        nsites = nx*ny*nz*nat
        print ('nx = {0}, ny = {1}, nz = {2}, nat = {3}'.format(nx,ny,nz,nat))
        print ('{} sites in total'.format(nx*ny*nat))
        print ('{} sites for dynamics'.format(nsites_dyn))
        print ('See dyn_idx.dat for index of sites for dynamics')
        if nsites!=nsites_dyn: print ('some spin sites are fixed, check your setup carefully')
        data_size = 2*nx*ny*nz*nat*3
        if ncore is not None:
            if ncore>1: print ('parallel on {0} cores'.format(ncore))
            else: print ('Run in parallel mode but only one core invoked')
            data_size += (nx*ny*nz*nat*3)/ncore
        else:
            print ('serial mode')
            data_size += nx*ny*nz*nat*3

        print ('Estimated required minimum memory = {:10.5f} MB / core'.format(data_size/1024**2))
        print ('\nUse Depondt\'s solver for numerical integration\n')
        if self._damping_only:
            print ('\n*** !!! Important note !!! ***')
            print ('You set damping_only = True')
            print ('Precession is supressred in the spin dynamics simulation')
            print ('In this way LLG works like an energy minimizer')
            print ('Make sure that this is what you want\n')
            if self._temperature>0: 
                print ('Warning: you set damping_only mode for a finite temperature LLG')
                print ('The results might be silly and meaningless')
                print ('Simulation won\'t be run')
                exit()
        if verbose_alpha:
            print ('damping factor alpha = {}'.format(self._alpha))
            print ('gamma_e/(1+alpha**2) = {}\n'.format(self._factor))
        print ('time step            = {:10.4f} fs'.format(self._dt*1e3))
        print ('max iteration steps  = {0:10d}'.format(self._nstep))
        print ('max simulation time  = {:10.4f} ps'.format(self._dt*self._nstep))
        print ('energy convergence threhold = {:6.3e} meV/site'.format(self._conv_ener))
        if self._temperature>1e-4:
            print ('\nSimulation performed at finite temperature')
            print ('Note that this is a stochastic LLG simulation')
            print ('T = {:10.5f} K'.format(self._temperature))
            print ('T ~ {:10.5f} meV'.format(kB*self._temperature))
            print ('T ~ {:10.5f} Tesla'.format(kB*self._temperature/muB))
            print ('Thermal field generation method = {}'.format(self._thermal_field_method))
            print ('See the source code for details')
        else:
            print ('Determinstic LLG at zero Kelvin')
        
        self._log_handle.verbose_logging_info()
        if verbose_end: print ('\n{0}\nLLG simulation setup: end\n{0}\n\n'.format('*'*60))
        sys.stdout.flush()



    def pre_LLG(self,ham,sp_lat,size=1,shared_memory=False,solver='simple'):
        self._log_handle.prepare_logging_dir()
        nx,ny,nz,nat,dyn_idx = get_latt_idx(sp_lat.shape,self._fix_boundary_spin,savetxt=True,outdir=self._outdir)
        ntask = len(dyn_idx)
        log_spin_hamiltonian(ham,sp_lat,self._log_ham_file)
        pkginfo = pkg_info().verbose_info()
        print ('\n{0}\n{1}{2}\n{0}\n'.format('='*60,llg_text,'{} LLG solver'.format(solver)))
        self.verbose_llg_setup(nx,ny,nz,nat,ntask,ncore=size)
        if size>1:
            print_oversize_warning(size,ntask,'mpi_llg_simulation')
            if shared_memory: 
                print_oversize_warning(size,ntask,'mpi_llg_simulation_shared_memory')
                print(shared_memory_warning)



    def first_step_LLG(self,ham,sp_lat,en0,force=None,Q=None,verbosity=1,func_name='mpi_llg_simulation'):
        fmt_head = '  {:>7s} {:>12s} {:>14s} '+'{:>16s} '*2+'{:>10s}'*3+'{:>14s}'
        tag_log = ['step','walltime(s)','LLG_time(ps)','E_tot(meV/site)','dE(meV/site)','Mx','My','Mz','max|H_i|']
        if force is not None: max_H = np.max(np.linalg.norm(force,axis=-1))
        else: max_H = -1
        nsites=np.prod(sp_lat.shape[:-1])
        log_time=[0]
        log_ener=[en0]
        log_conf=[copy.copy(sp_lat)]
        if Q is not None: log_Q=[Q]
        else: log_Q = []
        if verbosity:
            mm=np.average(sp_lat,axis=tuple(range(len(sp_lat.shape)-1)))
            print ('\n{0}\nLLG simulation: Start\n{0}\n'.format('*'*125))
            print ('Calling function {}'.format(func_name))
            print ('Started  at {0}\n'.format(time.ctime()))
            if force is None: print ('Note: force not calculated, but displayed as -1\n')
            print ('-'*125)
            print (fmt_head.format(*tuple(tag_log)))
            print ('-'*125)
            items = [0,0,0,en0,en0,mm[0],mm[1],mm[2],max_H]
            print (fmt_log.format(*tuple(items)))
            sys.stdout.flush()
            init_ovf = self._init_conf_file
            log_llg_data(log_time,log_ener,log_conf,log_conf_file=init_ovf,archive_file=None,dE=en0)
            log_llg_data(log_time,log_ener,log_conf,log_conf_file=self._log_conf_file,
            archive_file=self._archive_file,log_mode='w',topo_chg = log_Q,dE=en0)
        return log_time,log_ener,log_conf,log_Q


    def verbose_one_step_LLG(self,it,sp_lat,Etot_old,Etot_new,stime,force=None):
        diff_E = Etot_new-Etot_old
        if force is not None: max_H = np.max(np.linalg.norm(force,axis=-1))
        else: max_H = -1
        mm=np.average(sp_lat,axis=tuple(range(len(sp_lat.shape)-1)))
        print (fmt_log.format(it,time.time()-stime,self._llg_time[it],Etot_new,diff_E,mm[0],mm[1],mm[2],max_H))
        sys.stdout.flush()


    def finalize_LLG(self,run_steps,stime,log_time,log_ener,log_conf,verbosity,dE=0):
        print ('-'*125)
        print ('\nStop LLG simulation', end=' ')
        if run_steps==self._nstep: print ('because max iteration limitation')
        else: print ('because total energy convergence is achieved')
        if verbosity:
            print ('Finished at {}'.format(time.ctime()))
            print ('Time used : {:10.4f} s'.format(time.time()-stime))
            print ('Final energy = {:14.8f} meV/site'.format(log_ener[-1]))
            print ('\n{0}\nLLG simulation: End\n{0}\n'.format('*'*125))
        log_llg_data(log_time[-1:],log_ener[-1:],log_conf[-1:],log_conf_file=self._final_conf_file,archive_file=None,dE=dE)


    def llg_simulation(self,ham,sp_lat):
        sp_lat = initialize_spin_lattice(sp_lat,self._start_conf)
        check_sp_lat_norm(sp_lat)
        assert np.allclose(self._S_values, ham._S_values), 'S_values in LLG_solver and ham should be consistent'
        shape = sp_lat.shape
        nx,ny,nz,nat,dyn_idx = get_latt_idx(shape,self._fix_boundary_spin)
        nsites=np.prod(shape[:-1])
        if self._verbosity>1: self.pre_LLG(ham,sp_lat)

        if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
        else: sp_lat_log = copy.copy(sp_lat)
        if self._log_topo_chg: Q = calc_topo_chg(sp_lat_log,tri_simplices = self._tri_simplices)
        else: Q=None
        A_vec_all, force, sp_lat = self.llg_one_step(ham,sp_lat,dyn_idx)
        en0 = ham.calc_total_E(sp_lat,average_on_sites=True)
        log_time,log_ener,log_conf,log_Q = self.first_step_LLG(ham,sp_lat,en0,force,Q,self._verbosity,func_name='llg_simulation')

        stime=time.time()
        count = 0
        for it in range(1,self._nstep+1): 
            log_flag = (it%(max(1,self._n_log_magnetization))==0)
            if log_flag: Etot_old = ham.calc_total_E(sp_lat,average_on_sites=True)
            A_vec_all, force, sp_lat = self.llg_one_step(ham,sp_lat,dyn_idx)
            if log_flag:
                Etot_new = ham.calc_total_E(sp_lat,average_on_sites=True)

                force = None
                Q = None
                sp_lat_log = copy.copy(sp_lat)
                if self._log_force: force = self.calc_A_vec(ham,sp_lat,dyn_idx,damping_only=True)
                if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
                if self._log_topo_chg: Q = calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices)
     
                if self._log_topo_chg: log_Q.append(Q)
                dE = Etot_new - Etot_old
                log_ener.append(Etot_new)
                log_time.append(self._llg_time[it])
                log_conf.append(copy.copy(sp_lat_log))
                if self._verbosity: self.verbose_one_step_LLG(it,sp_lat_log,Etot_old,Etot_new,stime,force)
                if it%(max(1,self._n_log_configuration))!=0: fil_conf=None
                else: fil_conf = self._log_conf_file
                log_llg_data(log_time[-1:],log_ener[-1:],log_conf[-1:],fil_conf,self._archive_file,log_mode='a',topo_chg = log_Q[-1:],dE=dE)

                if abs(Etot_new-Etot_old) < self._conv_ener: count+=1
                if count == self._conv_ener_count: break
            run_steps=it
        self.finalize_LLG(run_steps,stime,log_time,log_ener,log_conf,self._verbosity,dE=Etot_new-Etot_old)
        return np.array(log_time),np.array(log_ener),np.array(log_conf)


    # the argument pinned_idx is still under developoment
    # it aims at pinning some spin sites during the LLG simulation
    # the variable pinned_idx should be an array of shape (N,M)
    # the first dim is no of sites spinned
    # the second is indices for each site (M=4 for 3D and M=3 for 2D)
    # in order of ix,iy,(iz),iat
    def mpi_llg_simulation(self,ham,sp_lat,pinned_idx=None):
        import mpi4py.MPI as MPI
        comm,size,rank,node = mt.get_mpi_handles()
        mt.inter_node_check(comm,rank,node)
        assert size>1 or self._free_root==False, 'Cannot run with free_root=True for single-core job!'
        if rank==self._rank_root: sp_lat = initialize_spin_lattice(sp_lat,self._start_conf)
        sp_lat = comm.bcast(sp_lat,root=self._rank_root)   # this extra step makes sure that all processes start from the same configuration
        shape = sp_lat.shape
        nx,ny,nz,nat,dyn_idx = get_latt_idx(shape,self._fix_boundary_spin,pinned_idx)
        nsites = np.prod(shape[:-1])
        ntask = len(dyn_idx)    # no. of sites directly involved in the dynamics

        check_sp_lat_norm(sp_lat)
        assert np.allclose(self._S_values, ham._S_values), 'S_values in LLG_solver and ham should be consistent'
        if rank==self._rank_root and  self._verbosity>1: self.pre_LLG(ham,sp_lat,size=size)

        kwargs1 = dict(gather=False,damping_only=self._damping_only)
        kwargs2 = dict(gather=True,damping_only=True)

        force = None
        Q = None
        sp_lat_log = copy.copy(sp_lat)
        if self._log_force: force = self.mpi_calc_A_vec(ham,sp_lat,dyn_idx,**kwargs2)
        if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
        if self._log_topo_chg: Q = mpi_calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices)
        en0 = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)
        log_time,log_ener,log_conf,log_Q = self.first_step_LLG(ham,sp_lat_log,en0,force,Q,verbosity=(rank==self._rank_root))

        stime=time.time()
        start,last = mt.assign_task(ntask,size,rank, self._free_root)
        updated_sp_lat = np.zeros((last-start,3),float)

        count = 0
        fil_archive = self._archive_file
        for it in range(1,self._nstep+1):
            log_flag = (it%(max(1,self._n_log_magnetization))==0)
            if log_flag:  Etot_old  = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)

            A_vec_all = self.mpi_calc_A_vec(ham,sp_lat,dyn_idx,**kwargs1)

            for nn,idx0 in enumerate(dyn_idx[start:last]):
                rot_mat = RT.from_rotvec(A_vec_all[nn]*self._dt).as_matrix()
                updated_sp_lat[nn] = np.dot(rot_mat,sp_lat[tuple(idx0)])
            comm.barrier()
            gather_sp_lat = comm.gather(updated_sp_lat,root=self._rank_root)
            if rank==self._rank_root:
                gather_sp_lat = np.concatenate(gather_sp_lat,axis=0)
                for ii,idx0 in enumerate(dyn_idx): sp_lat[tuple(idx0)] = gather_sp_lat[ii]
            sp_lat = comm.bcast(sp_lat,root=self._rank_root)

            if log_flag:
                if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
                else: sp_lat_log = copy.copy(sp_lat)
                if self._log_force: force = self.mpi_calc_A_vec(ham,sp_lat,dyn_idx,**kwargs2)
                if self._log_topo_chg: log_Q.append( mpi_calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices) )
                Etot_new = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)

                if rank==self._rank_root:
                    dE = Etot_new - Etot_old
                    log_ener.append(Etot_new)
                    log_time.append(self._llg_time[it])
                    log_conf.append(copy.copy(sp_lat_log))

                    if self._verbosity: self.verbose_one_step_LLG(it,sp_lat_log,Etot_old,Etot_new,stime,force)
                    if it%(max(1,self._n_log_configuration))!=0: fil_conf=None
                    else: fil_conf = self._log_conf_file
                    log_llg_data(log_time[-1:],log_ener[-1:],log_conf[-1:],fil_conf,fil_archive,log_mode='a',topo_chg = log_Q[-1:],dE=dE)

                    if abs(dE) < self._conv_ener: count+=1
                count = comm.bcast(count,root=self._rank_root)
                if count == self._conv_ener_count: break
        if rank==self._rank_root: self.finalize_LLG(it,stime,log_time,log_ener,log_conf,self._verbosity,dE=Etot_new-Etot_old)

        #MPI.finalize()
        return np.array(log_time),np.array(log_ener),log_conf


    def mpi_llg_simulation_shared_memory(self,ham,sp_lat_init,pinned_idx=None):
        import mpi4py.MPI as MPI
        comm,size,rank,node = mt.get_mpi_handles()
        mt.inter_node_check(comm,node,rank)
        assert size>1 or self._free_root==False, 'Cannot run with free_root=True for single-core job!'
        nodes_root = get_nodes_root(comm,size,rank,node)
        shape = sp_lat_init.shape
        nx,ny,nz,nat,dyn_idx = get_latt_idx(shape,self._fix_boundary_spin,pinned_idx)
        nsites = np.prod(shape[:-1])
        ntask = len(dyn_idx)    # no. of sites directly involved in the dynamics

        itemsize = MPI.DOUBLE.Get_size()
        nbytes = itemsize*np.prod(shape)

        win0 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
        buf, itemsize0 = win0.Shared_query(self._rank_root)
        assert itemsize0 == itemsize
        sp_lat = np.ndarray(buffer=buf, dtype='float', shape=shape)
        if rank in nodes_root: 
            sp_lat_init = initialize_spin_lattice(sp_lat_init,self._start_conf)
            sp_lat[:] = sp_lat_init

        win1 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
        buf, itemsize0 = win1.Shared_query(self._rank_root)
        assert itemsize0 == itemsize
        B_th = np.ndarray(buffer=buf, dtype='float', shape=shape)

        win2 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
        buf, itemsize0 = win2.Shared_query(self._rank_root)
        assert itemsize0 == itemsize
        sp_lat_predict = np.ndarray(buffer=buf, dtype='float', shape=shape)

        win3 = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
        buf, itemsize0 = win3.Shared_query(self._rank_root)
        assert itemsize0 == itemsize
        A_vec_all = np.ndarray(buffer=buf, dtype='float', shape=shape)

        comm.barrier()
        check_sp_lat_norm(sp_lat)
        assert np.allclose(self._S_values, ham._S_values), 'S_values in LLG_solver and ham should be consistent'
        if rank==self._rank_root and self._verbosity>1: self.pre_LLG(ham,sp_lat,size=size,shared_memory=True)

        kwargs1 = dict(gather=False,damping_only=self._damping_only)
        kwargs2 = dict(gather=True,damping_only=True)

        force = None
        Q = None
        sp_lat_log = copy.copy(sp_lat)
        if self._log_force: force = self.mpi_calc_A_vec_shared_memory(ham,A_vec_all,sp_lat,sp_lat_predict,B_th,dyn_idx,**kwargs2)
        if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
        if self._log_topo_chg: Q = mpi_calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices)
        en0 = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)
        log_time,log_ener,log_conf,log_Q = self.first_step_LLG(ham,sp_lat_log,en0,force,Q,verbosity=(rank==self._rank_root))

        stime=time.time()
        start,last = mt.assign_task(ntask,size,rank, self._free_root)
        comm.barrier()
        count = 0
        fil_archive = self._archive_file
        for it in range(1,self._nstep+1):
            log_flag = (it%(max(1,self._n_log_magnetization))==0)
            if log_flag:  Etot_old  = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)

            A_vec_all = self.mpi_calc_A_vec_shared_memory(ham,A_vec_all,sp_lat,sp_lat_predict,B_th,dyn_idx,**kwargs1)
            for nn,idx0 in enumerate(dyn_idx[start:last]):
                rot_mat = RT.from_rotvec(A_vec_all[tuple(idx0)]*self._dt).as_matrix()
                sp_lat[tuple(idx0)] = np.dot(rot_mat,sp_lat[tuple(idx0)])
            comm.barrier()
            if log_flag:
                if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
                else: sp_lat_log = copy.copy(sp_lat)
                if self._log_force: force = self.mpi_calc_A_vec(ham,sp_lat,dyn_idx,**kwargs2)
                if self._log_topo_chg: log_Q.append( mpi_calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices) )
                Etot_new = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)

                if rank==self._rank_root:
                    dE = Etot_new - Etot_old
                    log_ener.append(Etot_new)
                    log_time.append(self._llg_time[it])
                    log_conf.append(copy.copy(sp_lat_log))

                    if self._verbosity: self.verbose_one_step_LLG(it,sp_lat_log,Etot_old,Etot_new,stime,force)
                    if it%(max(1,self._n_log_configuration))!=0: fil_conf=None
                    else: fil_conf = self._log_conf_file
                    log_llg_data(log_time[-1:],log_ener[-1:],log_conf[-1:],fil_conf,fil_archive,log_mode='a',topo_chg = log_Q[-1:],dE=dE)

                    if abs(dE) < self._conv_ener: count+=1
                count = comm.bcast(count,root=self._rank_root)
                if count == self._conv_ener_count: break
        if rank==self._rank_root: self.finalize_LLG(it,stime,log_time,log_ener,log_conf,self._verbosity,dE=Etot_new-Etot_old)
        win0.Free()
        win1.Free()
        win2.Free()
        win3.Free()
        #MPI.finalize()
        return np.array(log_time),np.array(log_ener),log_conf



if __name__=='__main__':
    print ('Running script {}'.format(__file__))
    print ('{} A simple LLG simulator\n'.format(llg_text))
