#!/usr/bin/env python

#==========================================
# post-process of llg simulation results
# Shunhong Zhang
# szhang2@ustc.edu.cn
# last modified: Nov 12, 2021
#===========================================


import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import glob
import re
import pickle
import importlib
from asd.core.geometry import build_latt
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.utility.asd_arguments import *
from asd.core.llg_simple import *


def get_args():
    import argparse
    parser = argparse.ArgumentParser(prog='asd_arguments.py', description = 'post-processing of llg')
    add_common_arguments(parser)
    add_quiver_arguments(parser)
    add_llg_arguments(parser)
    add_spin_plot_arguments(parser)
    add_switch_arguments(parser)
    args = parser.parse_args()
    return args


def get_dE_from_out(outdir='./'):
    fil=glob.glob('{}/*.out'.format(outdir))
    if len(fil)>0: 
        fil=fil[0]
        lines = open(fil).readlines()
          
        lines = [line for line in lines if line.startswith('#')]
        time=np.array([line.split()[3] for  line in lines],float)
        ener=np.array([line.split()[4] for  line in lines],float)
        print ('Read diff_E   from {}'.format(fil))
        diff_E=np.array([line.split()[5] for  line in lines],float)
        print ('Read max|H_i| from {}'.format(fil))
        force=np.array([line.split()[-1] for  line in lines],float)
    else:
        time = None
        ener = None
        diff_E = None
        force = None
    return time,ener,diff_E,force



def plot_E_T(show=False):
    time,ener,diff_E,forc = get_dE_from_out()
    if time is None : 
        print ('skip plotting diff_E')
        return None,None,None

    fig,ax=plt.subplots(1,1)
    ax.plot(time,ener,'b-')
    ax.set_xlabel('Time (ps)')
    ax.set_ylabel('E (meV/site)',color='b')
    ax.tick_params(axis='y', labelcolor='b')
    if np.max(ener)-np.min(ener) < 0.1: ax.set_ylim(np.min(ener)-0.1,np.max(ener)+0.1)
    if diff_E is not None:
        axx=ax.twinx()
        axx.plot(time,np.log(abs(diff_E))/np.log(10),'r-')
        axx.set_ylabel('log|dE|',color='r')
        axx.tick_params(axis='y', labelcolor='r')
        axx.set_xlim(0,np.max(time))
    fig.tight_layout()
    fig.savefig('E_T',dpi=500)

    if forc is not None:
        fig1,ax1=plt.subplots(1,1)
        ax1.plot(time,np.log(abs(forc))/np.log(10),'g-')
        ax1.set_xlabel('Time (ps)')
        ax1.set_ylabel('log|forcee|')
        ax1.set_xlim(0,np.max(time))
        fig1.tight_layout()
        fig1.savefig('forc',dpi=500)
    return fig,ax,axx


def ax_plot_magnetization(ax,time,data):
    for i in range(3,6): ax.plot(time,data[:,i],label={3:'$M_x$',4:'$M_y$',5:'$M_z$'}[i])
    ax.plot(time,np.linalg.norm(data[:,3:5],axis=1),label='$M_\parallel$')
    ax.plot(time,np.linalg.norm(data[:,3:6],axis=1),label='M')
    ax.legend(ncol=2)
    ax.set_xlim(np.min(time),np.max(time))
    ax.set_ylim(-1.1,1.1)
    ax.set_yticks([-1,0,1])
    ax.set_xlabel('Time (ps)')
    ax.set_ylabel('M')
 


