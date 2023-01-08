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
import matplotlib.pyplot as plt
from matplotlib import gridspec
import time
import pickle
import glob
import copy
from asd.core.shell_exchange import get_latt_idx
from asd.core.spin_correlations import *
from asd.core.constants import *

meV_to_THz = 1e-3/(Hbar*1e12*2*np.pi)


def plot_struct_factor(qpt_cart,S_vector,figname='Struct_factor',colormap='parula',
    scatter_size=10,align='vertical',show=True,nqx=None,nqy=None):

    if colormap=='parula':
        from asd.utility.auxiliary_colormaps import parula
        colormap=parula

    gs = {'vertical':gridspec.GridSpec(3,1,height_ratios=(5,5,1)),
    'horizontal':gridspec.GridSpec(1,3,width_ratios=(5,5,1))}
    figsize =  {'vertical':(5,10),'horizontal':(10,5)}

    fig=plt.figure(figsize=figsize[align])
    ax= [ fig.add_subplot(gs[align][i]) for i in range(3)]

    vmin = np.min(S_vector)
    vmax = np.max(S_vector)
    S_normal = S_vector[:,0]+S_vector[:,1]
    S_parall = S_vector[:,2]
    if nqx is not None and nqy is not None:
        extent = [np.min(qpt_cart[:,0]),np.max(qpt_cart[:,0]),np.min(qpt_cart[:,1]),np.max(qpt_cart[:,1])]
        S_normal = S_normal.reshape(nqx,nqy)
        S_parall = S_parall.reshape(nqx,nqy)
        kwargs = dict(origin='lower',extent=extent,cmap=colormap,vmin=vmin,vmax=vmax)
        scat1 = ax[0].imshow(S_normal.T,**kwargs)
        scat2 = ax[1].imshow(S_parall.T,**kwargs)
    else:
        kwargs = dict(marker='o',s=scatter_size,cmap=colormap,vmin=vmin,vmax=vmax)
        scat1 = ax[0].scatter(*tuple(qpt_cart.T),c=S_normal,**kwargs)
        scat2 = ax[1].scatter(*tuple(qpt_cart.T),c=S_parall,**kwargs)

    if align=='vertical':   ax[1].set_xlabel('$q_x$')
    if align=='horizontal': ax[2].set_ylabel('$q_x$')

    component = {0:'$S_\perp$',1:'$S_\parallel$'}
    ax[2].set_axis_off()

    for i,ax0 in enumerate(ax[:2]):
        top=ax0.get_ylim()[1]
        left=ax0.get_xlim()[0]
        ax[i].text(left,top,component[i],va='top',ha='left',fontsize=14,bbox=dict(facecolor='w'))
        if align=='vertical':   ax0.set_ylabel('$q_y$')
        if align=='horizontal': ax0.set_xlabel('$q_x$')
        ax0.set_xlim(np.min(qpt_cart[:,0]),np.max(qpt_cart[:,0]))
        ax0.set_ylim(np.min(qpt_cart[:,1]),np.max(qpt_cart[:,1]))
        ax0.set_aspect('equal')
        ax0.set_axis_off()
    ori={'vertical':'horizontal','horizontal':'vertical'}[align]
    fig.colorbar(scat1, ax=ax[2], orientation=ori,shrink=0.6)
    fig.tight_layout()
    fig.savefig(figname,dpi=500)
    if show: plt.show()
    return fig,ax


