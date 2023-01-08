#!/usr/bin/env python

import numpy as np
from asd.utility.spirit_tool import *
from asd.utility.asd_arguments import *
import os
import glob
import matplotlib.pyplot as plt

import_spirit_err='''
\nNotes from {0}
fail to import modules from Spirit
{0} cannot be used
other scirpts are not affected
Please install Spirit properly
if you want ot use this script\n'''.format(__file__.split('/')[-1])

try:    from spirit import state,system,geometry,parameters
except: exit(import_spirit_err)

outdir='output'


def collect_confs_from_ovfs(outdir,prefix):
    confs=[]
    fils = glob.glob('{}/{}*Spins_*.ovf'.format(outdir,prefix))
    if len(fils)==0: exit('Cannot find ovf files in the directory\n{}'.format(outdir))
    indices = sorted([int(fil.split('_')[-1].rstrip('.ovf')) for fil in fils])
    nn = len(fils[-1].rstrip('.ovf').split('_')[-1])+1
    for idx in indices:
        found=False
        for n in range(nn):
            fil_key = '{}/*Spins_{}.ovf'.format(outdir,str(idx).zfill(n))
            fils= glob.glob(fil_key)
            if len(fils)>0: 
                fil_ovf = fils[0]
                found=True
                break
        if found: confs.append( parse_ovf_1(fil_ovf)[1] )
        else: exit('\nCannot find ovf file with prefix {} under directory\n{}'.format(prefix,outdir))
    return np.array(confs)
 

def get_GNEB(outdir):
    fil_en = glob.glob('{}/*Chain_Energies-interpolated-final.txt'.format(outdir))[0]
    lines = open(fil_en).readlines()[3:]
    data = [line.split() for line in lines]
    Rx = np.array([d[4] for d in data],float)
    Etot = np.array([d[6] for d in data],float)
    Etot -= Etot[0]
    return Rx,Etot


def plot_GNEB(outdir,show=False):
    Rx,Etot = get_GNEB(outdir)
    fig,ax=plt.subplots(1,1)
    ax.plot(Rx,Etot)
    ax.scatter(Rx[::10],Etot[::10],c='r')
    ax.scatter(Rx[-1],Etot[-1],c='r')
    emin = np.min(Etot)
    emax = np.max(Etot)
    erange = emax - emin
    ax.set_ylim(emin-erange*0.1,emax+erange*0.1)
    if erange<1e-4: ax.set_ylim(-0.1,0.1)
    ax.set_ylabel('E (meV)')
    ax.set_xlabel('Reaction coord')
    fig.tight_layout()
    if show: plt.show()
    return fig,ax


def get_params_from_cfg(fil_cfg,nx=0,ny=0,nz=0,lat_type=1,dt=0):
    lattice_constant = 1
    try:
        line = os.popen('grep lattice_constant {}'.format(fil_cfg)).readline()
        lattice_constant = float(line.rstrip('\n').split()[-1])
    except:
        pass
    with state.State(fil_cfg,quiet=True) as p_state:
        if fil_cfg=='': geometry.set_bravais_lattice_type(p_state, lat_type)
        if nx*ny*nz!=0: geometry.set_n_cells(p_state,[nx,ny,nz])
        pos=geometry.get_positions(p_state)
        nx,ny,nz=geometry.get_n_cells(p_state)
        nat=geometry.get_n_cell_atoms(p_state)
        latt=geometry.get_bravais_vectors(p_state)
        if dt==0: dt = parameters.llg.get_timestep(p_state)
    latt = lattice_constant*np.array(latt)
    return latt,pos,nx,ny,nz,nat,dt


def analyze_GNEB_results(scatter_size=10):
    Rx, Etot = plot_GNEB(outdir)

    fil_ovf=glob.glob('{}/*Spins-initial.ovf'.format(outdir))[0]
    print (fil_ovf)
    params,spins_init = parse_ovf_1(fil_ovf,parse_params=True)
    fil_ovf=glob.glob('{}/*Spins-final.ovf'.format(outdir))[0]
    print (fil_ovf)
    params,spins_final = parse_ovf_1(fil_ovf)

    nx = params['xnodes']
    ny = params['ynodes']
    nz = params['znodes']

    latt,pos,nx,ny,nz,nat,dt = get_params_from_cfg(fil_cfg,nx,ny,nz)

    plot_spin_2d(pos,spins_init, scatter_size=scatter_size,title='initial')
    plot_spin_2d(pos,spins_final,scatter_size=scatter_size,title='final'  )
    plt.show()

    fil = sorted(glob.glob('{}/*Chain*final.ovf'.format(outdir)))[0]
    print ('confs from file {}'.format(fil))
    Iter = np.array([line.split()[-1] for line in os.popen('grep Iteration {}'.format(fil)).readlines()],int)
    titles = ['Iter = {:10d}'.format(tt) for tt in Iter]
    params,confs = parse_ovf_ovf(fil,parse_params=False)
    make_ani(pos,confs,scatter_size=scatter_size,titles=titles,interval=5e3)


def get_energy_from_txt(start_conf=0,outdir='.',prefix='temp'):
    fil = glob.glob('{}/{}*Energy-archive.txt'.format(outdir,prefix))
    assert len(fil)>0, 'Energy file out found!'
    lines = open(fil[0]).readlines()[3:][start_conf:]
    iters = np.array([line.split()[0] for line in lines],float)
    ens = np.array([line.split()[2] for line in lines],float)
    return iters,ens