def plot_summary(fil='M.dat',plot_summary=True):
    data=np.loadtxt(fil,skiprows=1)
    time = data[:,0]
    ener = data[:,1]
    diff_E = data[:,2]
    if not plot_summary: return data,False

    fig,ax=plt.subplots(2,1,sharex=True,figsize=(6,6))

    ax[0].plot(time,ener,'b-')
    ax[0].set_ylabel('E (meV/site)',color='b')
    ax[0].tick_params(axis='y', labelcolor='b')
    if np.max(ener)-np.min(ener) < 0.1: ax[0].set_ylim(np.min(ener)-0.1,np.max(ener)+0.1)

    if diff_E is not None:
        axx=ax[0].twinx()
        axx.plot(time,np.log(abs(diff_E))/np.log(10),'r-')
        axx.set_ylabel('log|dE|',color='r')
        axx.tick_params(axis='y', labelcolor='r')

    ax_plot_magnetization(ax[1],time,data)
    fig.tight_layout()
    fig.savefig('E_M_T',dpi=500)

    if data.shape[1]==7:
        Qs = data[:,-1]
        fig,ax=plt.subplots(1,1)
        ax.plot(time,Qs)
        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('Q')
        ax.set_xlim(np.min(time),np.max(time))
        ax.set_ylim(min(-1.5,np.min(Qs)*1.05),max(1.5,np.max(Qs)*1.05))
        ax.axhline(0,c='gray',ls='--',lw=0.5,alpha=0.5,zorder=-2)
        fig.tight_layout()
        fig.savefig('topo_chg_evolution',dpi=600)
        calc_Q = False
    else:
        calc_Q = True

    return data,calc_Q



# this function is still under test
def calc_site_resolved_spin_energy(LLG,sp_lat):
    nx,ny,nat = sp_lat.shape[:3]
    en = np.zeros((nx,ny,nat),float)
    for ix,iy,iat in np.ndindex(nx,ny,nat):
        n_i = sp_lat[ix,iy,iat]
        B_eff = LLG.calc_local_B_eff_from_Jmat(sp_lat,ix,iy,iat)
        en[ix,iy,iat] = np.dot(n_i,B_eff)*LLG._S_values[iat]
    return en


def display_snapshot(latt,sites,conf,head,spin_plot_kwargs,args,tag='snapshot',title=None):
    shape = sites.shape
    if len(shape)==5: 
        nx,ny,nz,nat = shape[:4]
        conf = conf.reshape(nz,ny,nx,nat,3)
        print('3D latt, (nx,ny,nz,nat) = ( {} , {} , {} , {} )'.format(nx,ny,nz,nat))
        exit('Sorry, we currently do not support visualization of 3D lattice') 
    else:
        nx,ny,nat=sites.shape[:3]
        conf = conf.reshape(ny,nx,nat,3)
        conf = np.swapaxes(conf,0,1)
    if args.plot_superlatt: superlatt=np.dot([[nx*args.repeat_x,0],[0,ny*args.repeat_y]],latt)
    else: superlatt = None
    sites_repeat = get_repeated_sites(sites,args.repeat_x,args.repeat_y)
    sites_cart_repeat = np.dot(sites_repeat,latt)
    conf_repeat = get_repeated_conf(conf,args.repeat_x,args.repeat_y)

    figname='{0}_{1}.png'.format(head,tag)
    if title is None: title='{} '.format(tag)
    spin_plot_kwargs.update(
    color_mapping=args.color_mapping,
    title=title,
    figname=figname,
    superlatt=superlatt,
    colorbar_axes_position=args.colorbar_axes_position)
    plot_spin_2d(sites_cart_repeat,conf_repeat,**spin_plot_kwargs)

    if args.topo_chg and np.prod(sites_cart_repeat.shape[:-1])>=4:
        tri,Q_distri,Q = calc_topo_chg(conf_repeat,sites_cart_repeat,spatial_resolved=True,solid_angle_method=args.solid_angle_method)

        spin_plot_kwargs.update(
        color_mapping=args.Q_color_mapping,
        tri=tri,  
        Q_distri=Q_distri,
        title='{}: Q = {:6.2f}'.format(title,Q),
        mapping_all_sites=True,latt=latt,
        figname=figname.replace('.png','_topo_chg.png'))

        plot_spin_2d(sites_cart_repeat,conf_repeat,**spin_plot_kwargs)


