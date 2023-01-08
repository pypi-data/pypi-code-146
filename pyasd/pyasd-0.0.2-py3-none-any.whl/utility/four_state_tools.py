#!/usr/bin/env python

#==============================================
# some tools for four-state calculations
# with DFT codes
# Shunhong Zhang
# Last mofified: Oct 01, 2022
#==============================================


import os
import numpy as np

dirs=['x','y','z']
component = np.meshgrid(dirs,dirs)
component = np.array(component)
component = np.transpose(component,(2,1,0)).reshape(-1,2)

block_line_Jmat =  np.arange(0,36,4)
xticks_Jmat =      xx = np.arange(36)+0.5
xticklabels_Jmat = ['{0}{1}'.format(*tuple(item)) for item in component]
xticklabels_SIA  = ['Cr','Mn']


def get_en_from_conf(ham,magmom,nat=1):
    nx=int(np.sqrt(len(magmom)/3/nat))
    ny=nx
    mm = magmom.reshape(nat,ny,nx,3)
    sp_lat = np.transpose(mm,(2,1,0,3))
    norms = np.linalg.norm(sp_lat,axis=-1)
    for i in range(3): sp_lat[...,i] /= norms
    en = ham.calc_total_E_from_Jmat(sp_lat)/(len(magmom)/3)
    return en


def calc_bq_en_from_magmom(exch_bq,magmom):
    nat=2
    nx=int(np.sqrt(len(magmom)/3/nat))
    ny=nx
    mm = magmom.reshape(nat,ny,nx,3)
    sp_lat = np.transpose(mm,(2,1,0,3))
    norms = np.linalg.norm(sp_lat,axis=-1)
    for i in range(3): sp_lat[...,i] /= norms
    en_bq = exch_bq.calc_shell_exch_energy(sp_lat)/(nx*ny*nat)
    return en_bq


def compare_energy(ax,en_model,en_dft,set_name):
    max0 = np.max([en_model,en_dft])
    min0 = np.min([en_model,en_dft])
    margin = (max0-min0)*0.05
    ax.scatter(en_model,en_dft)
    ax.plot([min0-margin,max0+margin],[min0-margin,max0+margin],'g--',zorder=-1)
    ax.set_xlabel('$E_{model}$ / meV')
    ax.set_ylabel('$E_{dft}$ / meV')
    ax.set_aspect('equal')
    ax.set_title(set_name)
    ax.set_xlim(min0-margin,max0+margin)
    ax.set_ylim(min0-margin,max0+margin)
    ax.axhline(0,c='gray',ls='--',alpha=0.5,zorder=-1)
    ax.axvline(0,c='gray',ls='--',alpha=0.5,zorder=-1)


def diff_energy(ax,en_model,en_dft,set_name,conf_names=None,block_line=None,angles=np.arange(0,100,10)):
    nstate = len(en_model)
    xx = np.arange(nstate)+0.5
    if set_name=='MAE' or 'rot' in set_name: 
        ax.set_ylabel('$E\ (\\theta)\ (meV/site)$')
        ax.set_xlabel('$\\theta$')
        xx = angles
    else: 
        ax.set_ylabel('$E$ (meV/site)')
        if nstate == 2*4: tt = ['Cr','Mn']
        elif nstate == 9*4: tt = ['{0}{1}'.format(*tuple(item)) for item in component]
        else: tt=None
        ax.set_xticks(xx[2::4]-0.5)
        if tt: ax.set_xticklabels(tt)
        for tick in ax.get_xticklines(): tick.set_visible(False)
    if block_line is not None:
        for i in block_line: ax.axvline(i,zorder=-1,c='gray',ls='--',alpha=0.6)
    if conf_names is not None: ax.set_xtick_params(ticks=xx,labels=conf_names,rotation='vertical')
    ax.plot(xx,en_model,'o-',label='model')
    ax.plot(xx,en_dft,'*-',label='DFT')
    ax.axhline(0,ls='--',zorder=-1,c='gray',alpha=0.6)
    ax.legend()


def test_one_set(ham,magmom_set,en_dft,set_name,conf_names=None,
    block_line=None,angles=np.arange(0,100,10),nat=2):

    assert len(magmom_set) == len(en_dft), 'test_one_set {0}: no. of magmom {1} != no. of en_dft {2}'.format(set_name,len(magmom_set),len(en_dft))
    en_model = np.array([get_en_from_conf(ham,np.array(magmom),nat=nat) for magmom in magmom_set])
    en_model -= en_model[0]
    nats = np.array([len(magmom)/3 for magmom in magmom_set])
    en0_dft = (en_dft - en_dft[0])/nats

    print ('{0}'.format(set_name))
    if not os.path.isdir('dats'): os.mkdir('dats')
    with open('{0}/{1}.dat'.format('dats',set_name),'w') as fw:
        if conf_names is not None: fw.write('{:>20s} '.format('conf_name'))
        fw.write(('{:>20s} '*4+'\n').format('DFT (meV/cell)','DFT (meV/site)','model (meV/site)','DFT-model (meV/site)'))
        for ii, magmom in enumerate(magmom_set):
            if conf_names is not None: fw.write('{:>20s} '.format(conf_names[ii]))
            fw.write(('{:20.6f} '*4+'\n').format(en_dft[ii],en0_dft[ii],en_model[ii],en0_dft[ii]-en_model[ii]))

    if not os.path.isdir('figures'): os.mkdir('figures')
    import matplotlib.pyplot as plt
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4))
    compare_energy(ax1,en_model,en0_dft,set_name)
    diff_energy(ax2,en_model,en0_dft,set_name,conf_names=conf_names,block_line=block_line,angles=angles)
    fig.tight_layout()
    fig.savefig('figures/{}'.format(set_name),dpi=500)


def get_magmom_lines(filmom,outdir='magmom'):
    lines = open('{}/{}'.format(outdir,filmom)).readlines()
    conf_names = [line.split('/')[0] for line in lines if line!='\n']
    lines = [line.split('=')[1].split()[:-1] for line in lines if line!='\n']
    return lines, conf_names


def get_dft_en(fil,outdir='total_energy'):
    lines = open('{0}/{1}'.format(outdir,fil)).readlines() 
    lines=[line.split()[3] for line in lines if line!='\n']
    en_dft = np.array(lines,float)*1e3
    dirs_dft = [line.split('/')[0] for line in lines if line!='\n']
    return en_dft,dirs_dft

def gen_magmom_MAE(angles):
    moms = np.array([np.cos(np.deg2rad(angles)),np.zeros_like(angles),np.sin(np.deg2rad(angles))]).T
    magmom_MAE = np.array([[m,m] for m in moms]).reshape(-1,6)
    return magmom_MAE

angles = np.arange(0,91,5)


if __name__=='__main__':
    print ('Runing {}'.format(__file__))
    print ('some function to help analyze four-state method calculation results')