def animate_S_vectors(S_vectors,times,nqx,nqy,bound=2,comp='vertical',save=False,gif_name='S_vec'):
    from matplotlib.animation import FuncAnimation, PillowWriter
    def update(i,im,tl,SS,titles): 
        im.set_data(SS[i].T)
        tl.set_text(titles[i])

    nconf = S_vectors.shape[0]
    S_vectors = S_vectors.reshape(nconf,nqx,nqy,3)
    if comp=='vertical': SS = S_vectors[...,0] + S_vectors[...,1]
    if comp=='parallel': SS = S_vectors[...,2]

    fig,ax=plt.subplots(1,1)
    component = {'vertical':'$S_\perp$','parallel':'$S_\parallel$'}

    #kwargs = dict(cmap='hot',vmin=np.min(SS),vmax=np.max(SS))
    kwargs = dict()
    kwargs.update(origin='lower',extent=[-bound,bound,-bound,bound],aspect='equal')
    im = ax.imshow(SS[0].T,**kwargs)
    ax.set_xlabel('$q_x$')
    ax.set_ylabel('$q_y$')
    tl = ax.set_title('t = {:6.3f} ps'.format(times[0]))
    cbar = fig.colorbar(im,shrink=0.6)
    fig.tight_layout()
    titles = ['t = {:6.3f} ps'.format(tt) for tt in times]
    anim = FuncAnimation(fig, update, frames=range(nconf), interval=5e2, repeat=False,
    fargs=[im, tl, SS, titles])
    if save:
        print ('save animation to {0}.gif'.format(gif_name))
        anim.save('{0}.gif'.format(gif_name), dpi=gif_dpi, writer='imagemagick')
    else: plt.show()



def gen_qpts_from_path(q_path,rcell,nq=200,smooth_connect=True):
    qsymm = np.dot(q_path,rcell)
    q_dists = np.linalg.norm(qsymm[1:] - qsymm[:-1],axis=1)
    nqs = np.array([round(nq*q_dist/np.sum(q_dists)) for q_dist in q_dists],int)
    nqs[np.argmax(q_dists)] += nq - np.sum(nqs)
    npath,ndim = q_path.shape
    q_vec = np.zeros((nq,ndim))
    idx_nodes=np.append(0,np.cumsum(nqs))
    for ip,i in np.ndindex(npath-1,ndim):
        q_vec[idx_nodes[ip]:idx_nodes[ip+1],i] = np.linspace(q_path[ip,i],q_path[ip+1,i],nqs[ip],endpoint=(ip==npath-2))
    qpt_cart = np.dot(q_vec,rcell)
    q_dists = np.append(0,np.cumsum(np.linalg.norm(qpt_cart[1:] - qpt_cart[:-1],axis=1)))
    idx_nodes[-1] -= 1
    q_nodes = q_dists[idx_nodes]
    return qpt_cart,q_dists,q_nodes



