#!/usr/bin/env python

#==========================================================
# import arguments for LLG simulations and post-processing
# last updated: Jan 11 2021
# Shunhong Zhang <szhang2@ustc.edu.cn>
#==========================================================

import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):    return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):  return False
    else: raise argparse.ArgumentTypeError('Unsupported value encountered.')


desc_str = 'arguments for llg simulation and plotting'


def add_switch_arguments(parser):
    parser.add_argument('--colorful_quiver',type=str2bool,default=False,help='plot colorful or black quiver for spin')
    parser.add_argument('--colorbar',type=str2bool,default=True,help='plot colorbar for the spin mapping')
    parser.add_argument('--plot_summary',type=str2bool,default=True,help='plot summary of LLG simulation')
    parser.add_argument('--plot_struct_factor',type=str2bool,default=False,help='plot structure factor for the fianl conf')
    parser.add_argument('--plot_superlatt',type=str2bool,default=True,help='plot the superlattice with dashed lines')
    parser.add_argument('--plot_out',type=str2bool,default=False,help='plot with out file, deprecated for new versions')
    parser.add_argument('--make_ani',type=str2bool,default=True,help='make animation from LLG simulation snapshots')
    parser.add_argument('--savegif',type=str2bool,default=False,help='save animation to gif')
    parser.add_argument('--display',type=str2bool,default=True,help='Display snapshots (initial, latest, final, etc.)')
    parser.add_argument('--write_latest',type=str2bool,default=False,help='Extract latest config and write to ovf file')
    parser.add_argument('--dump_confs',type=str2bool,default=True,help='Dump the spin configurations to pickle, for restarting')
    parser.add_argument('--pick_confs',type=str2bool,default=False,help='Load the spin configurations from pickle, if exists')
    return parser


def add_mc_arguments(parser):
    parser.add_argument('--task',type=str,default='thermal',help='task for post processing of MC simulation results')
    parser.add_argument('--mc_file',type=str,default='mc.py',help='scirpt name for Monte Carlo simulation, used in post-processing')
    parser.add_argument('--start_conf_idx',type=int,default=0,help='index of the first snapshot to calculate ensemble average')
    parser.add_argument('--itemp',type=int,default=0,help='index for temperature points')
    parser.add_argument('--iconf',type=int,default=0,help='index for snapshot configuration')
    parser.add_argument('--outdir',type=str,default='.',help='directory to store MC data')


def add_llg_arguments(parser):
    #parser.add_argument('--',type=,default=,help='')
    parser.add_argument('--dt',type=float,default=0.001,help='time step for LLG')
    parser.add_argument('--lat_type',type=str,default='honeycomb',help='type of spin lattice')
    parser.add_argument('--solid_angle_method',type=int,default=2,help='method to calculate the solid angle (for topological charge)')
    parser.add_argument('--llg_file',type=str,default='llg.py',help='scirpt name for llg simulation, used in post-processing')
    parser.add_argument('--struct_factor_colormap',type=str,default='parula',help='colormap for structure factor plots')
    parser.add_argument('--struct_factor_scatter_size',type=int,default=30,help='scatter size for structure factor plots')
    parser.add_argument('--snapshot_idx',type=int,default=None,help='index of snapshot to display')
    parser.add_argument('--init_ovf',type=str,default='initial_spin_confs.ovf',help='ovf file for initial spin configuration')
    parser.add_argument('--final_ovf',type=str,default='final_spin_confs.ovf',help='ovf file for final spin configuration')

    return parser


def add_spirit_arguments(parser):
    parser.add_argument('--spirit_input_file',type=str,default='input.cfg',help='filename of Spirit input, for post processing')
    parser.add_argument('--job',type=str,default='llg',help='job type of Spriit runs')
    return parser


def add_common_arguments(parser):
    parser.add_argument('--outdir',type=str,default='.',help='directory to store outputs')
    parser.add_argument('--prefix',type=str,default='',help='prefix for the output file of LLG simulations')
    parser.add_argument('--nx',type=int,default=0,help='dimension in x')
    parser.add_argument('--ny',type=int,default=0,help='dimension in y')
    parser.add_argument('--nz',type=int,default=0,help='dimension in z')


