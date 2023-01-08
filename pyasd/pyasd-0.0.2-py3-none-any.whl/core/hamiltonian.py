#!/usr/bin/env python

#========================================================
#
# spin Hamiltonian for atomistic lattice
# See : Phys. Rev. B 2019, 99, 224414
#
# Shunhong Zhang <szhang2@ustc.edu.cn>
# Aug 07 2021
#
#=========================================================
#
# exchange couplings are grouped by shell
# exch_i (i=1,2,3...) are objects of shell_exchange class
# see shell_exchange.py for details
#
#=========================================================

# Aug 07, 2021: the SIA axis can be specified
# to do: multiple easy axis


from __future__ import print_function
import numpy as np
import sys
from asd.core.constants import muB,kB
from asd.core.shell_exchange import *
import copy


def calc_MAE(spin_energy_function,sp_lat,spin_coord=None,rotation_plane='xoz',collinear_magmom=None,max_deg=360,deg_step=5,verbosity=1):

    if collinear_magmom is not None:
        magmom_value_err = "map_MAE: collinear magmom can only have elements -1 or 1!"
        assert set(collinear_magmom.flatten()) in [{1},{-1},{-1.,1.}], magmom_value_err
    nx,ny,nat = sp_lat.shape[:-1]
    nsites = np.prod(sp_lat.shape[:-1])
    angles = np.arange(0,max_deg+deg_step*0.5,deg_step)
    cc = np.cos(np.deg2rad(angles))
    ss = np.sin(np.deg2rad(angles))
    ens = np.zeros_like(angles)

    for ian,angle in enumerate(angles):
        sp_lat = np.zeros_like(sp_lat)
        for ix,iy,iat in np.ndindex(nx,ny,nat): 
            if rotation_plane=='xoy': sp_lat[ix,iy,iat] = np.array([cc[ian],ss[ian],0])
            if rotation_plane=='xoz': sp_lat[ix,iy,iat] = np.array([cc[ian],0,ss[ian]])
            if rotation_plane=='yoz': sp_lat[ix,iy,iat] = np.array([0,cc[ian],ss[ian]])
            if collinear_magmom is not None: sp_lat[ix,iy,iat] *= collinear_magmom[ix,iy,iat]
        if spin_coord is not None: sp_lat = np.dot(sp_lat,np.linalg.inv(spin_coord))
        ens[ian] = spin_energy_function(sp_lat)

    if verbosity:
        fmt = 'Minimum energy in the {} plane: {:10.5f} meV/site'
        print (fmt.format(rotation_plane,np.min(ens)),end=' , ')
        if abs(np.max(ens)-np.min(ens))<1e-4: print ('isotropic')
        else: print ('at phi   = {:6.1f} deg'.format(angles[np.argmin(ens)]))
        fmt = 'Maximum energy in the {} plane: {:10.5f} meV/site'
        print (fmt.format(rotation_plane,np.max(ens)),end=' , ')
        if abs(np.max(ens)-np.min(ens))<1e-4: print ('isotropic')
        else: print ('at phi   = {:6.1f} deg'.format(angles[np.argmax(ens)]))
    MAE = ens - ens[0]
    return angles,MAE


def map_MAE_polar(angles,ens_xoy,ens_xoz,show=False,savefig=True,figname='MAE',title=None):
    import matplotlib.pyplot as plt
    angles_rad = np.deg2rad(angles)
    fig = plt.figure(figsize=(9,4))
    if title is not None: fig.suptitle(title,fontsize=14)
    ax = fig.add_subplot(1,2,1,projection='polar')
    ax.plot(angles_rad,ens_xoy,label='xoy',c='r')
    if np.max(ens_xoy)-np.min(ens_xoy)<1e-5: ax.set_yticks([-1,0,1])
    ax = fig.add_subplot(1,2,2,projection='polar')
    ax.plot(angles_rad,ens_xoz,label='xoz',c='g')
    if np.max(ens_xoz)-np.min(ens_xoz)<1e-5: ax.set_yticks([-1,0,1])
    fig.legend(loc='lower center')
    fig.tight_layout()
    if savefig: fig.savefig(figname,dpi=500)
    if show: plt.show()
    return fig