# analytic solution of magnon of 2D spin lattice
# within the framework of linear spin wave theroy
# Here Z1, Z2, ... are the coordination number
# J1, J2, ... are the heisenberg exchange of shells sorted by distance
# SIA is the single-ion anistropy which is assumed to be unified
# Here we assume the lattice constants of the real space magnetic unit cell to be 1
# The ground state should be Ferromagnetic along the z direction
def analytic_spin_wave_FM(lat_type,qpt_cart,J1,J2,SIA,DMI=0,S=1):

    def get_structure_factor_from_disp(qpt_cart,disp):
        return np.sum(np.exp(2.j*np.pi*np.dot(qpt_cart,disp.T)),axis=1).real/len(disp)

    def get_chiral_structure_factor_from_disp(qpt_cart,disp):
        nn = len(disp)//2
        f1 = np.sum(np.exp(2.j*np.pi*np.dot(qpt_cart, disp[:nn].T)),axis=1).real/len(disp)
        f2 = np.sum(np.exp(2.j*np.pi*np.dot(qpt_cart, disp[nn:].T)),axis=1).real/len(disp)
        return f1-f2


    r3=np.sqrt(3)
    r3h=r3/2
    nq = len(qpt_cart)
    if lat_type=='honeycomb':
        disp_1 = np.array([[r3h,-0.5],[-r3h,-0.5],[0,1]])/r3
        disp_2 = np.array([[1,0],[0.5,r3h],[-0.5,r3h],[-0.5,r3h],[-1,0],[-0.5,-r3h]])
    elif lat_type=='square':
        disp_1 = np.array([[1,0],[0,1],[-1,0],[0,-1]])
        disp_2 = np.array([[1,1],[-1,1],[-1,-1],[1,-1]])
    elif lat_type=='triangular':
        disp_1 = np.array([[1,0],[0.5,r3h],[-0.5,r3h],[-1,0],[-0.5,-r3h],[0.5,-r3h]])
        disp_2 = np.array([[3/2,r3h],[0,r3],[-3/2,r3h],[-3/2,-r3h],[0,-r3],[3/2,r3h]])
    elif lat_type=='chain':
        disp_1 = np.array([[-1,0],[1,0]])
        disp_2 = np.array([[-2,0],[2,0]])

    if lat_type!='kagome':
        Z1 = len(disp_1)
        Z2 = len(disp_2)
    if lat_type=='honeycomb':   # two bands for diatomic latice
        gamma_k_1 = get_structure_factor_from_disp(qpt_cart,disp_1)
        gamma_k_2 = get_structure_factor_from_disp(qpt_cart,disp_2)
        ham = np.zeros((nq,2,2))
        ham[:,0,1] = - Z1*J1*S*gamma_k_1 - Z2*J2*S*gamma_k_2
        ham[:,1,0] = ham[:,0,1].conj()
        for i in range(2): ham[:,i,i] = Z1*J1*S + Z2*J2*S + 2*SIA*S
        magnon = np.linalg.eigh(ham)[0].T
    elif lat_type=='kagome':
        Z1 = 2
        Z2 = 2
        disp_1_ab = np.array([[1,0],[-1,0]])/2
        disp_1_bc = np.array([[0.5, r3h],[-0.5,-r3h]])/2
        disp_1_ca = np.array([[0.5,-r3h],[-0.5, r3h]])/2
        disp_2_ab = np.array([[0,1],[0,-1]])/r3h
        disp_2_bc = np.array([[-r3h,0.5],[r3h,-0.5]])/r3h
        disp_2_ca = np.array([[-r3h,-0.5],[r3h,0.5]])/r3h

        gamma_k_1_ab = get_structure_factor_from_disp(qpt_cart,disp_1_ab) 
        gamma_k_1_bc = get_structure_factor_from_disp(qpt_cart,disp_1_bc) 
        gamma_k_1_ca = get_structure_factor_from_disp(qpt_cart,disp_1_ca) 
        gamma_k_2_ab = get_structure_factor_from_disp(qpt_cart,disp_2_ab)
        gamma_k_2_bc = get_structure_factor_from_disp(qpt_cart,disp_2_bc)
        gamma_k_2_ca = get_structure_factor_from_disp(qpt_cart,disp_2_ca)

        ham = np.zeros((nq,3,3))
        ham[:,0,1] = - Z1*J1*S*gamma_k_1_ab - Z2*J2*S*gamma_k_2_ab
        ham[:,1,2] = - Z1*J1*S*gamma_k_1_bc - Z2*J2*S*gamma_k_2_bc
        ham[:,2,0] = - Z1*J1*S*gamma_k_1_ca - Z2*J2*S*gamma_k_2_ca
        ham += np.swapaxes(ham.conj(),1,2)
        for i in range(3): ham[:,i,i] = 2*Z1*J1 + 2*Z2*J2 + 2*SIA*S
        magnon = np.linalg.eigh(ham)[0].T
    else: 
        gamma_k_1 = get_structure_factor_from_disp(qpt_cart,disp_1)
        gamma_k_2 = get_structure_factor_from_disp(qpt_cart,disp_2)
        magnon1 = 2*Z1*J1*S*(1-gamma_k_1) + 2*Z2*J2*S*(1-gamma_k_2) + 4*SIA*S
        if DMI!=0:
            chiral_gamma_k_1 = get_chiral_structure_factor_from_disp(qpt_cart,disp_1)
            magnon1 += 2*Z1*DMI*S * chiral_gamma_k_1
        magnon = np.array([magnon1])
    freqs = magnon*meV_to_THz
    return freqs


def get_qpath_2D_latt(lat_type):
    if lat_type=='chain':
        q_path = np.array([[-0.5,0],[0,0],[0.5,0]])
        labels = '\\bar{X} \Gamma X'
    elif lat_type in ['honeycomb','triangular','kagome']:
        q_path = np.array([[0.5,0.],[0,0],[1/3,1/3],[0.5,0]])
        labels = 'M \Gamma K M'
    elif lat_type=='square':
        q_path = np.array([[0.5,0.5],[0,0],[0.5,0.],[0.5,0.5]])
        labels = 'M \Gamma X M'
    return q_path,labels


