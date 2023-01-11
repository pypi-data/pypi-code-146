# Input generation of vasp input files using config files and templates
"""
A module for generating vasp input and submission files using config files and templates.
"""
import os
import sys
import configparser as cp


def generate_input(incar_template):
    '''
    Generates the INCAR, and POTCAR files used to perform VASP calculations.

    Parameters
    ----------
    incar_template : str 

    Configuration files
    -------------------
    The incar_template file is a configuration file that contains the parameters for the INCAR file.
    The configuration file is a standard .ini file. The parameters are the same as those in the INCAR file.
    The parameters are read in as strings, and are converted to the appropriate type when the INCAR file is generated.
    The configuration files can be generated using the generate_config program.

    NOTE
    ----
    This program requires the use of a HOST configuration file.
    The HOST configuration file contains the information about the host machine.
    This includes:
        - The hostname
        - The architecture of the host machine and the subprocess it uses
        - The location of the POTPAW pseudopotential files on the host machine
    '''

    config = cp.ConfigParser()
    # create a variable for the vasp_templates directory inside the home directory and join it to the host.ini file 
    host_file = os.path.join(os.path.expanduser('~'),'vasp_templates','host.ini')
    config.read(host_file)
    hostname = config['host']['hostname']
    architecture = config['host']['architecture']
    potpaw_location = config['host']['potpaw']
    config = cp.ConfigParser()
    input_file = os.path.join(os.path.expanduser('~'),'vasp_templates',incar_template)
    config.read(input_file)
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