def analyze_LLG_results(args,lat_type=1,dt=0,
    outdir='.',prefix='',fil_cfg='',jump=1,quiver_kws=None,anim=True):

    spin_plot_kwargs = get_spin_plot_kwargs(args)
    spin_anim_kwargs = get_spin_anim_kwargs(args)
    spin_plot_kwargs.update(quiver_kws=quiver_kws)
    spin_anim_kwargs.update(quiver_kws=quiver_kws)


    if outdir=='.': outdir=os.getcwd()
    print ('spirit input file: {}\n'.format(fil_cfg))
    latt,pos,nx,ny,nz,nat,dt = get_params_from_cfg(fil_cfg,args.nx,args.ny,args.nz,dt=dt)

    def display_snapshot(pos,latt,outdir,prefix,status='initial',show=False):
        superlatt = np.dot(np.diag([nx,ny]),latt)
        fils=glob.glob('{}/{}*Spins-{}.ovf'.format(outdir,prefix,status))
        if len(fils)>0: 
            fil_ovf = fils[0]
            print ('\nDisplay config of file {}'.format(fil_ovf))
            spins = parse_ovf_1(fil_ovf)[1]
            conf = spins.reshape(ny,nx,nat,3)
            conf = np.swapaxes(conf,0,1)
            spin_plot_kwargs.update(title=status,superlatt=superlatt,
            show=show,save=True,figname='{}_spin_conf'.format(status))
            plot_spin_2d(pos,conf, **spin_plot_kwargs)
        else:
            print ('\nFile for display not found at\n{}'.format(outdir))


    def plot_energy(iters,dt,ens,show=True):
        assert dt>0, 'Time step should be positive!'
        fig,ax=plt.subplots(1,1)
        ax.plot(iters*dt,ens)
        ax.set_xlabel('t (ps)')
        ax.set_ylabel('E (meV/site)')
        fig.tight_layout()
        fig.savefig('LLG_energies_profile',dpi=300)
        if show: plt.show()

    try: 
        iters,ens = get_energy_from_txt(0,outdir,prefix)
        plot_energy(iters,dt,ens)
    except:
        print ('Fail to read energy from txt file, skip plotting energy')

    latt = np.array(latt)[:2,:2].T
    if nx*ny*nz!=0:
        nat = pos.shape[0]//(nx*ny)
        pos=pos.reshape(ny,nx,nat,3)
        pos = np.swapaxes(pos,0,1)
        display_snapshot(pos,latt,outdir,prefix,'initial')
        display_snapshot(pos,latt,outdir,prefix,'final',show=True)

    if anim:
        titles = None
        fil = glob.glob('{}/{}*Spins-archive.ovf'.format(outdir,prefix))
        if len(fil)==1:
            fil = fil[0]
            print ('\nSpin configs from achive file {}'.format(fil))
            Iter = np.array([line.split()[-1] for line in os.popen('grep Iteration {}'.format(fil)).readlines()],int)
            titles = ['t = {:10.4f} ps'.format(tt) for tt in Iter*dt]
            confs = parse_ovf_1(fil,parse_params=False)[1]
        else:
            confs = collect_confs_from_ovfs(outdir,prefix)
        confs = confs.reshape(-1,ny,nx,nat,3)
        confs = np.swapaxes(confs,1,2)
        spin_anim_kwargs.update(latt=latt)
        make_ani(pos, confs, titles=titles, **spin_anim_kwargs)
    
        #under development
        #confs_repeat = np.array([get_repeated_conf(conf,args.repeat_x,args.repeat_y) for conf in confs])
        #pos_repeat = np.tile(pos,(args.repeat_x,args.repeat_y,1,1))
        #for ix,iy in np.ndindex(args.repeat_x,arge.repeat_y):
        #    pos_repeat[ny*ii:ny*(ii+1),:,:,1] += ii*latt[1,1]
        #make_ani(pos_repeat, confs_repeat, titles=titles, **spin_anim_kwargs)

    return 1


def gen_args():
    import argparse
    prog='analyze_Spirit_results.py'
    description = 'post-processing of Spirit LLG simulations'
    parser = argparse.ArgumentParser(prog=prog,description=description)
    add_switch_arguments(parser)
    add_llg_arguments(parser)
    add_spirit_arguments(parser)
    add_quiver_arguments(parser)
    add_spin_plot_arguments(parser)
    add_common_arguments(parser)
    args = parser.parse_args()
    return args

if __name__=='__main__':
    args = gen_args()
    quiver_kws = dict([(k.split('_')[1],v) for (k,v) in vars(args).items() if k.startswith('quiver')])
    quiver_kws.update(pivot='mid',units='x')
    print ('keyword arguments for quivers\n')
    for key in quiver_kws.keys(): print ('{:>15s} = {}'.format(key,quiver_kws[key]))

    fil_cfg = args.spirit_input_file
    print ('\ntask = {}\n'.format(args.job))
    if args.job=='llg':     
        kwargs = dict(
        fil_cfg=args.spirit_input_file,
        outdir=args.outdir,prefix=args.prefix,
        quiver_kws=quiver_kws,
        anim=args.make_ani,
        dt=args.dt)
        analyze_LLG_results(args,**kwargs)
    elif args.job=='gneb':  analyze_GNEB_results()