def map_MAE_spheric(ens_map,
    map_shape=True,show=False,savefig=True,figname='map_MAE',
    display_mode=None,show_minima=True,alpha=0.5,
    cmap='viridis',scatter_size=10,phis=None,thetas=None):

    from asd.utility.plot_tools_3d import map_sphere_on_2d, map_3d_surface, map_sphere_on_2d_Kavrayskiy
    if display_mode is not None:
        print ('Display mode = {}'.format(display_mode))
        if '3d' in display_mode.lower():
            figname+='_3d'
            fig = map_3d_surface(ens_map,map_shape=map_shape,alpha=alpha,show=show,cmap=cmap)
        if '2d' in display_mode.lower():
            figname += '_2d'
            if 'kav' in display_mode.lower():
                print ('2D plot with Kavaryskiy projection')
                fig = map_sphere_on_2d_Kavrayskiy(ens_map,cmap,scatter_size)
            else:
                polar = ('polar' in display_mode.lower())
                fig = map_sphere_on_2d(ens_map,polar=polar,show_minima=show_minima,show=show,cmap=cmap,phis=phis,thetas=thetas)
        if savefig: fig.savefig(figname,dpi=500)
    else: fig = None
    return fig



# Currently we support biquadratic exchange shell
# when it is given explicitly, the contribution to total energy and efffective field
# will be included to the Hamiltonian

# boundary condition: 1 for periodic and 0 for open boundary

