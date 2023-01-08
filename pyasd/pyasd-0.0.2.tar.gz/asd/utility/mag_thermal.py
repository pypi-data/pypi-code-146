#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import asd.mpi.mpi_tools as mt
import matplotlib.pyplot as plt
import glob
from asd.utility.ovf_tools import *
from asd.core.constants import kB


def mag_statistics(spins,start_img=0):
    mm = np.average(spins[start_img:],axis=1)
    m_tot = np.linalg.norm(mm,axis=-1)
    mm1 = np.average(m_tot)
    mm2 = np.average(m_tot**2)
    mm4 = np.average(m_tot**4)
    return mm,mm1,mm2,mm4,m_tot



def dump_mag_temp(temp_list,mm1,mm2,mm4,E=None,E2=None,fil='M_temp.dat'):
    with open('M_temp.dat','w') as fw:
        if E is not None and E2 is not None: 
            fmt = '{:10.5f} '+'{:12.8f} '*5+'\n'
            for (TT,m1,m2,m4,E_,E2_) in zip(temp_list,mm1,mm2,mm4,E_,E2_):fw.write(fmt.format(TT,m1,m2,m4,E_,E2_))
        else: 
            fmt = '{:10.5f} '+'{:12.8f} '*3+'\n'
            for (TT,m1,m2,m4) in zip(temp_list,mm1,mm2,mm4): fw.write(fmt.format(TT,m1,m2,m4))


def mpi_get_magnetization(temp_list,start_img=0,fil_tag='K/output/*Spins-*archive*',verbosity=1):
    import asd.mpi.mpi_tools as mt
    ntemp=len(temp_list)
    comm,size,rank,node=mt.get_mpi_handles()
    if not rank and verbosity:
        print ('\nmpi_get_magnetization')
        print ('parallel on {} cores'.format(size))
        print ('{} temperature points\n'.format(ntemp))
    start,last=mt.assign_task(ntemp,size,rank)
    mm=np.zeros((last-start,3),float)
    mm1=np.zeros(last-start,float)
    mm2=np.zeros(last-start,float)
    mm4=np.zeros(last-start,float)
    for iT,TT in enumerate(temp_list[start:last]):
        fil_ovf=glob.glob('{0}{1}'.format(TT,fil_tag))[0]
        if not rank and verbosity: print (fil_ovf,end=' ')
        params,spins = parse_ovf_1(fil_ovf,parse_params=False)
        if not rank and verbosity: print ('{0} images, statistics starting from {1}'.format(spins.shape[0],start_img))
        sys.stdout.flush()
        mm[iT],mm1[iT],mm2[iT],mm4[iT],m_tot = mag_statistics(spins,start_img)

    mm=comm.gather(mm,root=0)
    mm1=comm.gather(mm1,root=0)
    mm2=comm.gather(mm2,root=0)
    mm4=comm.gather(mm4,root=0)
    if not rank:
        mm=np.concatenate(mm,axis=0)
        mm1=np.concatenate(mm1,axis=0)
        mm2=np.concatenate(mm2,axis=0)
        mm4=np.concatenate(mm4,axis=0)
        dump_mag_tmep(temp_ilst,mm1,mm2,mm4)
    return mm,mm1,mm2,mm4


def get_energy_from_txt(start_conf=0,outdir='.',prefix='temp'):
    fil = glob.glob('{}/{}*Energy-archive.txt'.format(outdir,prefix))
    assert len(fil)>0, 'Energy file out found!'
    lines = open(fil[0]).readlines()[3:][start_conf:]
    ens = np.array([line.split()[2] for line in lines],float)
    return ens


def get_magnetization(temp_list,outdir='mag',fil_tag='K/M.dat',start_img=10):
    ntemp=len(temp_list)
    mm1=np.zeros(ntemp)
    mm2=np.zeros(ntemp)
    mm4=np.zeros(ntemp)
    E=np.zeros(ntemp)
    E2=np.zeros(ntemp)

    bad_idx=[]

    for iT,temp in enumerate(temp_list):
        try:
            fil = '{}/{}{}'.format(outdir,temp,fil_tag)
            data=np.loadtxt(fil)
            m_tot = np.linalg.norm(data[start_img:,2:],axis=1)
            mm1[iT] = np.average(m_tot)
            mm2[iT] = np.average(m_tot**2)
            mm4[iT] = np.average(m_tot**4)
            E[iT] = np.average(data[start_img:,1])
            E2[iT]= np.average(data[start_img:,1]**2)
        except:
            bad_idx.append(iT)

    if len(bad_idx)>0:
        temp_list=np.delete(temp_list,bad_idx)
        mm1=np.delete(mm1,bad_idx)
        mm2=np.delete(mm2,bad_idx)
        mm4=np.delete(mm4,bad_idx)

    dump_mag_temp(temp_list,mm1,mm2,mm4,E,E2)
    return mm1,mm2,mm4,E,E2


