#!/usr/bin/env python

#========================================================
#
# Self-developed code for LLG simulation
# use Depondt modified Heun method for
# numerical integration of the LLG equation
# Ref. Depondt and Mertens, J. Phys. 2009, 21, 336005
# See also: Phys. Rev. B 2019, 99, 224414
#
# This scirpt is a supplement to llg_simple
# with some advanced functionalities
# such as imhomogeneous or alternative magnetic fields
# thermal gradients, spin-transfer torques, etc.
#
# Shunhong Zhang <szhang2@ustc.edu.cn>
# Apr 01 2021
#
#=========================================================
#
#=========================================================
# TODO: use max change of local magnetic field 
# as convergence criteria
#=========================================================

from asd.core.constants import e_chg
from asd.core.llg_simple import *

td_field_notes='''
The function to calculate this td-field will be passed
via the parameter td_reginoal_field
This customized function can be defined by user
It should contain the variable current_llg_time 
as the first positional argument and possibly 
other time-independent positional arguments
which are passed to the solver via td_field_args'''


class llg_solver_adv(llg_solver):
    def __init__(self,
        alpha=0.1,dt=1e-3,nstep=20000,
        S_values=np.array([1/2]),
        g_factor=2,
        temperature=0.,
        lat_type='unknown',
        name = 'simple LLG simulation',
        prefix = None,
        fix_boundary_spin=False,
        conv_forc=1e-8,conv_ener=1e-7,conv_ener_count=2,
        damping_only=False,
        thermal_field_method=1,
        log_handle = log_handle,
        rank_root = 0,

        current_density = 0., 
        current_polarization = 0., 
        current_direction = np.array([1,0,1]), 
        M_s=1,

        td_regional_field = None,
        td_field_args = (),
        include_td_field_energy = False):

        #super(llg_solver_adv,self).__init__(
        super().__init__(
        alpha = alpha,
        dt = dt,
        nstep = nstep,
        S_values = S_values, 
        g_factor = g_factor,
        temperature = temperature,
        lat_type = lat_type,
        name = name,
        prefix = prefix,
        fix_boundary_spin = fix_boundary_spin,
        conv_forc = conv_forc,
        conv_ener = conv_ener,
        conv_ener_count = conv_ener_count,
        damping_only = damping_only,
        thermal_field_method = thermal_field_method,
        rank_root = rank_root,
        log_handle = log_handle)


        self._current_density      = current_density
        self._current_polarization = current_polarization
        self._current_direction    = current_direction
        self._u_factor = current_density*current_polarization*g_factor*muB/(2*e_chg*M_s)

        self._td_regional_field = td_regional_field  # a function to get time-dependent imhomogeneous field
        self._td_field_args = td_field_args          # arguments for the function td_reginoal_field besides currenet_llg_time
        self._include_td_field_energy = include_td_field_energy

        if np.array([self._alpha]).shape==(1,): self._site_alpha=False
        else: self._site_alpha=True


    def set_verbosity(self,verbosity):
        super().set_verbosity(verbosity)


    def verbose_llg_setup_advanced(self,nx,ny,nz,nat,nsites_dyn,ncore=None):
        self.verbose_llg_setup(nx,ny,nz,nat,nsites_dyn,
        ncore,verbose_alpha=(self._site_alpha==False),verbose_end=False)
        if self._site_alpha or self._td_regional_field is not None:
            print ('\n{0} Advanced setup for LLG simulations {0}\n'.format('*'*10))
        if self._site_alpha:
            print ('\nIt seems that you are using a site-dependent damping')
            print ('See alpha.dat for the site-dependent damping parameters\n')
            open('alpha.dat','w').write('\n'.join(['{:10.6f}'.format(a) for a in self._alpha.flatten()]))
        if self._td_regional_field is not None:
            print ('\nA time-dependent field is applied to the system')
            print (td_field_notes)
            print ('\nSet include_td_field_energy = {}'.format(self._include_td_field_energy))
            print ('Zeeman energy from the td_field')
            if self._include_td_field_energy: print ('is included in logged energy\n')
            else: print ('is not included in logged energy\n')
        print ('\n{0}\nLLG simulation setup: end\n{0}\n\n'.format('*'*60))
        sys.stdout.flush()


    def get_instant_regional_field(self,current_llg_time):
        return self._td_regional_field(current_llg_time,*self._td_field_args)


    def calc_en_td_field(self,ham,sp_lat,it=0):
        if self._td_regional_field is None: return 0
        shape = sp_lat.shape
        instant_field = self.get_instant_regional_field(self._llg_time[it])
        if len(shape)==4: en_td_field = np.einsum('xyad,xyad,a',sp_lat,instant_field,self._S_values)
        if len(shape)==5: en_td_field = np.einsum('xyzad,xyzad,a',sp_lat,instant_field,self._S_values)
        en_td_field *= self._g_factor*muB
        return en_td_field


    def first_step_LLG_advanced(self,ham,sp_lat,en0,force=None,Q=None,verbosity=1,func_name='mpi_llg_simulation'):
        results = self.first_step_LLG(ham,sp_lat,en0,force,Q,verbosity,func_name)
        log_time,log_ener,log_conf,log_Q = results
        if self._include_td_field_energy: log_ener[0] += self.calc_en_td_field(ham,sp_lat,it=0)/np.prod(sp_lat.shape[:-1])
        return log_time,log_ener,log_conf,log_Q


    def prepare_thermal_field_advanced(self,sp_lat):
        shape = sp_lat.shape
        if self._thermal_field_method == 1:   B_th = np.random.normal(size=shape) 
        if self._thermal_field_method == 2:   B_th = gen_normal_random_spin(n=np.prod(shape[:-1])).reshape(shape)

        for iat in range(shape[-2]):
            B_th[...,iat,:] *= np.sqrt(self._thermal_factor[...,iat]*self._g_factor*self._S_values[iat])  # in unit of meV
            B_th[...,iat,:] /= self._g_factor*self._S_values[iat]*muB  # in unit of Tesla
        return B_th

 
    def mpi_calc_A_vec_advanced(self,ham,sp_lat,dyn_idx,gather=True,damping_only=False,it=0):
        import asd.mpi.mpi_tools as mt
        shape = sp_lat.shape
        ntask = len(dyn_idx)
        comm,size,rank,node = mt.get_mpi_handles()

        B_th = np.zeros_like(sp_lat)
        if self._temperature and rank==self._rank_root: B_th = prepare_thermal_field_advanced(sp_lat)
        B_th = comm.bcast(B_th,root=self._rank_root)

        start,last=mt.assign_task(ntask,size,rank)
        A_vec_all = np.zeros((last-start,3),float)
        A_vec_predict = np.zeros((last-start,3),float)
        sp_lat_predict = np.zeros((last-start,3),float)

        sp_lat_predict_full = copy.copy(sp_lat)  # all sites, either fixed or dyanmic

        td_field = None
        if self._td_regional_field is not None: td_field = self.get_instant_regional_field(self._llg_time[it])

        for nn,idx0 in enumerate(dyn_idx[start:last]):
            n_i = sp_lat_predict_full[tuple(idx0)]
            B_eff = ham.calc_local_B_eff(sp_lat,idx0) + B_th[tuple(idx0)]
            if self._site_alpha:
                alpha = self._alpha[tuple(idx0)]
                factor = self._factor[tuple(idx0)]
            else:
                alpha=self._alpha
                factor=self._factor
            if td_field is not None: B_eff += td_field[tuple(idx0)]
            if damping_only: A_vec_predict[nn] = alpha*factor*np.cross(n_i,B_eff)
            else:            A_vec_predict[nn] = factor* (B_eff + alpha*np.cross(n_i,B_eff))
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
            if self._site_alpha:
                alpha = self._alpha[tuple(idx0)]
                factor = self._factor[tuple(idx0)]
            else:
                alpha=self._alpha
                factor=self._factor
            B_eff = ham.calc_local_B_eff(sp_lat_predict_full,idx0) + B_th[tuple(idx0)]
            if td_field is not None: B_eff += td_field[tuple(idx0)]
            if damping_only: A_vec_predict[nn] += alpha*factor*np.cross(n_i,B_eff)
            else:            A_vec_predict[nn] += factor* (B_eff + alpha*np.cross(n_i,B_eff))

        A_vec_all = A_vec_predict/2

        if gather:
            A_vec_all = comm.allgather(A_vec_all)
            A_vec_all = np.concatenate(A_vec_all,axis=0)
        return A_vec_all


    def mpi_llg_simulation_advanced(self,ham,sp_lat,pinned_idx=None):
        import asd.mpi.mpi_tools as mt
        comm,size,rank,node = mt.get_mpi_handles()
        mt.inter_node_check(comm,node,rank)
        sp_lat = comm.bcast(sp_lat,root=self._rank_root)   # this extra step makes sure that all processes start from the same configuration
        shape = sp_lat.shape
        nx,ny,nz,nat,dyn_idx = get_latt_idx(shape,self._fix_boundary_spin,pinned_idx)
        nsites = np.prod(shape[:-1])
        ntask = len(dyn_idx)    # no. of sites directly involved in the dynamics

        if rank==self._rank_root: 
            check_sp_lat_norm(sp_lat)
            assert np.allclose(self._S_values, ham._S_values), 'S_values in LLG_solver and ham should be consistent'
            if self._verbosity>1: self.pre_LLG(ham,sp_lat,size=size,solver='advanced')

        kwargs1 = dict(gather=False,damping_only=self._damping_only)
        kwargs2 = dict(gather=True,damping_only=True)

        force = None
        Q = None
        sp_lat_log = copy.copy(sp_lat)
        if self._log_force: force = self.mpi_calc_A_vec_advanced(ham,sp_lat,dyn_idx,it=0,**kwargs2)
        if ham._spin_coord is not None: sp_lat_log = np.dot(sp_lat,ham._spin_coord)
        if self._log_topo_chg: Q = mpi_calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices)
        en0 = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)
 
        log_time,log_ener,log_conf,log_Q = self.first_step_LLG_advanced(ham,sp_lat_log,en0,force,Q,verbosity=(rank==self._rank_root))

        stime=time.time()
        start,last = mt.assign_task(ntask,size,rank)
        updated_sp_lat = np.zeros((last-start,3),float)

        count = 0
        for it in range(1,self._nstep+1):
            log_flag = (it%(max(1,self._n_log_magnetization))==0)
            if log_flag:  
                Etot_old  = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)
                if self._include_td_field_energy: Etot_old += self.calc_en_td_field(ham,sp_lat,it=it)/nsites

            A_vec_all = self.mpi_calc_A_vec_advanced(ham,sp_lat,dyn_idx,it=it,**kwargs1)

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

                if self._log_force: force = self.mpi_calc_A_vec_advanced(ham,sp_lat,dyn_idx,it=it,**kwargs2)
                if self._log_topo_chg: log_Q.append( mpi_calc_topo_chg_one_conf(sp_lat_log,tri_simplices = self._tri_simplices) )
                Etot_new = ham.calc_total_E(sp_lat,parallel=True,average_on_sites=True)
                if self._include_td_field_energy: Etot_new += self.calc_en_td_field(ham,sp_lat,it=it)/nsites

                if rank==self._rank_root:
                    dE = Etot_new - Etot_old
                    log_ener.append(Etot_new)
                    log_time.append(self._llg_time[it])
                    log_conf.append(copy.copy(sp_lat_log))

                    if self._verbosity: self.verbose_one_step_LLG(it,sp_lat_log,Etot_old,Etot_new,stime,force)
                    fil_conf = {True:self._log_conf_file,False:None}[it%(max(1,self._n_log_configuration))==0]
                    log_llg_data(log_time[-1:],log_ener[-1:],log_conf[-1:],fil_conf,self._archive_file,log_mode='a',topo_chg = log_Q[-1:],dE=dE)

                    if abs(dE) < self._conv_ener: count+=1
                count = comm.bcast(count,root=self._rank_root)
                if count == self._conv_ener_count: break
        if rank==self._rank_root: self.finalize_LLG(it,stime,log_time,log_ener,log_conf,self._verbosity,dE=Etot_new-Etot_old)

        return np.array(log_time),np.array(log_ener),log_conf


if __name__=='__main__':
    print (llg_text)
    print ('Running script {}'.format(__file__))
    print ('Advanced LLG simulator')
