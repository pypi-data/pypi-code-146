#!/usr/bin/env python3

#=================================================
# post-process of Monte Carlo simulation results
# Shunhong Zhang
# szhang2@ustc.edu.cn
# last modified: Oct 01 2022
#==================================================



import os
import numpy as np
from asd.core.topological_charge import calc_topo_chg
from asd.utility.spin_visualize_tools import *
from asd.utility.mag_thermal import *
from asd.utility.asd_arguments import *
import matplotlib.pyplot as plt
import importlib
import re
import glob

def get_args():
    import argparse
    parser = argparse.ArgumentParser(prog='asd_arguments.py', description = 'post-processing of llg')
    add_mc_arguments(parser)
    add_switch_arguments(parser)
    add_quiver_arguments(parser)
    add_spin_plot_arguments(parser)
    args = parser.parse_args()
    return args


def plot_lowest_energy_snapshot(repeat_x=1,repeat_y=1,outdir='snapshots'):
    ovfs=sorted(glob.glob('{}/*ovf'.format(outdir)))
    ens = np.array([os.popen('grep "Etot =" {}'.format(fil)).readline().rstrip('\n').split()[-2] for fil in ovfs],float)
    idx=np.argmin(ens)
    plot_snapshot(ovfs[idx],tag='E = {:8.3f} meV/site'.format(ens[idx]),repeat_x=repeat_x,repeat_y=repeat_y)
    

def plot_snapshot(fil_ovf,spin_plot_kwargs,repeat_x,repeat_y,tag=None):
    spins = parse_ovf_1(fil_ovf)[1]
    sites_repeat = get_repeated_sites(sites,repeat_x,repeat_y)
    sites_cart = np.dot(sites_repeat,latt)
    sp_lat = get_repeated_conf(sp_lat,repeat_x,repeat_y)
    title = '{} '.format(tag)
    spin_plot_kwargs.update(latt=latt,title=title,show=False)
    plot_spin_2d(sites_cart,sp_lat,**spin_plot_kwargs)

    try:
        tri,Q_distri,Q = calc_topo_chg(sp_lat,sites_cart,spatial_resolved=True)
        title += 'Q = {:5.2f}'.format(Q)
        spin_plot_kwargs.update(tri=tri,Q_distri=Q_distri,color_mapping='Q_full')
        plot_spin_2d(sites_cart,sp_lat,**spin_plot_kwargs)
    except:
        pass
    plt.show()


def get_snapshot_confs(outdir='snapshots'):
    ovfs=sorted(glob.glob('{}/*ovf'.format(outdir)))
    if len(ovfs)==1:   all_spins = parse_ovf_1(ovfs[0])[1]
    else:  all_spins = [parse_ovf_1(fil_ovf_1)[1] for fil_ovf in ovfs]
    all_spins = np.array(all_spins)
    return all_spins


def get_mag_en_from_log(outdir='snapshots',log_file='log_0',start_conf_idx=30,jump_conf=1):
    lines = open('{}/{}'.format(outdir,log_file)).readlines()
    idx = np.where([re.search('#',line) for line in lines])[0]
    data = np.array([lines[ii].split()[1:] for ii in idx],float)
    data = data[start_conf_idx:][::jump_conf]
    E  = np.average(data[:,1])
    E2 = np.average(data[:,1]**2)
    mm = np.linalg.norm(data[:,-2:],axis=1)
    m1 = np.average(mm)
    m2 = np.average(mm**2)
    m4 = np.average(mm**4)
    return m1,m2,m4,E,E2


def get_mag_en_from_dat(outdir='snapshots',dat_file='M.dat',start_conf_idx=30,jump_conf=1):
    data = np.loadtxt('{}/{}'.format(outdir,dat_file),skiprows=4)
    data = data[start_conf_idx::jump_conf]
    E  = np.average(data[:,1])
    E2 = np.average(data[:,1]**2)
    mm = np.linalg.norm(data[:,-2:],axis=1)
    m1 = np.average(mm)
    m2 = np.average(mm**2)
    m4 = np.average(mm**4)
    return m1,m2,m4,E,E2


def plot_magnetization(temp_list,start_conf_idx=30):
    mm = []
    for itemp,temp in enumerate(temp_list):
        all_spins = get_snapshot_confs('snapshots_{}'.format(itemp))
        mm.append(np.average(all_spins[start_conf_idx:],axis=(0,1)))
    mm=np.array(mm)
    magnetization = np.linalg.norm(mm,axis=1)
    fig,ax=plt.subplots(1,1)
    ax.plot(temp_list,magnetization)
    ax.set_xlabel('T')
    ax.set_ylabel('M')
    plt.show()


def plot_thermal(temp_list,outdir='.',start_conf_idx=30):
    ntemp = len(temp_list)
    kws = dict(outdir=outdir,start_conf_idx=start_conf_idx)
    try:    data = [get_mag_en_from_log(log_file='log_{}'.format(itemp),**kws) for itemp in range(ntemp)]
    except: data = [get_mag_en_from_dat(dat_file='M.dat',**kws) for itemp in range(ntemp)]
    data = np.array(data)
    m1,m2,m4,E,E2 = data.T 
    M,chi,C_v,u4 = calc_thermodynamic_properties(temp_list,m1,m2,m4,E,E2)
    plot_thermodynamic_properties(temp_list,M,chi,E,C_v,figname='therm_prop')
        

if __name__=='__main__':
    args = get_args()
    quiver_kws = dict([(k.split('_')[1],v) for (k,v) in vars(args).items() if k.startswith('quiver')])
    quiver_kws.update(pivot='mid',units='x')
    print ('keyword arguments for quivers\n')
    for key in quiver_kws.keys(): print ('{:>15s} = {}'.format(key,quiver_kws[key]))
    spin_plot_kwargs = get_spin_plot_kwargs(args)
    spin_plot_kwargs.update(quiver_kws=quiver_kws)
    assert os.path.isfile(args.mc_file),'{} for Monte Carlo simulation not found!'.format(args.mc_file)
    mc_file = args.mc_file.rstrip('.py')
    mc = importlib.import_module(mc_file)
    nx=mc.nx
    ny=mc.ny
    nat=mc.nat
    sites=mc.sites

    if args.task == 'thermal': 
        try: temp_list = mc.temp_list
        except: temp_list = np.array([mc.MC._temperature])
        plot_thermal(temp_list,args.outdir,args.start_conf_idx)
    elif args.task=='snapshot':
        #plot_lowest_energy_snapshot(repeat_x=2,repeat_y=2,outdir='snapshots_0')
        #get_snapshot_confs('snapshots_0')
        #plot_magnetization(temp_list)
        #all_spins = get_snapshot_confs('snapshots_0')
        plot_snapshot('{}/MCS_spin_confs.ovf'.format(args.outdir),spin_plot_kwargs,args.repeat_x,args.repeat_y)