def calc_thermodynamic_properties(temp_list,m1,m2,m4,E,E2):
    M = m1
    chi=(m2-m1**2) / (kB*temp_list)
    u4=1-m4/3/m2**2
    C_v= (E2-E**2) / (kB*temp_list)**2
    fmt = '{:8.3f} {:12.5f} '+'{:20.8f} '*3+'\n'
    with open('thermal_mag.dat','w') as fw:
        for i,temp in enumerate(temp_list):
            fw.write(fmt.format(temp,M[i],chi[i],C_v[i],u4[i]))
    return M,chi,C_v,u4


def plot_thermodynamic_properties(temp_list,M,chi,E,C_v,figname='therm_prop',write_formula=True):
    fig,ax=plt.subplots(2,2,sharex=True,figsize=(9,6))
    #fig.subplots_adjust(wspace=0.2)
    ax[0,0].plot(temp_list,M,'ro-',label='M')
    ax[1,0].plot(temp_list,chi/np.max(chi),'g-',label='$\chi$')
    ax[0,1].plot(temp_list,E,'m-',label='$E$')
    ax[1,1].plot(temp_list,C_v/np.max(C_v),'b-',label='$C_v$')
    ax[0,0].axhline(0,c='gray',ls='--',alpha=0.5,zorder=-1)
    ax[0,0].set_ylabel('$M\ /\ M_{max}$')
    ax[1,0].set_ylabel('$\chi$')
    ax[0,1].set_ylabel('$E\ (meV/site)$')
    ax[1,1].set_ylabel('$C_v$')
    ax[1,0].set_xlabel('T(K)')
    ax[1,1].set_xlabel('T(K)')
    Tc_chi = temp_list[np.argmax(chi)]
    Tc_C_v = temp_list[np.argmax(C_v)]
    ax[1,0].axvline(Tc_chi,ls='--',alpha=0.5,zorder=-1)
    ax[1,1].axvline(Tc_C_v,ls='--',alpha=0.5,zorder=-1)
    prefix = 'Transition temperature estimated from' 
    print ('{} susceptibility: {:8.4f} K'.format(prefix,Tc_chi))
    print ('{} specific heat:  {:8.4f} K'.format(prefix,Tc_C_v))
    if write_formula:
        left = ax[1,0].get_xlim()[1]*0.7
        ax[1,0].text(left,0.9,'$\chi=\\frac{<M^2>-<M>^2}{k_B T}$',fontsize=14,ha='center')
        ax[1,1].text(left,0.9,'$C_v=\\frac{<E^2>-<E>^2}{(k_B T)^2}$',fontsize=14,ha='center')
    fig.tight_layout()
    fig.savefig(figname,dpi=500)
    plt.show()


def logarithmic_magnetization(temperature,Tc,beta):
    assert Tc>0, 'Critical temperature should be positive!'
    f = 1-(temperature/Tc)
    if type(temperature)==float:
        return np.power(f,beta) if f>0 else 0
    else:
        idx1 = np.where(f>0)
        M = np.zeros_like(temperature)
        M[idx1] = np.power(f[idx1],beta)
        return M


def display_log_magnetization_with_varying_beta(temperatures=np.linspace(0,20,100,),Tc=10,betas=[0.125,np.pi**2*3/128],show=False):
    fig,ax=plt.subplots(1,1,figsize=(6,4))
    for beta in betas:
        yy = logarithmic_magnetization(temperatures,Tc,beta)
        ax.plot(temperatures,yy,label='$\\beta\ =\ {:.3f}$'.format(beta))
    for beta,label in zip([0.125,np.pi**2*3/128],['Ising','XY']):
        yy = logarithmic_magnetization(temperatures,Tc,beta)
        ax.plot(temperatures,yy,lw=3,label='$\\beta\ =\ {0:.3f}$'.format(beta)+' 2D {}'.format(label))
    ax.legend()
    ax.set_xlabel('T (K)')
    ax.set_ylabel('M')
    fig.tight_layout()
    fig.savefig('Tc_beta_power',dpi=400)
    if show: plt.show()


if __name__=='__main__':
    print ('script to calculate spin related thermodynamic properties')
    betas = [0.15,0.3,0.6,1.2,1.8]
    display_log_magnetization_with_varying_beta(betas=betas,show=True)