class spin_hamiltonian():
    def __init__(self,
        name = 'spin_ham',
        desc = 'spin hamiltonian',
        Bfield=np.zeros(3),
        S_values=np.array([1/2]),
        BL_SIA=[], BL_SIA_axis=[np.array([0,0,1])],
        BQ_SIA=[], BQ_SIA_axis=[np.array([0,0,1])],
        BL_exch=[],BQ_exch=[],general_exch=[],
        g_factor=2,
        spin_coord = None,
        iso_only=False,
        from_sym_mat=False,
        exchange_in_matrix=False,
        boundary_condition=[1,1,1],
        regional_field = None ):

        self._name = name
        self._desc = desc
        self._Bfield = Bfield                   #   homogeneous magnetic field
        self._regional_field = regional_field   # imhomogeneous magnetic field in Telsa, passed upon initialization

        self._S_values = S_values   # spin quantum number, S=1/2 corresponds to 1 mu_B
        self._g_factor = g_factor
        self._spin_coord = spin_coord # coordinate framework for spin vectors
        self._nat = len(S_values)

        self._BL_SIA = []       # single ion anisotropy
        self._BQ_SIA = []       # single ion anisotropy in biquadratic form
        self._BL_SIA_axis = []
        self._BQ_SIA_axis = []
        self._naxis_bl = 0 
        self._naxis_bq = 0

        for iaxis,sia in enumerate(BL_SIA): self.add_axial_single_ion_anisotropy(sia,BL_SIA_axis[iaxis],'BL')
        for iaxis,sia in enumerate(BQ_SIA): self.add_axial_single_ion_anisotropy(sia,BQ_SIA_axis[iaxis],'BQ')

        self._BL_exch = []
        self._BQ_exch = []
        self._general_exch = []
        self._nshell_BL = len(self._BL_exch)
        self._nshell_BQ = len(self._BQ_exch)
        self._nshell_general = len(self._general_exch)
        for exch in BL_exch: self.add_shell_exchange(exch,'BL')
        for exch in BQ_exch: self.add_shell_exchange(exch,'BQ')
        for exch in general_exch: self.add_shell_exchange(exch,'general')

        self._iso_only = iso_only
        self._from_sym_mat = from_sym_mat
        self._exchange_in_matrix = exchange_in_matrix
        self.set_boundary_condition(boundary_condition)
        self.sanity_check_exchange()


    def sanity_check_exchange(self):
        for exch in self._BL_exch + self._BQ_exch:
            assert len(exch._neigh_idx) == self._nat, 'No. of sites in {} inconsistent with No. of sites!'.format(exch._shell_name)
            if self._iso_only: assert len(exch._J_iso) == self._nat, 'No. of isotropic exchanges in {} inconsistent with No. of sites!'.format(exch._shell_name)
        for exch in self._BL_exch:
            if hasattr(exch,'_Jmat'):
                if exch._Jmat is None: continue
                nn = len(exch._Jmat)
                assert nn == self._nat, 'No. of tensorial exchanges in {} inconsistent with No. of sites!'.format(exch._shell_name)
        for exch in self._BQ_exch:
            nn = len(exch._BQ)
            assert nn == self._nat, 'No. of tensorial exchanges in {} inconsistent with No. of sites!'.format(exch._shell_name)


    # add an axial single-ion anisotropy to the spin Hamiltonian
    def add_axial_single_ion_anisotropy(self,SIA,SIA_axis,order='BL'):
        assert len(SIA) == self._nat, 'No. of SIA inconsistent with No. of sites!'
        if len(SIA_axis.shape)==1: SIA_axes = np.tile(SIA_axis/np.linalg.norm(SIA_axis),(self._nat,1))
        else: SIA_axes = (SIA_axis.T/np.linalg.norm(SIA_axis,axis=1)).T

        if order=='BL':
            self._BL_SIA.append(SIA)
            self._BL_SIA_axis.append(SIA_axes)
            self._naxis_bl += 1
        if order=='BQ':
            self._BQ_SIA.append(SIA)
            self._BQ_SIA_axis.append(SIA_axes)
            self._naxis_bq += 1


    def add_shell_exchange(self,exch,exch_type='BL'):
        if exch_type=='BL':
            self._BL_exch.append(exch)
            self._nshell_BL += 1
        if exch_type=='BQ':
            self._BQ_exch.append(exch)
            self._nshell_BQ += 1
        if exch_type=='general':
            self._general_exch.append(exch)
            self._nshell_general += 1


    def set_boundary_condition(self,boundary_condition=[1,1,1]):
        self._boundary_condition = boundary_condition

    def get_boundary_condition(self):
        return self._boundary_condition  


    def verbose_all_interactions(self,verbose_file=None):
        if verbose_file is not None: fw=open(verbose_file,'w')
        else: fw=None
        print ('\n{0}\nGeneral information of the spin Hamiltonian\n{0}'.format('-'*80),file=fw)
        print ('Boundary condition {}'.format(self._boundary_condition),file=fw)
        print ('1 for periodic and 0 for open boundary',file=fw)
        if self._spin_coord is not None:
            print ('!!!!!Caution!!!!!!!!!',file=fw)
            print ('You use the argument spin_coord',file=fw)
            print ('spin vectors will be expressed in this coord system',file=fw)
            print ('So do the spin-spin and spin-field interactions',file=fw)
            print ('check it with caution',file=fw)
            print ((('{:10.3f} '*3+'\n')*3+'\n').format(*tuple(self._spin_coord.flatten())),file=fw)
            print ('Note: when dumping the spin configurations\nand calculating the topological charges',file=fw)
            print ('We still use the Cartesian coordinate',file=fw)
            print ('So that the post-processing is more convenient\n',file=fw)
        print ('Set g factor = {:5.2f} (defalut is 2)'.format(self._g_factor),file=fw)
        ndim = len(self._Bfield)
        if ndim==2: print (('Magnetic field = [{:8.3f}, {:8.3f}] T  <-- cartesian coord').format(*tuple(self._Bfield)),file=fw)
        if ndim==3: print (('Magnetic field = [{:8.3f}, {:8.3f}, {:8.3f}] T  <-- cartesian coord').format(*tuple(self._Bfield)),file=fw)
 
        if self._spin_coord is not None:
            H_trans = np.dot(self._Bfield,np.linalg.inv(self._spin_coord))
            print (('Magnetic field = [{:8.3f}, {:8.3f}, {:8.3f}] T  <--      spin coord').format(*tuple(H_trans)),file=fw)

        if self._regional_field is not None:
            print ('Note: a regional field is exerted.\nMake sure it is what you want.',file=fw)
        print ('Mag. Moments at each site: (muB)',file=fw)
        print (' '.join(['{:5.2f} '.format(item) for item in self._S_values*2])+'\n',file=fw)
 
        print ('\n{0}\nMagnetic interactions in meV: Start\n{0}'.format('-'*80),file=fw)
        print ('\nImportant Note: we take the convention that',file=fw)
        print ('each term in the Hamiltonian has a negative sign ahead',file=fw)
        print ('Positive      (negative) value represents',file=fw)
        print ('ferromagnetic (antiferromagnetic) exchange couplings respectively',file=fw)
        print ('For single-ion part,\npositive     (negative) values favor\nout-of-plane (in-plane) magnetization respectively\n',file=fw)

        print ('\n{0}\nSingle ion part\n{0}'.format('*'*50),file=fw)
        if self._naxis_bl == self._naxis_bq == 0: print ('Not detected',file=fw)
        else:  print ('\nSingle ion anisotropy: ',file=fw)
        if self._naxis_bl:
            print ('\nBilinear\n',file=fw)
            print (('{:>8s} '*5).format('iat','SIA','A_x','A_y','A_z'),file=fw)
            for iaxis in range(self._naxis_bl):
                for iat in range(self._nat):
                    print (('{:8d} '+'{:8.3f} '*4).format(iat,self._BL_SIA[iaxis][iat],*tuple(self._BL_SIA_axis[iaxis][iat])),file=fw)
        if self._naxis_bq:
            print ('\nBiquadratic\n',file=fw)
            print (('{:>8s} '*5).format('iat','SIA','A_x','A_y','A_z'),file=fw)
            for iaxis in range(self._naxis_bq):
                for iat in range(nat):
                    print (('{:8d} '+'{:8.3f} '*4).format(iat,self._BQ_SIA[iaxis][iat],*tuple(self._BQ_SIA_axis[iaxis][iat])),file=fw)

        print ('\n{0}\nTwo-site part\n{0}'.format('*'*50),file=fw)
        if self._nshell_BL == self._nshell_BQ == 0: print ('Not detected',file=fw)
        if self._naxis_bl: print ('\nBilinear\n',file=fw)
        for exch in self._BL_exch: exch.verbose_interactions(self._from_sym_mat,self._exchange_in_matrix,file_handle=fw)
        if self._naxis_bq: print ('\nBiquadratic\n',file=fw)
        for exch in self._BQ_exch: exch.verbose_interactions(file_handle=fw)

        print ('\n{0}\nCustomized part\n{0}'.format('*'*50),file=fw)
        if self._nshell_general>0: 
            print ('Found some exchange couplings beyond',file=fw)
            print ('standard biliear and biquadratic two-site exchanges',file=fw)
            print ('They wont\' be presented  here',file=fw)
            print ('Please check your input manully',file=fw)
        else:
            print ('Not detected',file=fw)
        print ('\n{0}\nMagnetic interactions in meV: End\n{0}'.format('-'*80),file=fw)

        if verbose_file is not None:
            fw.flush()
            fw.close()
        else:
            sys.stdout.flush()


    def calc_self_exchange_energy(self,sp_lat):
        nat = sp_lat.shape[-2]
        E_SIA_bl = 0
        E_SIA_bq = 0
        assert nat==self._nat, 'self_exchange_energy: sp_lat nat ({}) should be equal to self._nat ({})!'.format(nat,self._nat)
        for iaxis in range(self._naxis_bl):
            proj_bl =np.zeros(sp_lat.shape[:-1])
            for iat in range(nat):
                proj_bl[...,iat] = np.dot(sp_lat[...,iat,:],self._BL_SIA_axis[iaxis][iat])
                E_SIA_bl += -np.sum(proj_bl[...,iat]**2 * self._BL_SIA[iaxis][iat])
        for iaxis in range(self._naxis_bq):
            proj_bq =np.zeros(sp_lat.shape[:-1])
            for iat in range(nat):
                proj_bq[...,iat] = np.dot(sp_lat[...,iat,:],self._BQ_SIA_axis[iaxis][iat])
                E_SIA_bq += -np.sum(proj_bq[...,iat]**4 * self._BQ_SIA[iaxis][iat])
        E_SIA = E_SIA_bl + E_SIA_bq
        return E_SIA


    def calc_zeeman_energy(self,sp_lat):
        E_zeeman = -np.sum(np.dot(np.dot(sp_lat,self._Bfield),self._S_values.T))*self._g_factor*muB
        return E_zeeman


    def calc_isotropic_total_E(self,sp_lat,parallel=False):
        E_iso_shell = np.zeros(self._nshell_BL)
        for i,exch in enumerate(self._BL_exch): 
            E_iso_shell[i] = exch.calc_shell_isotropic_exch_energy(sp_lat,self._boundary_condition,parallel)
        E_iso = np.sum(E_iso_shell)
        return E_iso


    def calc_total_E_general(self,sp_lat,interaction_resolved=False,shell_resolved=False):
        E_SIA = self.calc_self_exchange_energy(sp_lat)
        E_zeeman = self.calc_zeeman_energy(sp_lat)
        E_iso_shell    = np.zeros(self._nshell_BL)
        E_DMI_shell    = np.zeros(self._nshell_BL)
        E_Kitaev_shell = np.zeros(self._nshell_BL)
        E_bq_shell     = np.zeros(self._nshell_BQ)

        for i,exch in enumerate(self._BL_exch): E_iso_shell[i], E_DMI_shell[i], E_Kitaev_shell[i] = exch.calc_shell_exch_energy(sp_lat,self._boundary_condition)
        for i,exch in enumerate(self._BQ_exch): E_bq_shell[i] = exch.calc_shell_exch_energy(sp_lat,self._boundary_condition)

        E_iso = np.sum(E_iso_shell)
        E_DMI = np.sum(E_DMI_shell)
        E_Kitaev = np.sum(E_Kitaev_shell)
        E_bq = np.sum(E_bq_shell)

        E_tot = E_zeeman + E_SIA + E_iso + E_DMI + E_Kitaev + E_bq
        if interaction_resolved:
            if shell_resolved: return E_tot, E_Zeeman, E_SIA, E_iso_shell, E_DMI_shell, E_Kitaev_shell, E_bq_shell
            else: return E_tot, E_zeeman, E_SIA, E_iso, E_DMI, E_Kitaev, E_bq
        else: return E_tot


    def calc_total_E_from_sym_mat(self,sp_lat,interaction_resolved=False,shell_resolved=False):
        E_SIA = self.calc_self_exchange_energy(sp_lat)
        E_zeeman = self.calc_zeeman_energy(sp_lat)
        E_sym_shell = np.zeros(self._nshell_BL)
        E_DMI_shell = np.zeros(self._nshell_BL)
        E_bq_shell  = np.zeros(self._nshell_BQ)

        for i,exch in enumerate(self._BL_exch): E_sym_shell[i],E_DMI_shell[i] = exch.calc_shell_exch_energy_from_sym_mat(sp_lat,self._boundary_condition)
        for i,exch in enumerate(self._BQ_exch): E_bq_shell[i] = exch.calc_shell_exch_energy(sp_lat,self._boundary_condition)

        E_sym = np.sum(E_sym_shell)
        E_DMI = np.sum(E_DMI_shell)
        E_bq  = np.sum(E_bq_shell)

        E_tot = E_zeeman + E_SIA + E_sym + E_DMI + E_bq
        if interaction_resolved:
            if shell_resolved: return E_tot, E_Zeeman, E_SIA, E_sym_shell, E_DMI_shell, E_bq_shell
            else: return E_tot, E_zeeman, E_SIA, E_sym, E_DMI, E_bq
        else: return E_tot


    def calc_total_E_from_Jmat(self,sp_lat,interaction_resolved=False,shell_resolved=False,use_new_method=False,parallel=False):
        E_SIA = self.calc_self_exchange_energy(sp_lat)
        E_zeeman = self.calc_zeeman_energy(sp_lat)
        E_bl_shell = np.zeros(self._nshell_BL)
        E_bq_shell = np.zeros(self._nshell_BQ)

        for i,exch in enumerate(self._BL_exch): 
            if use_new_method: E_bl_shell[i] = exch.calc_shell_exch_energy_from_Jmat_new(sp_lat)
            else: E_bl_shell[i] = exch.calc_shell_exch_energy_from_Jmat(sp_lat,self._boundary_condition,parallel)
        for i,exch in enumerate(self._BQ_exch): E_bq_shell[i] = exch.calc_shell_exch_energy(sp_lat,self._boundary_condition,parallel)

        E_bl = np.sum(E_bl_shell)
        E_bq = np.sum(E_bq_shell)

        E_tot = E_zeeman + E_SIA + E_bl + E_bq
        if interaction_resolved:
            if shell_resolved: return E_tot, E_Zeeman, E_SIA, E_bl_shell, E_bq_shell
            else: return E_tot, E_zeeman, E_SIA, E_bl, E_bq
        else: return E_tot


    def calc_total_E(self,sp_lat,use_new_method=False,parallel=False,average_on_sites=True):
        from asd.core.spin_configurations import check_sp_lat_norm
        check_sp_lat_norm(sp_lat)
        if self._exchange_in_matrix:
            Etot = self.calc_total_E_from_Jmat(sp_lat,use_new_method,parallel=parallel)
        elif self._from_sym_mat:      
            Etot = self.calc_total_E_from_sym_mat(sp_lat)
        elif self._iso_only: 
            E_SIA = self.calc_self_exchange_energy(sp_lat)
            E_zeeman = self.calc_zeeman_energy(sp_lat)
            Etot = self.calc_isotropic_total_E(sp_lat,parallel=parallel)
            Etot+= E_SIA + E_zeeman
        else: 
            Etot = self.calc_total_E_general(sp_lat)
        if self._nshell_general>0:
            for exch in self._general_exch: Etot += exch.calc_shell_exch_energy(sp_lat,self._boundary_condition,parallel=parallel)
        if average_on_sites: Etot /= np.prod(sp_lat.shape[:-1])
        return Etot


    def verbose_reference_energy(self,sp_lat,file_handle=None,spin_coord=None):
        print ('\nEnergy for reference configurations (meV/site)\n',file=file_handle)
        if self._exchange_in_matrix or self._from_sym_mat: tags = ['E_tot','E_zeeman','E_SIA','E_symmetric','E_DMI','E_bq']
        else:               tags = ['E_tot','E_zeeman','E_SIA','E_heisenberg','E_DMI','E_Kitaev','E_bq']
        dirs = {0:'x',1:'y',2:'z'}
        en_ref = []
        shape=sp_lat.shape
        ndim = shape[-1]
        shape0 = np.array(shape)
        if 0 not in self._boundary_condition: shape0[:-2] = 1
        for i in range(ndim):
            uc_sp_lat = np.zeros(shape0,float)
            uc_sp_lat[...,i] = 1.
            if spin_coord is not None: uc_sp_lat = np.dot(uc_sp_lat,np.linalg.inv(spin_coord))
            if self._iso_only:
                E_SIA = self.calc_self_exchange_energy(uc_sp_lat)
                E_zeeman = self.calc_zeeman_energy(uc_sp_lat)
                E_iso = self.calc_isotropic_total_E(uc_sp_lat)
                Etot = E_SIA + E_zeeman + E_iso
                en = [Etot,E_zeeman,E_SIA,E_iso,0,0,0]
            elif self._exchange_in_matrix  or self._from_sym_mat:  
                en = self.calc_total_E_from_sym_mat(uc_sp_lat,interaction_resolved=True)
            else: 
                en = self.calc_total_E_general(uc_sp_lat,interaction_resolved=True)
            en_ref.append(en)
        en_ref = np.array(en_ref)/np.prod(uc_sp_lat.shape[:-1])
        print (('{:15s}'+'{:>15s}'*4+'\n{}').format('configuration','FM along x', 'FM along y', 'FM along z','MAE','-'*75),file=file_handle)
        for i in np.arange(1,len(tags)):
            print (('{:15s}'+'{:15.8f}'*ndim).format(tags[i],*tuple(en_ref[:,i])),end=' ',file=file_handle)
            print ('{:15.8f}'.format(en_ref[-1,i]-np.min(en_ref[:-1,i])),file=file_handle)
        print ('{0}'.format('-'*75),file=file_handle)
        print (('{:15s}'+'{:15.8f}'*ndim).format(tags[0],*tuple(en_ref[:,0])),end=' ',file=file_handle)
        print ('{:15.8f}\n'.format(en_ref[-1,0]-np.min(en_ref[:-1,0])),file=file_handle)
        if file_handle is not None: file_handle.flush()
        else: sys.stdout.flush()
        return en_ref


    def calc_SIA_exch_field(self,sp_lat,site_idx):
        shape = sp_lat.shape
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        SIA_B_eff = np.zeros(3)
        for iaxis in range(self._naxis_bl):
            proj_bl = np.dot(self._BL_SIA_axis[iaxis][iat],n_i)
            SIA_B_eff += 2*self._BL_SIA[iaxis][iat]*proj_bl*self._BL_SIA_axis[iaxis][iat]  # SIA contributed effective field
        for iaxis in range(self._naxis_bq):
            proj_bq = np.dot(self._SIA_bq_axis[iaxis][iat],n_i)
            SIA_B_eff += 4*self._BQ_SIA[iaxis][iat]*proj_bq**3*self._BQ_SIA_axis[iaxis][iat]
        return SIA_B_eff/(self._g_factor*self._S_values[iat]*muB)  # convert from meV to Tesla


    def calc_local_isotropic_B_eff(self,sp_lat,site_idx):
        shape = sp_lat.shape
        iat = site_idx[-1]
        B_eff = np.zeros(3)
        for exch in self._BL_exch: B_eff += exch.calc_shell_isotropic_exch_field(sp_lat,site_idx,self._boundary_condition)
        B_eff = B_eff/(self._g_factor*self._S_values[iat]*muB)  # convert from meV to Tesla
        return B_eff


    # local effective magnetic field is tne negative derivative of energy with respect to spin
    def calc_local_B_eff_general(self,sp_lat,site_idx):
        shape = sp_lat.shape
        iat = site_idx[-1]
        B_eff = np.zeros(3)
        for exch in self._BL_exch: B_eff += exch.calc_shell_exch_field(sp_lat,site_idx,self._boundary_condition)
        for exch in self._BQ_exch: B_eff += exch.calc_shell_exch_field(sp_lat,site_idx,self._boundary_condition)
        B_eff = B_eff/(self._g_factor*self._S_values[iat]*muB)  # convert from meV to Tesla
        return B_eff


    # local effective magnetic field is tne negative derivative of energy with respect to spin
    def calc_local_B_eff_from_sym_mat(self,sp_lat,site_idx):
        shape = sp_lat.shape
        iat = site_idx[-1]
        B_eff = np.zeros(3)
        for exch in self._BL_exch: B_eff += exch.calc_shell_exch_field_from_sym_mat(sp_lat,site_idx,self._boundary_condition)
        for exch in self._BQ_exch: B_eff += exch.calc_shell_exch_field(sp_lat,site_idx,self._boundary_condition)
        B_eff = B_eff/(self._g_factor*self._S_values[iat]*muB)  # convert from meV to Tesla
        return B_eff


    def calc_local_B_eff_from_Jmat(self,sp_lat,site_idx):
        shape = sp_lat.shape
        iat = site_idx[-1]
        n_i = sp_lat[tuple(site_idx)]
        B_eff = np.zeros(3)
        for exch in self._BL_exch: B_eff += exch.calc_shell_exch_field_from_Jmat(sp_lat,site_idx,self._boundary_condition)
        for exch in self._BQ_exch: B_eff += exch.calc_shell_exch_field(sp_lat,site_idx,self._boundary_condition)
        B_eff = B_eff/(self._g_factor*self._S_values[iat]*muB)  # convert from meV to Tesla
        return B_eff


    def calc_local_B_eff(self,sp_lat,site_idx):
        if self._exchange_in_matrix:    B_eff = self.calc_local_B_eff_from_Jmat(sp_lat,site_idx)
        elif self._from_sym_mat:        B_eff = self.calc_local_B_eff_from_sym_mat(sp_lat,site_idx)
        elif self._iso_only:            B_eff = self.calc_local_isotropic_B_eff(sp_lat,site_idx)
        else:                           B_eff = self.calc_local_B_eff_general(sp_lat,site_idx)

        if self._nshell_general:
            iat = site_idx[-1]
            for exch in self._general_exch: B_eff_general = exch.calc_shell_exch_field(sp_lat,site_idx)
            B_eff += B_eff_general/(self._g_factor*self._S_values[iat]*muB)  # convert from meV to Tesla
        B_eff+= self.calc_SIA_exch_field(sp_lat,site_idx)   # already in unit of Tesla

        # homogeneous Zeeman field
        B_eff += self._Bfield

        # imhomogeneous magnetic field
        shape = sp_lat.shape
        if self._regional_field is not None and self._regional_field.shape == shape:
            B_eff += self._regional_field[tuple(site_idx)]

        return B_eff


    def calc_local_energy(self,sp_lat,site_idx,spin_coord=None):
        if spin_coord is not None: sp_lat = np.dot(sp_lat,np.linalg.inv(spin_coord))
        shape = sp_lat.shape
        iat = site_idx[-1]
        n_i = copy.copy(sp_lat[tuple(site_idx)])
        E_SIA = 0
        for iaxis in range(self._naxis_bl):
            E_SIA -= self._BL_SIA[iaxis][iat] * np.dot(n_i,self._BL_SIA_axis[iaxis][iat])**2
        for iaxis in range(self._naxis_bq):
            E_SIA -= self._BQ_SIA[iaxis][iat] * np.dot(n_i,self._BQ_SIA_axis[iaxis][iat])**4
        E_zeeman = -np.dot(n_i, self._Bfield)*2*self._S_values[iat]*muB
        E_exch = 0.
        for exch in self._BL_exch: E_exch += exch.calc_local_exchange_energy(sp_lat,site_idx,self._boundary_condition)
        for exch in self._BQ_exch: E_exch += exch.calc_local_exchange_energy(sp_lat,site_idx,self._boundary_condition)
        for exch in self._general_exch: E_exch += exch.calc_local_exchange_energy(sp_lat,site_idx,self._boundary_condition)
        E_local = E_SIA + E_zeeman + E_exch
        return E_local


    def calculate_MAE(self,sp_lat,rotation_plane='xoz',collinear_magmom=None,max_deg=360,deg_step=5,verbosity=1):
        return calc_MAE(self.calc_total_E,sp_lat,self._spin_coord,rotation_plane,collinear_magmom,max_deg,deg_step,verbosity)


    # map the MAE for a 2D spin lattice and a given spin Hamiltonian
    def map_MAE(self,sp_lat,show=False,savefig=True,figname='MAE',collinear_magmom=None,max_deg=360,deg_step=5):
        angles,ens_xoy = self.calculate_MAE(sp_lat,'xoy',collinear_magmom,max_deg,deg_step)
        angles,ens_xoz = self.calculate_MAE(sp_lat,'xoz',collinear_magmom,max_deg,deg_step)
        fig = map_MAE_polar(angles,ens_xoy,ens_xoz,show,savefig,figname,self._name)
        return fig


    def map_MAE_3d(self,sp_lat,
        collinear_magmom=None,ntheta=20,nphi=60,
        map_shape=True,show=False,savefig=True,figname='map',
        display_mode='3d',show_minima=True,alpha=0.5,
        cmap='viridis',scatter_size=10):

        from asd.utility.plot_tools_3d import gen_grid_points_on_sphere
        nx,ny,nat = sp_lat.shape[:-1]
        thetas,phis,Rvec = gen_grid_points_on_sphere(nphi,ntheta)
        ens_map = np.zeros((ntheta,nphi))

        for itheta,iphi in np.ndindex(ntheta,nphi):
            sp_lat = np.zeros_like(sp_lat)
            for ix,iy,iat in np.ndindex(nx,ny,nat):
                sp_lat[ix,iy,iat] = Rvec[:,itheta,iphi]
                if collinear_magmom is not None: sp_lat[ix,iy,iat] *= collinear_magmom[ix,iy,iat]
            if self._spin_coord is not None: sp_lat = np.dot(sp_lat,np.linalg.inv(self._spin_coord))
            ens_map[itheta,iphi] = self.calc_total_E(sp_lat)/np.prod(sp_lat.shape[:-1])
        fig = map_MAE_spheric(ens_map,map_shape,show,savefig,figname,display_mode,show_minima,alpha,cmap,scatter_size,phis,thetas)
        return ens_map,fig


def log_spin_hamiltonian(ham,sp_lat,log_ham_file=None):
    ham.verbose_all_interactions(verbose_file=log_ham_file)
    if log_ham_file is not None:
        with open(log_ham_file,'a') as fw:
            ham.verbose_reference_energy(sp_lat,file_handle=fw)
    else:
        ham.verbose_reference_energy(sp_lat)
 

if __name__=='__main__':
    print ('Atomistic spin hamiltonian')