def test_spin_wave(lat_type,J1=1,J2=0,SIA=0.1,nx=1,ny=1,nq=100,plot_en_axis=True,show=False):
    from asd.core.geometry import build_latt
    latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False)
    nat=sites.shape[-2]
    rcell = np.linalg.inv(latt).T  # in 2pi
    q_path,labels=get_qpath_2D_latt(lat_type)
    qpt_cart,q_dists,q_nodes = gen_qpts_from_path(q_path,rcell,nq)
    analytic_spectra = analytic_spin_wave_FM(lat_type,qpt_cart,J1,J2,SIA)
    max_omega = np.max(analytic_spectra)*1.1

    fmt = '$J_1$={:4.2f} meV, $J_2$={:4.2f} meV, $A_z$={:4.2f} meV'
    params = fmt.format(J1,J2,SIA)
    title = '{} lattice\n{}'.format(lat_type,params)
    fig,ax=plt.subplots(1,1)
    #ax.text(0.1,0.8,params)
    ax.set_title(title)
    ax.set_xticks(q_nodes)
    ax.set_xticklabels(['${}$'.format(item) for item in labels.split()])
    for q in q_nodes: ax.axvline(q,c='grey',alpha=0.5,zorder=-1)
    ax.set_xlim(q_dists[0],q_dists[-1])
    ax.set_ylabel('$\omega\ \mathrm{(THz)}$')
    ax.plot(q_dists,analytic_spectra.T)
    ax.axhline(0,ls='--',c='grey',zorder=-1)
    if plot_en_axis:
        tax = ax.twinx()
        tax.plot(q_dists,analytic_spectra.T/meV_to_THz,ls='--')
        ylim=ax.get_ylim()
        tax.set_ylim(ylim[0]/meV_to_THz,ylim[1]/meV_to_THz)
        tax.set_ylabel('$\\hbar \omega\ \mathrm{(meV)}$')
        tax.axhline(SIA,ls='--',c='grey',alpha=0.5)
    fig.tight_layout()
    output = '{}_FM_spin_wave'.format(lat_type)
    fig.savefig(output,dpi=400)
    if show: plt.show()



def bandmap(dynS,q_dists,q_nodes,labels,max_omega,comp='xy',show=True,
    analytic_spectra=None,output='dyn_struct_factor',plot_en_axis=True):
    from .auxiliary_colormaps import parula
    dirs = {'x':0,'y':1,'z':2}
    if len(comp)==2: SS = np.linalg.norm(dynS[...,[dirs[comp[0]],dirs[comp[1]]]],axis=-1)
    else: SS = dynS[...,dirs[comp]]
    griddata = SS.T.real
    griddata = np.log(abs(griddata))/np.log(10)
    fig,ax=plt.subplots(1,1,figsize=(6,6))
    kwargs=dict(origin='lower',extent=[q_dists[0],q_dists[-1],0,max_omega],aspect='auto',cmap=parula)
    im = ax.imshow(griddata,**kwargs)
    ax.set_xticks(q_nodes)
    ax.set_xticklabels(['${}$'.format(item) for item in labels.split()])
    ax.set_ylabel('$\omega\ \mathrm{(THz)}$')
    cbar = fig.colorbar(im,shrink=0.6,orientation='horizontal')
    cbar.ax.set_title('$\mathrm{Log}\ \\vert S_{'+comp+'}\ (\mathbf{q},\omega) \\vert$')
    colors=['r','g','b','c']
    if analytic_spectra is not None:
        for i,sw in enumerate(analytic_spectra): ax.plot(q_dists,sw,c=colors[i])
    if plot_en_axis:
        tax=ax.twinx()
        ylim=ax.get_ylim()
        tax.set_ylim(ylim[0]/meV_to_THz,ylim[1]/meV_to_THz)
        tax.set_ylabel('$\\hbar \omega\ \mathrm{(meV)}$')
    fig.tight_layout()
    fig.savefig(output,dpi=400)
    if show: plt.show()
    return fig,ax



if __name__=='__main__':
    print ('Running {}'.format(__file__.split('/')[-1]))
    test_spin_wave('chain',J2=0.,SIA=0)
    #test_spin_wave('kagome',SIA=0)
    test_spin_wave('honeycomb',SIA=0)
    test_spin_wave('square',SIA=0,show=True)