def display_conf_from_ovf(fil_ovf,latt,sites,args,spin_plot_kwargs,tag='initial',title=None,head='spin'):
    if args.prefix!='': fil_ovf = '{}_{}'.format(args.prefix,fil_ovf)
    fils = glob.glob('{}/{}'.format(args.outdir,fil_ovf))
    if len(fils)==0:
        print ('\n{} not found, skip plotting'.format(fil_ovf))
        return False
    else:
        params,conf=parse_ovf(fils[0],parse_params=False)
        display_snapshot(latt,sites,conf,head,spin_plot_kwargs,args,tag=tag,title=title)
        return True



def main(head='spin'):
    args=get_args()
    quiver_kws = dict([(k.split('_')[1],v) for (k,v) in vars(args).items() if k.startswith('quiver')])
    quiver_kws.update(pivot='mid',units='x')
    print ('keyword arguments for quivers\n')
    for key in quiver_kws.keys(): print ('{:>15s} = {}'.format(key,quiver_kws[key]))
    spin_plot_kwargs = get_spin_plot_kwargs(args)
    spin_plot_kwargs.update(quiver_kws=quiver_kws)
    spin_anim_kwargs = get_spin_anim_kwargs(args)
    spin_anim_kwargs.update(quiver_kws=quiver_kws)

    fil_archive='M.dat'
    if args.prefix!='': fil_archive = '{}_M.dat'.format(args.prefix)
    fil_archive = glob.glob('{}/{}'.format(args.outdir,fil_archive))
    if args.plot_out: fig,ax,axx = plot_E_T(outdir=args.outdir)
    if fil_archive:  data,calc_Q = plot_summary(fil_archive[0],plot_summary=args.plot_summary)
    else: calc_Q=True
    plt.show()

    llg = importlib.import_module(args.llg_file.rstrip('.py'))
    lat_type = args.lat_type
    if args.nx==0:  nx=llg.nx
    else: nx = args.nx
    if args.ny==0:  ny=llg.ny
    else: ny = args.ny
    if args.nz==0:  nz = 1
    else: nz = args.nz
    print ('nx={}\nny={}\nnz={}'.format(nx,ny,nz))
    sites=llg.sites
    latt=llg.latt
    nat = sites.shape[-2]

    p1 = display_conf_from_ovf('initial_spin_confs.ovf',latt,sites,args,spin_plot_kwargs,tag='initial',title='initial')
    p2 = display_conf_from_ovf('final_spin_confs.ovf',latt,sites,args,spin_plot_kwargs,tag='final',title='final')
    if p2:
        plt.show()
        display_latest=False
    else:
        print ('\nfinal_spin_confs.ovf not found')
        print ('skip plotting final spin configuration')
        print ('please check whether your simulation has terminated normally\n')
        print ('We will instead display the last snapshot configuration later')
        print ('which is read from spin_confs.ovf')
        display_latest=True

    if display_latest==args.make_ani==False: exit()

    fil_ovf = 'spin_confs.ovf'
    if args.prefix!='': fil_ovf = '{}_{}'.format(args.prefix,fil_ovf)
    fil_conf=glob.glob('{}/{}'.format(args.outdir,fil_ovf))
    if fil_conf: 
        fil_conf=fil_conf[0]
        lines=open(fil_conf).readlines()
        idx=np.where([re.search('time =',line) for line in lines])[0]
        log_time=np.array([lines[ii].split('=')[1].rstrip('ps\n') for ii in idx],float) 
        idx=np.where([re.search('ener =',line) for line in lines])[0]
        log_ener=np.array([lines[ii].split('=')[1].rstrip('meV\n') for ii in idx],float)

        if args.pick_confs: 
            assert os.path.isfile('spin_confs.pickle'),'Set pick_confs = True but spin_confs.pickle not found!'
            print ('Load spin configurations from spin_confs.pickle')
            confs = pickle.load(open('spin_confs.pickle','rb'))
        else: 
            params,confs=parse_ovf(fil_conf,parse_params=True)
            if args.dump_confs: pickle.dump(confs,open('spin_confs.pickle','wb'))

        if args.write_latest:
            fil_latest = 'latest_spin_confs.ovf'
            print ('Latest configuration written to {}'.format(fil_latest))
            spins_latest = confs[-1]
            params['nsegment'] = 1
            write_ovf(params,spins_latest,filename=fil_latest)

        if display_latest:
            title = 'Snapshot at t = {:8.2f} ps'.format(log_time[-1])
            display_snapshot(latt,sites,confs[-1],head,spin_plot_kwargs,args,tag='latest',title=title)
            plt.show()

        if args.snapshot_idx is not None:
            idx=args.snapshot_idx
            print ('\nDisplay snapshot at t = {:8.3f} ps\n'.format(log_time[idx]))
            kwargs = dict(
            title = 'Snapshot at t = {:8.2f} ps'.format(log_time[idx]),
            tag='snapshot_{}'.format(idx), )
            display_snapshot(latt,sites,confs[idx],head,spin_plot_kwargs,args,**kwargs)
            log_confs = np.swapaxes(confs[idx:idx+1],1,2).reshape(1,ny,nx,nat,3)
            log_llg_data(log_time[idx:idx+1],log_ener[idx:idx+1],log_confs,
            'spin_conf_snapshot_{}.ovf'.format(idx),None,log_mode='w')
            plt.show()

        if args.topo_chg:
            if calc_Q==False and os.path.isfile('M.dat'):
                print ('Read topological charges from M.dat')
                data = np.loadtxt('M.dat',skiprows=1)
                llg_time = data[:,0]
                llg_topo_chg = data[:,-1]
                if len(llg_time) == len(llg_topo_chg):
                    idx=np.array([it for it in range(len(llg_time)) if llg_time[it] in log_time])
                    tcs=llg_topo_chg[idx]
            else:
                sites_cart = np.dot(sites,latt)
                sites_cart = np.swapaxes(sites_cart,0,1)
                if np.prod(sites_cart.shape[:-1])<4:
                    print ('No. of sites <4, topological charge won\'t be calculated')
                    args.topo_chg=False
                    tcs = None
                else:
                    print ('\nCalculate the evolution of topological charge during simulation\n')
                    tcs = [calc_topo_chg(conf,sites_cart,solid_angle_method=args.solid_angle_method) for conf in confs]
        else: tcs = None

        if args.make_ani:
            if tcs is None:  titles=['{:8.2f} ps'.format(tt) for tt in log_time]
            else:            titles=['{:8.2f} ps, Q = {:6.2f}'.format(tt,tc) for tt,tc in zip(log_time,tcs)]
            nn=min(len(titles),len(confs))
            sites_repeat = get_repeated_sites(sites,args.repeat_x,args.repeat_y)
            sites_cart_repeat = np.dot(sites_repeat,latt)
            sites_cart_repeat=np.swapaxes(sites_cart_repeat,0,1)

            nx,ny,nat = sites.shape[:-1]
            confs = confs.reshape(confs.shape[0],ny,nx,nat,3)
            confs_repeat=np.tile(confs,(1,args.repeat_x,args.repeat_y,1,1))[:nn]
            if confs_repeat.shape[0]<10: args.jump_images=1

            if args.plot_superlatt: superlatt=np.dot([[nx,0],[0,ny]],latt)
            else: superlatt = None
            spin_anim_kwargs.update(superlatt=superlatt,colorbar_axes_position=args.colorbar_axes_position)
            make_ani(sites_cart_repeat,confs_repeat,titles,**spin_anim_kwargs)
    else:
        print ('\nSorry, cannot find spin_confs.ovf')
        print ('skip plotting')

if __name__=='__main__':
    main()
