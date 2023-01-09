# Input generation of vasp input files using config files and templates

import os
import sys
import configparser as cp


def generate_input(incar_template):
    config = cp.ConfigParser()
    config.read('host.ini')
    hostname = config['host']['hostname']
    architecture = config['host']['architecture']
    potpaw_location = config['host']['potpaw']
    config = cp.ConfigParser()
    config.read(incar_template)
    with open('INCAR', 'w') as f:
        for section in config.sections():
            for key in config[section]:
                key = key.upper()
                f.write(f'''{key} = {config[section][key]}
''')
    with open('POTCAR','a') as f:
        f.truncate(0)
        with open('POSCAR','r') as g:
            poscar = []
            for lines in g:
                stripped_lines = lines.strip()
                poscar.append(stripped_lines)
            atoms = poscar[5].split()
            potpaw = ['H', 'He', 'Li_sv', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na_pv', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K_sv', 'Ca_sv', 'Sc_sv', 'Ti_sv', 'V_sv', 'Cr_pv', 'Mn_pv', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga_d', 'Ge_d', 'As', 'Se', 'Br', 'Kr', 'Rb_sv', 'Sr_sv', 'Y_sv', 'Zr_sv', 'Nb_sv', 'Mo_sv', 'Tc_pv', 'Ru_pv', 'Rh_pv', 'Pd', 'Ag', 'Cd', 'In_d', 'Sn_d', 'Sb', 'Te', 'I', 'Xe', 'Cs_sv', 'Ba_sv', 'La', 'Ce_3', 'Nd_3', 'Pm_3', 'Sm_3', 'Eu_2', 'Gd_3', 'Tb_3', 'Dy_3', 'Ho_3', 'Er_3', 'Tm_3', 'Yb_2', 'Lu_3', 'Hf_pv', 'Ta_pv', 'W_sv', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl_d', 'Pb_d', 'Bi_d', 'Po_d', 'At', 'Rn', 'Fr_sv', 'Ra_sv', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm']
            potpaw_f = []
            for i in range(len(atoms)):
                for j in potpaw:
                    k = j.split('_')
                    if atoms[i] == k[0]:
                            potpaw_f.append(j)
            cwd = os.getcwd()
            os.system('cd ')
            os.system('module load vasp')
            os.chdir(potpaw_location)
            for i in potpaw_f:
                os.chdir(f'{i}')
                with open('POTCAR','r') as d:
                    for line in d:
                        f.write(line)
                os.chdir('../')
            os.chdir(cwd)

def generate_job(job_template, title):
    config = cp.ConfigParser()
    config.read('host.ini')
    hostname = config['host']['hostname']
    architecture = config['host']['architecture']
    potpaw_location = config['host']['potpaw']
    config = cp.ConfigParser()
    config.read(job_template)
    version = config['job']['version']
    nodes = config['job']['nodes']
    cores = config['job']['cores']
    module_location = config['job']['module_location']
    vasp_type = config['job']['vasp_type']
    if architecture == 'slurm':
        with open('submit.sh','w') as f:
            f.truncate(0)
            f.write(f'''#!/bin/bash
#SBATCH -p {nodes}       
#SBATCH -n {cores}
#SBATCH --job-name="{title}"

echo "Starting run at: `date`"

module load {module_location}
module load anaconda3/2020.07

# Call VASP directly.

mpirun -np {cores} {vasp_type}

echo "Job finished with exit code $? at: `date`"
''')
      
        with open('slurm_Opt.sh','r') as f:
            opt = f.read()
        with open('Opt.sh','w') as f:
            f.write(opt)

    elif architecture == 'sqe':
         if nodes == 'multicore':
            with open('submit.sh','w') as f:
                f.truncate(0)
                f.write(f'''#!/bin/bash --login
#$ -cwd             # Job will run from the current directory
#$ -pe smp.pe {cores}
#$ -N '{title}'

echo "Starting run at: `date`"

module load {module_location}

mpirun -n $NSLOTS {vasp_type}

echo "Job finished with exit code $? at: `date`"
''')
         if nodes == 'multinode':
             with open('submit.sh','w') as f:
                 f.truncate(0)
                 f.write(f'''#!/bin/bash --login
#$ -cwd                       # Job will run from the current directory
#$ -pe mpi-24-ib.pe {cores}
#$ -N '{title}'

module load {module_location}

mpirun -n $NSLOTS {vasp_type}

echo "Job finished with exit code $? at: `date`"               
''')
         with open('sge_Opt.sh','r') as f:
             opt = f.read()
         with open('Opt.sh','w') as f:
             f.write(opt)
    elif architecture == 'local':
        with open('submit.sh','w') as f:
            f.truncate(0)
            f.write(f'''nohup mpirun -n {cores} {vasp_type} > output01.txt &''')

    else:
        print('Architecture not supported')
    

