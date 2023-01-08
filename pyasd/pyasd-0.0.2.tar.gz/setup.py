#!/usr/bin/env python

#===========================================================================#
#                                                                           #
#  File:       setup.py                                                     #
#  Author:     Shunhong Zhang                                               #
#  Date:       Jan 04, 2023                                                 #
#                                                                           #
#===========================================================================#


from __future__ import print_function
import sys
import os
import glob
from utility_setup import *
import time
#from distutils.core import setup  # deprecated soon
import setuptools


core_modules = [
'constants',
'random_vectors',
'shell_exchange',
'geometry',
'spin_configurations',
'spin_correlations',
'hamiltonian',
'topological_charge',
'log_general',
'llg_simple',
'llg_advanced',
'monte_carlo',
'gneb',
]

utility_modules = [
'head_figlet',
'plot_tools_3d',
'auxiliary_colormaps',
'asd_arguments',
'Swq',
'ovf_tools',
'spin_visualize_tools',
'spirit_tool',
'mag_thermal',
'post_llg',
'post_mc',
'analyze_Spirit_results',
'four_state_tools',
'curve_fit',
]

platform = sys.platform
database_modules = glob.glob('asd/data_base/exchange_*py')
database_modules = [item.rstrip('.py') for item in database_modules]
init_files = ['asd/__init__']
core_modules  = ['asd/core/{}'.format(item) for item in core_modules]
utility_modules  = ['asd/utility/{}'.format(item) for item in utility_modules]
mpi_modules = ['asd/mpi/mpi_tools']


kwargs_setup = dict(
name='pyasd',
version='0.0.2',
author='Shunhong Zhang',
author_email='zhangshunhong.pku@gmail.com',
url='https://to_be_posted',
download_url='https://on_request',
keywords='spin dynamics simulation',
py_modules = utility_modules + core_modules + database_modules + mpi_modules + init_files,
packages = setuptools.find_packages(),
license='LICENSE',
license_file='LICENSE',
description='A python-based spin dynamics simulator',
long_description='LLG/Monte Carlo/GNEB simulators for classical spin systems',
platforms=[sys.platform],
install_requires=[
'numpy',
'scipy',
'matplotlib',
'mpi4py',
'pyfiglet',
'ovf'],
classifiers=[
'Programming Language :: Python :: 3',],
)

      
bindirs = ['{}/asd/utility'.format(os.getcwd())]


def set_build_time_stamp(kwargs_setup):
    with open('asd/__init__.py','r') as fw: lines = fw.readlines()
    __doc__ = '{:<20s}  =  "built at {} {}"\n'.format('__built_time__',time.ctime(),time.tzname[1])
    lines = [__doc__] + [line for line in lines if '__built_time__' not in line]
    with open('asd/__init__.py','w') as fw: 
        fw.write(__doc__)
        for key in ['__name__','__version__','__author__','__author_email__','__url__','__license__']:
            print ('{:<20s}  =  "{}"'.format(key,kwargs_setup[key.strip('__')]),file=fw)
 
 
 
if __name__=='__main__':
    set_build_time_stamp(kwargs_setup)
    print('\n{0}\nINSTALL\n{0}'.format('='*50))
    #setup(**kwargs_setup)  # deprecated soon
    setuptools.setup(**kwargs_setup)
    test_modules(core_modules,     'core modules')
    test_modules(utility_modules,  'utility_modules')
    test_modules(database_modules, 'materials database')
    set_path(bindirs)
    print ('\n{0}\nDone\n{0}\n'.format('='*50))