def add_quiver_arguments(parser):
    parser.add_argument('--quiver_scale',type=float,default=1,help='scale of arrow in plotting in-plane spin components')
    parser.add_argument('--quiver_width',type=float,default=0.1,help='width of arrow in plotting in-plane spin components')
    parser.add_argument('--quiver_headlength',type=float,default=5,help='length of arrows in 2d spin plot')
    parser.add_argument('--quiver_headwidth',type=float,default=3,help='length of arrows in 2d spin plot')
    parser.add_argument('--quiver_headaxislength',type=float,default=3,help='length of arrows in 2d spin plot')


def add_spin_plot_arguments(parser):
    parser.add_argument('--color_mapping',type=str,default='Sz_full',help='quantity used for color mapping in 2d spin plot')
    parser.add_argument('--xs',type=int,default=1,help='plot 1 per xs sites along x direction in 2d spin plot')
    parser.add_argument('--ys',type=int,default=1,help='plot 1 per ys sites along y direction in 2d spin plot')
    parser.add_argument('--site_plot_idx',default=-1,help='index of sites (in unit cell) to plot spin texture')
    parser.add_argument('--title',type=str,default='spin',help='title for spin plot')
    parser.add_argument('--repeat_x',type=int,default=1,help='repeat periodic images along x')
    parser.add_argument('--repeat_y',type=int,default=1,help='repeat periodic images along y')
    parser.add_argument('--scatter_size',type=int,default=5,help='scatter size in 2d spin plot')

    parser.add_argument('--framework',type=str2bool,default=False,help='plot framework in 2d spin configuration')
    parser.add_argument('--colormap',type=str,default='rainbow',help='colormap for out-of-plane component in 2d spin plot')
    parser.add_argument('--colorbar_orientation',type=str,default='auto',help='orientation of colorbar')
    parser.add_argument('--colorbar_shrink',type=float,default=0.3,help='shrink ratio of  the colorbar')
    parser.add_argument('--colorbar_axes_position',type=eval,default=None,help='position of addtional axis for colorbar')

    parser.add_argument('--topo_chg',type=str2bool,default=True,help='calculate and plot topological charges distrbution')
    parser.add_argument('--Q_colormap',type=str,default='bwr',help='colormap for topological charge distribution')
    parser.add_argument('--Q_color_mapping',type=str,default='Q_full',help='quantities used for color mapping in topo chg plot')
    parser.add_argument('--Qmax',type=float,default=-0.1,help='max Q value for color mapping')
    parser.add_argument('--Qmin',type=float,default= 0.1,help='min Q value for color mapping')

    parser.add_argument('--jump_images',type=int,default=5,help='no. of images to jump in making animation')
    parser.add_argument('--mapping_all_sites',type=str2bool,default=True,help='color mapping for all sites or for sites with quiver only')
    parser.add_argument('--interval',type=float,default=0.5e3,help='time step for animation')
    parser.add_argument('--width_ratios', type=eval,default=(8,1),help=' width ratio for main plot and colorbar')
    parser.add_argument('--height_ratios',type=eval,default=(8,1),help='height ratio for main plot and colorbar')
    parser.add_argument('--gif_dpi',type=int,default=200,help='dpi of gif file for animation')
    parser.add_argument('--gif_name',type=str,default='LLG.ani',help='file name of saved gif (animation)')

def get_args(fil='asd_arguments.py'):
    parser = argparse.ArgumentParser(prog=fil, description = desc_str)
    args = parser.parse_args()
    return parser,args


def get_spin_plot_kwargs(args):
    keys = ['color_mapping','xs','ys','site_plot_idx',
    'scatter_size','framework','colormap',
    'colorful_quiver',
    'colorbar','colorbar_orientation','colorbar_shrink','colorbar_axes_position',
    'Q_colormap','Qmax','Qmin','mapping_all_sites',
    'width_ratios','height_ratios']
    spin_plot_kwargs={}
    for key in keys: spin_plot_kwargs.setdefault(key,vars(args)[key])
    spin_plot_kwargs.setdefault('save',True)
    return spin_plot_kwargs


def get_spin_anim_kwargs(args):
    keys = ['color_mapping','xs','ys','site_plot_idx',
    'scatter_size','framework','colormap',
    'colorful_quiver',
    'colorbar','colorbar_orientation','colorbar_shrink','colorbar_axes_position',
    'interval','mapping_all_sites', 'width_ratios','height_ratios',
    'savegif','gif_dpi','gif_name']
    spin_anim_kwargs={}
    for key in keys: spin_anim_kwargs.setdefault(key,vars(args)[key])
    spin_anim_kwargs.update(jump=args.jump_images)
    return spin_anim_kwargs


if __name__=='__main__':
    print ('This is a collection of arguments for llg tools')