def generate_job(job_template, title, opt):
    '''
    Generates the job submission script for the VASP calculation.

    Parameters
    ----------
    job_template : str
        The name of the job template file.
    title : str 

    Configuration files
    -------------------
    The job_template file is a configuration file that contains the parameters for the job submission script.
    The configuration file is a standard .ini file. The parameters are the same as those in the job submission script.
    The parameters are used to generate the job submission script based upon the subprocess 

    NOTE
    ----
    This program requires the use of a HOST configuration file.
    The HOST configuration file contains the information about the host machine.
    This includes:
        - The hostname
        - The architecture of the host machine and the subprocess it uses
        - The location of the POTPAW pseudopotential files on the host machine
    '''

    config = cp.ConfigParser()
    host_file = os.path.join(os.path.expanduser('~'),'vasp_templates','host.ini')
    config.read(host_file)
    hostname = config['host']['hostname']
    architecture = config['host']['architecture']
    potpaw_location = config['host']['potpaw']
    config = cp.ConfigParser()
    job_file = os.path.join(os.path.expanduser('~'),'vasp_templates',job_template)
    config.read(job_file)
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
      
        with open('Opt.sh','w') as f:
            f.write(f'''#!/bin/bash --login
#SBATCH -p {nodes}
#SBATCH -n {cores}
#SBATCH --job-name="{title}"

# Check to see if the required files to run vasp are in the cwd if not exit job. 
if test -e 'INCAR' && test -e 'POSCAR' && test -e 'POTCAR'; then
   echo "Submission files located"
else
   echo "Submission files missing exit with code 1 at: `date`"
   exit 1;
fi

module load {module_location}
module load anaconda3/2020.07

run_num=0
running=True
while running=True
do
    
    echo "Started running at: `date`"
    
    mpirun -np {cores} {vasp_type} >> vasp.out

    let run_num++

    conv=$(grep "reached required accuracy" vasp.out | wc -l)

    # check to see if the calculation has converged
''')
        with open('Opt.sh','a') as f:
            f.write('''
    if [[ "$conv" == 1 ]]; then
        E=$(awk '/F=/ {print}' OSZICAR)
        echo 'RUN NUMBER: ' $run_num
        echo $E
        echo "Job finished with exit code 0 at: `date`"
        mkdir  Opt-$run_num
        cp {CHG,CHGCAR,CONTCAR,DOSCAR,EIGENVAL,IBZKPT,INCAR,KPOINTS,OSZICAR,OUTCAR,PCDAT,POSCAR,POTCAR,REPORT,vasp.out,WAVECAR,XDATCAR} Opt-$run_num
        cp CONTCAR POSCAR.opt
        rm CHG CHGCAR CONTCAR DOSCAR EIGENVAL IBZKPT OSZICAR OUTCAR PCDAT REPORT WAVECAR XDATCAR vasprun.xml
        break
     elif [[ "$run_num" == 15 ]]; then
        E=$(awk '/F=/ {print}' OSZICAR)
        echo 'RUN NUMBER: ' $run_num
        echo $E
        echo "Running iteration limit reached: 15, Job finished with exit code 0 at: `date`"
        cp {CHG,CHGCAR,CONTCAR,DOSCAR,EIGENVAL,IBZKPT,INCAR,KPOINTS,OSZICAR,OUTCAR,PCDAT,POSCAR,POTCAR,REPORT,vasp.out,WAVECAR,XDATCAR} Opt-$run_num
        cp CONTCAR POSCAR
        rm CHG CHGCAR CONTCAR DOSCAR EIGENVAL IBZKPT OSZICAR OUTCAR PCDAT REPORT WAVECAR XDATCAR vasprun.xml
        break
    else
        E=$(awk '/F=/ {print}' OSZICAR)
        echo 'RUN NUMBER: ' $run_num
        echo $E
        mkdir  Opt-$run_num
        cp {CHG,CHGCAR,CONTCAR,DOSCAR,EIGENVAL,IBZKPT,INCAR,KPOINTS,OSZICAR,OUTCAR,PCDAT,POSCAR,POTCAR,REPORT,vasp.out,WAVECAR,XDATCAR} Opt-$run_num
        cp CONTCAR POSCAR
        rm CHG CHGCAR CONTCAR DOSCAR EIGENVAL IBZKPT OSZICAR OUTCAR PCDAT REPORT vasp.out WAVECAR XDATCAR vasprun.xml
        echo "Number of iterations reached NSW, job finished at: `date`"
        echo " "
        echo " "
    fi
done
''')
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
         with open('Opt.sh','w') as f:
             f.write(f'''#!/bin/bash --login
#$ -cwd             
#$ -pe smp.pe {cores}
#$ -N '{title}'

# Check to see if the required files to run vasp are in the cwd if not exit job. 
if test -e 'INCAR' && test -e 'POSCAR' && test -e 'POTCAR'; then
   echo "Submission files located"
else
   echo "Submission files missing exit with code 1 at: `date`"
   exit 1;
fi

module load {module_location}
module load anaconda3/2020.07

run_num=0
running=True
while running=True
do
    
    echo "Started running at: `date`"
    
    mpirun -np {cores} {vasp_type} >> vasp.out

    let run_num++

    conv=$(grep "reached required accuracy" vasp.out | wc -l)

    # check to see if the calculation has converged
''')
         with open('Opt.sh','a') as f:
             f.write('''
    if [[ "$conv" == 1 ]]; then
        E=$(awk '/F=/ {print}' OSZICAR)
        echo 'RUN NUMBER: ' $run_num
        echo $E
        echo "Job finished with exit code 0 at: `date`"
        mkdir  Opt-$run_num
        cp {CHG,CHGCAR,CONTCAR,DOSCAR,EIGENVAL,IBZKPT,INCAR,KPOINTS,OSZICAR,OUTCAR,PCDAT,POSCAR,POTCAR,REPORT,vasp.out,WAVECAR,XDATCAR} Opt-$run_num
        cp CONTCAR POSCAR.opt
        rm CHG CHGCAR CONTCAR DOSCAR EIGENVAL IBZKPT OSZICAR OUTCAR PCDAT REPORT WAVECAR XDATCAR vasprun.xml
        break
     elif [[ "$run_num" == 15 ]]; then
        E=$(awk '/F=/ {print}' OSZICAR)
        echo 'RUN NUMBER: ' $run_num
        echo $E
        echo "Running iteration limit reached: 15, Job finished with exit code 0 at: `date`"
        cp {CHG,CHGCAR,CONTCAR,DOSCAR,EIGENVAL,IBZKPT,INCAR,KPOINTS,OSZICAR,OUTCAR,PCDAT,POSCAR,POTCAR,REPORT,vasp.out,WAVECAR,XDATCAR} Opt-$run_num
        cp CONTCAR POSCAR
        rm CHG CHGCAR CONTCAR DOSCAR EIGENVAL IBZKPT OSZICAR OUTCAR PCDAT REPORT WAVECAR XDATCAR vasprun.xml
        break
    else
        E=$(awk '/F=/ {print}' OSZICAR)
        echo 'RUN NUMBER: ' $run_num
        echo $E
        mkdir  Opt-$run_num
        cp {CHG,CHGCAR,CONTCAR,DOSCAR,EIGENVAL,IBZKPT,INCAR,KPOINTS,OSZICAR,OUTCAR,PCDAT,POSCAR,POTCAR,REPORT,vasp.out,WAVECAR,XDATCAR} Opt-$run_num
        cp CONTCAR POSCAR
        rm CHG CHGCAR CONTCAR DOSCAR EIGENVAL IBZKPT OSZICAR OUTCAR PCDAT REPORT vasp.out WAVECAR XDATCAR vasprun.xml
        echo "Number of iterations reached NSW, job finished at: `date`"
        echo " "
        echos " "
    fi
done
''')
    elif architecture == 'local':
        with open('submit.sh','w') as f:
            f.truncate(0)
            f.write(f'''nohup mpirun -n {cores} {vasp_type} > output01.txt &''')

    else:
        print('Architecture not supported')
    
