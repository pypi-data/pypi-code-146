#vasp_suite.py>

#Imports
import os
from textwrap import dedent
import numpy as np
import argparse
import socket
from gemmi import cif
from pymatgen.core.lattice import Lattice
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.electronic_structure.core import Orbital
from matplotlib import transforms
import matplotlib.pyplot as plt 

class ParseExtra(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, [[], {}])
        for key, val in values:
            if val is None:
                getattr(namespace, self.dest)[0].append(key)
            else:
                getattr(namespace, self.dest)[1][key] = val

#RAW_Functions
def generate_input(calc_type,functional,ENCUT,mesh):
    hostname = socket.gethostname()
    if not 'csf' in hostname:
        print('''
 ------------------------------------------------------------------------------------------
|                               Unknown Architecture !!!                                   |
|                                                                                          |
|   The architecture detected by vasp_suite is unknown. The creation of the POTCAR file    |
|   cannot be completed: path to POTPAW files in unkown!                                   |
|                                                                                          |
|  Vasp suite will create an empty POTCAR file to be ammended by the user.                 |
 ------------------------------------------------------------------------------------------
''')


    with open('INCAR','a') as f:
        f.truncate(0)
        calc_type = calc_type.lower()
        functional = functional.lower()
        ENCUT = ENCUT.lower()
        mesh = [int(i) for i in str(mesh)]
        f.write('''!GENERAL
PREC = accurate
LREAL = .FALSE.
LASPH = .TRUE.
ISMEAR = 0
SIGMA = 0.01
NELM = 150
NELMMIN = 6
IVDW = 11
NCORE = 4
!CONVERGENCE
EDIFF = 1.E-8
EDIFFG = -1.E-2
''')
        if calc_type == 'relaxation':
            f.write('''!RELAXATION
IBRION = 2
POTIM = 0.1
ISIF = 3
NSW = 250
!OUTPUT
LWAVE = .FALSE.
LCHARG = .FALSE.
''')
        if calc_type == 'scf':
            f.write('''!SELF CONSISTENT FIELD
IBRION = -1
NSW = 0
!OUTPUT
LWAVE = .FALSE.
LCHARG = .TRUE.
''')
        if calc_type == 'efield':
            field_direction = input('Field Direction (1=x, 2=y, 3=z, 4=All) ')
            field_strength = input('Field strength (eV/Å) ')
            f.write(f'''!RELAXATION
IBRION = 2
POTIM = 0.1
ISIF = 3
NSW = 250
!OUTPUT
LWAVE = .FALSE.
LCHARG = .FALSE.
!EFIELD
!Electric Field
EFIELD = {field_strength}
IDIPOL = {field_direction}
LDIPOL = .FALSE.
''')
        if calc_type == 'molecular_dynamics':
            nsw = input('NSW: ')
            pomass = input('POMASS: ')
            potim = input('POTIM: ')
            smass = input('SMASS: ')
            tebeg = input('TEBEG: ')
            teend = input('TEEND: ')
            f.write(f'''!Molecular Dynamics
ML_LMLFF = .TRUE.
ML_ISTART = 1
IBRION = 0
NSW = {nsw}
POMASS = {pomass}
POTIM = {potim}
SMASS = {smass}
TEBEG = {tebeg}
TEEND = {teend}
!OUTPUT
LWAVE = .FALSE.
LCHARG = .FALSE.
''')


        if functional =='pbe0':
            f.write('''!FUNCTIONAL = PBE0
LHFCALC = .TRUE.
GGA = PE
''')
        if functional == 'b3lyp':
            f.write('''!FUNCTIONAL = B3LYP
LHFCALC = .TRUE. 
GGA     = B3
AEXX    = 0.2
AGGAX   = 0.72 
AGGAC   = 0.81 
ALDAC   = 0.19
''')
        if functional == 'pbe':
            f.write('''!FUNCTIONAL = PBE
GGA = PE
''')
        if functional == 'scan':
            f.write('''!FUNCTIONAL = SCAN
METAGGA = SCAN
BPARAM = 6.3
ADDGRID = .TRUE.
''')
        if functional == 'scan+rvv10':
            f.write('''!FUNCTIONAL = SCAN+rVV10
METAGGA = SCAN
BPARAM = 15.7
LUSE_VDW = .TRUE.
ADDGRID = .TRUE.
''')

        if functional == 'pbe+u':
            u_param = input('input the +U parameters in the order the atoms appear in the POSCAR: ').split()
            #u_param = [float(x) for x in u_param]
            u = " ".join(u_param)
            f.write(f'''!FUNCTIONAL = PBE+U
LDAU = .TRUE.
LDAUTYPE = 2 
''')
            
            f.write(f'''LDAUU = {u}
''')
            uj = []
            for i in u_param:
                uj.append(0)
            uj = [str(x) for x in uj]
            uj = " ".join(uj)
            f.write(f'''LDAUJ = {uj}
''')

            ul = []
            u_param = [float(x) for x in u_param]
            for i in u_param:
                if i > 0:
                    ul.append(2)
                else:
                    ul.append(-1)
            ul = [str(x) for x in ul]
            ul = " ".join(ul)
            f.write(f'''LDAUL = {ul}
''') 
            

        f.write('''!CUT OFF VALUE
''')
        f.write(f'''ENCUT = {ENCUT}
''')

    with open('KPOINTS','w') as f:
            f.truncate(0)
            f.write(f'''Regular {mesh[0]} x {mesh[1]} x {mesh[2]} mesh centered at Gamma
0
Gamma
{mesh[0]} {mesh[1]} {mesh[2]}
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
            if 'csf4' in hostname:
                cwd = os.getcwd()
                os.system('cd ')
                os.system('module load vasp')
                os.chdir('/opt/software/RI/apps/VASP/5.4.4-iomkl-2020.02/pseudopotentials/potpaw_PBE.54')
            if 'csf3' in hostname:
                cwd = os.getcwd()
                os.system('cd ')
                os.system('module load apps/intel-17.0/vasp/5.4.4')
                os.chdir('/opt/apps/apps/intel-17.0/vasp/5.4.4/pseudopotentials/potpaw_PBE.54')
            for i in potpaw_f:
                os.chdir(f'{i}')
                with open('POTCAR','r') as d:
                    for line in d:
                        f.write(line)
                os.chdir('../')
            os.chdir(cwd)
    
    return

def generate_job(version,nodes,cores,title,vasp_type):
    hostname = socket.gethostname()
    if 'csf' in hostname:
        version = version.lower()
        nodes = nodes.lower()
        vasp_type = vasp_type.lower()
        if 'csf4'in hostname:
            with open('submit.sh','w') as f:
                f.truncate(0)
                f.write(f'''#!/bin/bash
#SBATCH -p {nodes}       
#SBATCH -n {cores}
#SBATCH --job-name="{title}"

echo "Starting run at: `date`"

module load vasp/{version}-iomkl-2020.02
module load anaconda3/2020.07

# Call VASP directly.

mpirun -np {cores} {vasp_type}

# Run VASP via Python scripts.

#python Conv.py
#python Opt.py

echo "Job finished with exit code $? at: `date`"
    ''')
        if 'csf3' in hostname:
            if nodes == 'multicore':
                with open('submit.sh','w') as f:
                    f.truncate(0)
                    f.write(f'''#!/bin/bash --login
#$ -cwd             # Job will run from the current directory
#$ -pe smp.pe {cores}
#$ -N '{title}'
                    # NO -V line - we load modulefiles in the jobscript

echo "Starting run at: `date`"

module load apps/intel-17.0/vasp/5.4.4

mpirun -n $NSLOTS {vasp_type}
                        
# Run VASP via Python scripts.

#python Conv.py
#python Opt.py

echo "Job finished with exit code $? at: `date`"
''')
            if nodes == 'multinode':
                with open('submit.sh','w') as f:
                    f.truncate(0)
                    f.write(f'''#!/bin/bash --login
#$ -cwd                       # Job will run from the current directory
#$ -pe mpi-24-ib.pe {cores}
#$ -N '{title}'

                              # NO -V line - we load modulefiles in the jobscript
module load apps/intel-17.0/vasp/5.4.4

mpirun -n $NSLOTS {vasp_type}

# Run VASP via Python scripts.

#python Conv.py
#python Opt.py

echo "Job finished with exit code $? at: `date`"               
''')

        with open('Opt.py','a') as f:       #add the argument keywords to edit this file too when writing
            f.truncate(0)
            f.write(f'''# Opt.py


JobDirPrefix = "Opt"

RunVASP = r"mpirun -np {cores} {vasp_type}"
''')
        with open('Opt.py','a') as f:
            f.write(r'''import glob
import os
import re
import shutil
import sys


def _CheckComplete(file_path = r"OUTCAR"):
    """
    Inspects an OUTCAR file and (crudely!) determines whether a VASP job has finished cleanly.
    
    Params:
       file_path -- path to an OUTCAR-format file (default: OUTCAR)
    
    Returns:
       Number of ionic steps N if the calculation completed, or -1 otherwise.
    """
    
    # If file_path does not exist, assume VASP failed to start.
    
    if not os.path.isfile(file_path):
        return -1
    
    num_steps = 0
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as input_reader:
            for line in input_reader:
               if "LOOP+" in line:
                   # Identify ionic steps by the "LOOP+" string.
                   
                   num_steps += 1
               
               elif "Voluntary context switches" in line:
                   # Unless a user does something strange this string _should_ only appear in the last line of the OUTCAR.
                   
                   return num_steps
    
    return -1


if __name__ == "__main__":
    # Check required VASP input files are present.
    
    for req_file in r"INCAR", r"POSCAR", r"POTCAR":
        if not os.path.isfile(req_file):
            print(r"Error: Required file '{0}' not found.".format(req_file))
            sys.exit(1)
    
    # Check there are no folders with the set JobDirPrefix.
    # (A smarter script should handle this properly.)
    
    job_dirs = glob.glob(
        "{0}-*".format(JobDirPrefix)
        )
    
    if len(job_dirs) > 0:
        print("Error: Folders with prefix '{0}' already exist - please change JobDirPrefix.".format(JobDirPrefix))
        sys.exit(1)
    
    # Read NSW from INCAR.
    
    nsw = None
    
    nsw_regex = re.compile(
        r"NSW\s*=\s*(?P<nsw>\d+)"
        )
   
    with open(r"INCAR", 'r') as input_reader:
        for line in input_reader:
            match = nsw_regex.search(line)
            
            if match:
                # Specifying the same INCAR tag multiple times is a bad idea...
                
                if nsw is not None:
                    print("Error: NSW specified multiple times in INCAR.")
                    sys.exit(1)
                
                nsw = int(
                    match.group('nsw')
                    )
    
    if nsw is None:
        print("Error: NSW not specified in INCAR.")
        sys.exit(1)
    
    # Keep track of the run number and current POSCAR file.
    # After each successful run, current_poscar is updated to point at the CONTCAR file.
    
    run_num = 1
    current_poscar = r"POSCAR"
    
    # Run VASP until a run does N < NSW steps.
    
    while True:
        # Set up a folder for the current VASP job.
        
        job_dir = r"{0}-{1:0>3}".format(JobDirPrefix, run_num)
        
        os.mkdir(job_dir)
        
        # Copy INCAR/POTCAR and KPOINTS, if required, from the startup directory.
        
        for input_file in r"INCAR", r"POTCAR":
            shutil.copy(
                input_file, os.path.join(job_dir, input_file)
                )
        
        if os.path.isfile(r"KPOINTS"):
            shutil.copy(
                r"KPOINTS", os.path.join(job_dir, r"KPOINTS")
                )
        
        # Copy current_poscar -> POSCAR.
        
        shutil.copy(
            current_poscar, os.path.join(job_dir, r"POSCAR")
            )
        
        # Run VASP.
        
        os.chdir(job_dir)
        
        os.system(
            "{0} | tee \"../{1}.out\"".format(RunVASP, job_dir)
            )
        
        os.chdir("..")
        
        # Check VASP job completed successfully.
        
        result = _CheckComplete(
            r"{0}/OUTCAR".format(job_dir)
            )
        
        if result == -1:
            print("Error: A VASP run failed to complete.")
            sys.exit(1)
        
        # Update current_poscar.
        
        current_poscar = "{0}/CONTCAR".format(job_dir)
        
        # If VASP ran < NSW ionic steps, assume the optimisation is finished and stop.
        
        if result < nsw:
            # If not already present, try and copy the optimised POSCAR to POSCAR.Opt.
            # Otherwise, just print the location of the optimised POSCAR.
            
            if not os.path.isfile(r"POSCAR.Opt"):
                shutil.copy(current_poscar, r"POSCAR.Opt")
                
                print("INFO: Optimised POSCAR copied to POSCAR.Opt.")
                
            else:
                print("INFO: Optimised POSCAR at: {0}".format(current_poscar))
                
            sys.exit(0)
        
        # If not, update run_number and run again.
        
        run_num += 1

''')
    else:
        print('''
 ------------------------------------------------------------------------------------------
|                               Unknown Architecture !!!                                   |
|                                                                                          |
|   The architecture detected by vasp_suite is unknown. The creation of the submission     |
|   files cannot be completed: Submission interpreter unknown?                             |
|   Interpreters supported: slurm, sge, local                                              |
|                                                                                          |
|   vasp_suite will generate a general submission script for your achitecture, please      |
|   note editing of the submission script be required!                                     |
|                                                                                          |
 ------------------------------------------------------------------------------------------
''')
        interpreter = input('Architecture submission interpreter: ')
        interpreter = interpreter.lower()
        if interpreter == 'slurm':
            with open('submit.sh','w') as f:
                f.truncate(0)
                f.write(f'''#!/bin/bash
#SBATCH -p {nodes}       
#SBATCH -n {cores}
#SBATCH --job-name="{title}"

echo "Starting run at: `date`"

module load (_location_of_vasp_module_)

# Call VASP directly.

mpirun -np {cores} {vasp_type}

echo "Job finished with exit code $? at: `date`"
''')
        if interpreter == 'sge':
            with open('submit.sh','w') as f:
                f.truncate(0)
                f.write(f'''#!/bin/bash --login
#$ -cwd             
#$ -pe smp.pe {cores}
#$ -N '{title}'

echo "Starting run at: `date`"

module load (_location_of_vasp_module_)

mpirun -n $NSLOTS {vasp_type}
                        
echo "Job finished with exit code $? at: `date`"
''')
        if interpreter == 'local':
            with open('submit.sh','w') as f:
                f.truncate(0)
                f.write(f'''nohup mpirun -n {cores} {vasp_type} > output01.txt &''')

    return

def structure_compare(path1,path2):
    s1 = []
    s2 = []
    element = []
    element_num = []
    element_ind = []
    cwd = os.getcwd()
    os.system('cd')
    os.chdir(path1)
    with open('POSCAR','r') as f:
        for lines in f:
            split_lines = lines.split()
            s1.append(split_lines)
    os.system('cd')
    os.chdir(path2)
    with open('POSCAR','r') as f:
        for lines in f:
            split_lines = lines.split()
            s2.append(split_lines)
    element.append(s1[5])
    element_num.append(s1[6])
    element_num[0] = [int(x) for x in element_num[0]]
    cumsum_element = np.cumsum(element_num[0])
    element_ind.append(list(cumsum_element))
    
    del s1[0:8], s2[0:8]
    try:
        for i in s1:
            del i[3]
        for i in s2:
            del i[3]
    except:
        pass
    s1_matrix, s2_matrix = np.float_(s1), np.float_(s2)
    matrix_diff = np.subtract(s1_matrix,s2_matrix)
    os.system('cd ')
    os.chdir(cwd)
    with open('structure_compare.txt','w') as f:
        f.truncate(0)
        for i in range(len(matrix_diff)):
            for j in range(len(element[0])):
                if element_ind[0][j] > i and element_ind[0][j] < element_ind[0][j-1]:
                    f.write(f'''Element: {element[0][0]} | Index: {i+1} | Perturbation: {matrix_diff[i]}
''')
                if element_ind[0][j-1] < i <= element_ind[0][j]:
                    f.write(f'''Element: {element[0][j]} | Index: {i+1} | Perturbation: {matrix_diff[i]}
''')
        f.write('''
The following Atoms have been perturbed by more that 0.01 Å

''')
        for i in range(len(matrix_diff)):
            for j in range(len(matrix_diff[i])):
                if element_ind[0][j] > i and element_ind[0][j] < element_ind[0][j-1]:
                    if abs(matrix_diff[i][j]) > 0.01:
                        f.write(f'''Element: {element[0][0]} | Index: {i+1} | Perturbation: {matrix_diff[i]}
''')
                if element_ind[0][j-1] < i <= element_ind[0][j]:
                    if abs(matrix_diff[i][j]) > 0.01:
                        f.write(f'''Element: {element[0][j]} | Index: {i+1} | Perturbation: {matrix_diff[i]}
''')
    return

def convertcif(cif_file,atoms,atom_number):
    doc = cif.read_file(cif_file)
    block = doc.sole_block()
    name = cif_file.strip('.cif')
    len_a = block.find_pair('_cell_length_a')
    len_a = float(len_a[1])
    len_b = block.find_pair('_cell_length_b')
    len_b = float(len_b[1])
    len_c = block.find_pair('_cell_length_c')
    len_c = float(len_c[1])
    alpha = block.find_pair('_cell_angle_alpha')
    alpha = (float(alpha[1]))
    beta = block.find_pair('_cell_angle_beta')
    beta = (float(beta[1]))
    gamma = block.find_pair('_cell_angle_gamma')
    gamma = (float(gamma[1]))
    lattice_list =[]
    lattice_list.append(len_a)
    lattice_list.append(len_b)
    lattice_list.append(len_c)
    lattice_list.append(alpha)
    lattice_list.append(beta)
    lattice_list.append(gamma)
    try:
        atom_num = block.find_pair('_chemical_formula_sum')
        atom_num = atom_num[1][1:-1].split()
        print(atom_num)
        atom_number = []
        for i in range(len(atom_num)):
            store =[]
            for j in atom_num[i]:
                if j.isdigit():
                    store.append(j)
            store = ''.join(store)
            atom_number.append(store)
        atom_number = "    ".join(atom_number)
        atoms=list(block.find_loop('_atom_type_symbol'))
        for i in range(len(atoms)):
            atoms[i] = atoms[i][:-2]
        atoms = "    ".join(atoms)
    except: pass

    x_pos = list(block.find_loop('_atom_site_fract_x'))
    y_pos = list(block.find_loop('_atom_site_fract_y'))
    z_pos = list(block.find_loop('_atom_site_fract_z'))

    lattice = Lattice.from_parameters(lattice_list[0],lattice_list[1],lattice_list[2],lattice_list[3],lattice_list[4],lattice_list[5])
    

    with open('POSCAR','a') as f:
        f.truncate(0)
        f.write(f'''{name}
   1.00000000000000
    {lattice}
   {atoms}
    {atom_number}
direct
''')
        for i in range(len(x_pos)):
            f.write(f'''     {x_pos[i]}     {y_pos[i]}     {z_pos[i]}
''')

def convert_xyz(file):
    with open(file,'r') as f:
            poscar = []
            for lines in f:
                stripped_lines = lines.strip()
                split_lines = stripped_lines.split()
                poscar.append(split_lines)
    lattice_matrix = np.float_(poscar[2:5])
    frac_coord = np.float_(poscar[8:])
    name = ''.join(poscar[0])
    cart_coord = []
    for i in range(len(frac_coord)):
        cart_coord.append(np.matmul(frac_coord[i],lattice_matrix))
    element = poscar[5]
    element_num = poscar[6]
    element_num = [int(x) for x in element_num]
    cumsum_element = list(np.cumsum(element_num))
    element_list =[]
    for i in range(len(element)):
        element_list.append(f'{element[i]} '*int(element_num[i]))
    for i in range(len(element_list)):
        element_list[i] = ' '.join(element_list[i].split())
    element_list = ' '.join(element_list)
    element_list = element_list.split()

    with open('POSCAR.xyz','a') as f:
        f.truncate(0)
        f.write(f'''{len(cart_coord)}
{name}
''')
    with open('POSCAR.xyz','a') as f:
        for i in range(len(cart_coord)):
            f.write(f'''{element_list[i]}    {float(cart_coord[i][0])}    {float(cart_coord[i][1])}    {float(cart_coord[i][2])}   
''')  

def plot_BandStruct_DOS(dos_path,bandstruct_path,title,dos_xlim_min,dos_xlim_max,dos_ylim_min,dos_ylim_max):
    cwd = os.getcwd()
    os.system(f'cd ~{dos_path}')

    if not os.path.isfile(r"POTCAR"):
        print('''
 ---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                             No 'POTCAR' located in this directory!                          |
|                                                                                             |
 ---------------------------------------------------------------------------------------------     
''')

    #Check to see if VASPRUN.xml is in the directory
    if not os.path.isfile(r"vasprun.xml"):
        print('''
 ---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                           No 'vasprun.xml' located in this directory!                       |
|                                                                                             |
 ---------------------------------------------------------------------------------------------   
''')
    else: pass
    
    base = plt.gca().transData
    rot = transforms.Affine2D().rotate_deg(90)
    fig, axs = plt.subplots(1,2)
    v = Vasprun('vasprun.xml')
    cdos = v.complete_dos
    element_dos = cdos.get_element_dos()
    plotter = DosPlotter()
    plotter.add_dos_dict(element_dos)
    axs[0,0] = plotter.get_plot([dos_xlim_min,dos_xlim_max],[dos_ylim_min,dos_ylim_max],transform= rot+base)
    
    os.system(f'cd ~{bandstruct_path}')
    if not os.path.isfile(r"vasprun.xml"):
        print('''
 ---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                           No 'vasprun.xml' located in this directory!                       |
|                                                                                             |
 ---------------------------------------------------------------------------------------------   
''')
    else: pass
    vaspout = Vasprun('vasprun.xml')
    bandstr =  vaspout.get_band_structure(line_mode=True)
    axs[0,1] = BSPlotter(bandstr).get_plot(ylim=[-12,10])
    os.system(f'cd ~{cwd}')   
    fig.tight_layout()
    image_name = f'{title}.pdf'
    image_format = 'pdf'
    fig.savefig(image_name,format=image_format,dpi=3000)
    #fig.show()

def plot_DOS(DOS_type, element, element_number, orbitals,title,xlim_min,xlim_max,ylim_min,ylim_max):
    # Check to see if the CHGCAR is in the directory and has been printed
    if not os.path.isfile(r"CHGCAR"):
        print('''
 ---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                             No 'CHGCAR' located in this directory!                          |
|                                                                                             |
 ---------------------------------------------------------------------------------------------       
''')
    else: pass

    if os.path.getsize(r"CHGCAR") == 0:
        print('''
 ---------------------------------------------------------------------------------------------
|                                        !!! WARNING !!!                                      |
|                                                                                             |
| The CHGCAR file is empty! Run a non self consistent field (SCF) calculation and specify to  |
| calculate the charges using LCHARG = .TRUE. as an INCAR tag. Then run a non-SCF calculation |
| using ICHARG = 11 to print the calculated charges. NOTE a lower KSPACING value or a more    |
| accurate mesh should be used for the best resolved specrtrum                                |
 ---------------------------------------------------------------------------------------------
''')
    else: pass
    
    #Check to see if the POTCAR is in the directory

    if not os.path.isfile(r"POTCAR"):
        print('''
---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                             No 'POTCAR' located in this directory!                          |
|                                                                                             |
 ---------------------------------------------------------------------------------------------     
''')

    #Check to see if VASPRUN.xml is in the directory
    if not os.path.isfile(r"vasprun.xml"):
        print('''
---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                           No 'vasprun.xml' located in this directory!                       |
|                                                                                             |
 ---------------------------------------------------------------------------------------------   
''')
    else: pass

    if DOS_type == 'total':
        v = Vasprun('vasprun.xml')
        cdos = v.complete_dos
        element_dos = cdos.get_element_dos()
        plotter = DosPlotter()
        plotter.add_dos_dict(element_dos)
        plot = plotter.get_plot([xlim_min,xlim_max],[ylim_min,ylim_max])
        plot.tight_layout()
        image_name = f'{title}.pdf'
        image_format = 'pdf'
        plot.savefig(image_name,format=image_format,dpi=3000)
        # plot.show()              
        
    
    if DOS_type == 'orbital':
        if orbitals == "d":
            dosrun = Vasprun("vasprun.xml")
            dos = dosrun.complete_dos
            plotter = DosPlotter()
            pdos = dos.get_element_spd_dos(f'{element}')
            for i in [element_number]:
                pdos1 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.dxy)
                pdos2 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.dxz)
                pdos3 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.dyz)
                pdos4 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.dz2)
                pdos5 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.dx2)
                plotter.add_dos(r'$dz^2$', pdos4)
                plotter.add_dos(r'$dx^2-y^2$', pdos5)
                plotter.add_dos("dyx", pdos1)
                plotter.add_dos("dxz", pdos2)
                plotter.add_dos("dyz", pdos3)
                plot = plotter.get_plot([xlim_min,xlim_max],[ylim_min,ylim_max])
                image_name = f'{title}_{element}{element_number}_{orbitals}.jpeg'
                image_format = 'jpeg'
                plot.savefig(image_name,format=image_format,dpi=3000)
                plot.show()
        
    if orbitals == 'f':
        dosrun = Vasprun("vasprun.xml")
        dos = dosrun.complete_dos
        plotter = DosPlotter()
        pdos = dos.get_element_spd_dos(f'{element}')
        for i in [int(element_number)]:
            pdos1 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f0)
            pdos2 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f1)
            pdos3 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f2)
            pdos4 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f3)
            pdos5 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f_1)
            pdos6 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f_2)
            pdos7 = dos.get_site_orbital_dos(dosrun.final_structure.sites[i], Orbital.f_3)
            plotter.add_dos('f0',pdos1)
            plotter.add_dos('f1',pdos2)
            plotter.add_dos('f2',pdos3)
            plotter.add_dos('f3',pdos4)
            plotter.add_dos('f_1',pdos5)
            plotter.add_dos('f_2',pdos6)
            plotter.add_dos('f_3',pdos7)
            plot = plotter.get_plot([xlim_min,xlim_max],[ylim_min,ylim_max])
            image_name = f'{title}_{element}{element_number}_{orbitals}.jpeg'
            image_format = 'jpeg'
            plot.savefig(image_name,format=image_format,dpi=3000)
            plot.show()

def generate_bandstructure_kpoints(structure):
    struct = Structure.from_file(structure)
    kpath = HighSymmKpath(struct)
    kpts = Kpoints.automatic_linemode(divisions=40,ibz=kpath)
    if os.path.isfile('KPOINTS'):
        kpts.write_file('KPOINTS_ncs')
        os.system('mv KPOINTS_ncs KPOINTS')
    else:
        kpts.write_file('KPOINTS')

def plot_bandstructure(title):
    #Check that there is a 'vasprun.xml' file in the directory
    if not os.path.isfile(r"vasprun.xml"):
        print('''
---------------------------------------------------------------------------------------------
|                                                                                             |
|                                        !!! WARNING !!!                                      |
|                                                                                             |
|                           No 'vasprun.xml' located in this directory!                       |
|                                                                                             |
 ---------------------------------------------------------------------------------------------   
''')
    else: pass

    vaspout = Vasprun('vasprun.xml')
    bandstr =  vaspout.get_band_structure(line_mode=True)
    plt = BSPlotter(bandstr).get_plot(ylim=[-12,10])
    image_name = f'{title}_bandstructure.pdf'
    image_format = 'pdf'
    plt.savefig(image_name,image_format,dpi=3000)
    plt.show()

#Call functions with args
def generate_input_func(args):

    generate_input(
        calc_type=args.calc_type,
        functional=args.functional,
        ENCUT=args.ENCUT,
        mesh=args.mesh
    )

def generate_job_func(args):

    generate_job(
        version=args.version,
        nodes=args.nodes,
        cores=args.cores,
        title=args.title,
        vasp_type=args.vasp_type
    )

def structure_compare_func(args):

    structure_compare(
        path1=args.eq_path,
        path2=args.pert_path
    )

def convert_cif_func(args):

    convertcif(
        cif_file=args.cif_file,
        atoms=args.atoms,
        atom_number=args.atom_number
    )

def convert_to_xyz_func(args):

    convert_xyz(
        file=args.file
    )

def plot_BandStruct_DOS_func(args):
    plot_BandStruct_DOS(
        dos_path=args.dos_path,
        bandstruct_path=args.bandstructure_path,
        title=args.title,
        dos_xlim_min= args.dos_xlim_min,
        dos_xlim_max= args.dos_xlim_max,
        dos_ylim_min= args.dos_ylim_min,
        dos_ylim_max= args.dos_ylim_max,
    )

def plot_dos_func(args):
    
    plot_DOS(
        DOS_type=args.DOS_type,
        element=args.element,
        element_number=args.element_number,
        orbitals=args.orbitals,
        title=args.title,
        xlim_min=args.xlim_min,
        xlim_max=args.xlim_max,
        ylim_min=args.ylim_min,
        ylim_max=args.ylim_max
    )

def generate_bandstructure_kpoints_func(args):

    generate_bandstructure_kpoints(
        structure=args.structure
    )

def plot_bandstructure_func(args):

    plot_bandstructure(
        title=args.title
    )

#Arguments
def read_args(arg_list=None):
    description = dedent(
        '''
        A package for dealing with vasp input and output files.

        avaliable programs:
            vasp_suite generate_input ...
            vasp_suite generate_job ...
            vasp_suite structure_compare ...
            vasp_suite covert_cif ...
            vasp_suite convert_to_xyz ... 
            vasp_suite plot_dos_bandstructure ...
            vasp_suite plot_DOS
            vasp_suite generate_bandstructure_kpoints ...
            vasp_suite plot_bandstructure ...
        '''
    )

    epilog = dedent('''
    To display options for a specific program, use vasp_suite PROGRAMNAME -h
    
    '''
    )
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='prog')

    #generate input files

    gen_inp = subparsers.add_parser(
        'generate_input',
        description='''
        Generation of input files for vasp calculations.

        To generate The INCAR, POTCAR and KPOINTS input files run the following command:
        vasp_suite generate_job --calc_type {arg} --functional {arg} --ENCUT {arg} --mesh {arg}

        If you dont provide positional arguents the default INCAR file generation if for 
        a relaxation calculation using the PBE functional.
        
        for help run the command:
        vasp_suite generate_input --{ARG_NAME} -h

        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    gen_inp.set_defaults(func=generate_input_func)

    gen_inp.add_argument(
        '--calc_type',
        type=str,
        default='Relaxation',
        help='''
        The vasp calculation type:
            relaxation,
            scf (self consistent field),
            efield (electric field)
            molecular_dynamics
        '''
    )
    gen_inp.add_argument(
        '--functional',
        type=str,
        default='PBE',
        help='''
        Avaliable functionals:
            PBE
            PBE0
            PBE+U
            B3LYP
            SCAN
            SCAN+rVV10
        '''
    )
    gen_inp.add_argument(
        '--ENCUT',
        type=str,
        default='520',
        help='''
        Energy cut off value in eV
            Usually 1.3x the maximum value in the POTCAR
        '''
    )
    gen_inp.add_argument(
        '--mesh',
        type=str,
        default='111',
        help='''
        k-point mesh
            input in the following format:
            111
        '''
    )

    submit = subparsers.add_parser(
        'generate_job',
        formatter_class=argparse.RawTextHelpFormatter
    )
    submit.set_defaults(func=generate_job_func)

    #version,nodes,cores,title,vasp_type    
    submit.add_argument(
        '--version',
        type=str,
        default='6.1.2',
        help='''
        CSF4:
                    vasp version:
                        5.4.4
                        6.1.2
        CSF3:
                    do not include '--version' as an argument
        '''
    )

    submit.add_argument(
        '--nodes',
        type=str,
        default='multicore',
        help='''
        job nodes:
            multicore
            multinode
            serial
        '''
    )

    submit.add_argument(
        '--cores',
        type=str,
        default='16',
        help='''
        number of cores
        '''
    )

    submit.add_argument(
        '--title',
        type=str,
        default='VaspJob',
        help='''
        job title
        '''
    )

    submit.add_argument(
        '--vasp_type',
        type=str,
        default='vasp_gam',
        help='''
        vasp type:
            vasp_gam: gamma point mesh
            vasp_std: any other mesh
        '''
    )

    compare = subparsers.add_parser(
        'structure_compare',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    compare.set_defaults(func=structure_compare_func)

    compare.add_argument(
        '--eq_path',
        type=str,
        help='''
        path to the directory of the equilibrium POSCAR
        '''
    )

    compare.add_argument(
        '--pert_path',
        type=str,
        help='''
        path to the directory of the perturbed POSCAR
        '''
    )
    conv = subparsers.add_parser(
        'convert_cif',
        description='''
        this program converts .cif files into POSCAR input files for vasp
            
            to generate the input files using "vasp_suite generat_input" 
            a POSCAR file is required in the directory
            first run "vasp_suite convert_cif --cif_file {file_name}.cif"
            
            if the  .cif file contains the line "_chemical_formual_sum"
            you do NOT need to include the positional arguments:
            --atoms 
            --atom_number
            
            ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    conv.set_defaults(func=convert_cif_func)

    conv.add_argument(
        '--cif_file',
        type=str,
        help='''
        the name of your .cif file
        '''
    )
    conv.add_argument(
        '--atoms',
        type=str,
        help='''
        the order atoms appear in cif file:
            eg. "Dy C H"
            you must include the quotation marks
        '''
    )
    conv.add_argument(
        '--atom_number',
        type=str,
        help='''
        the number of each type of atom in the cif file
        eg "1 2 3"
        you must include the quotation marks
        '''
    )

    xyz = subparsers.add_parser(
        'convert_to_xyz',
        description='''
        this program converst POSCAR files to the .xyz format
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    xyz.set_defaults(func=convert_to_xyz_func)

    xyz.add_argument(
        '--file',
        type=str,
        help='''
        The file you want to convert to .xyz format
            POSCAR
            CONTCAR
        '''
    )
    dos_band = subparsers.add_parser(
    'plot_dos_bandstructure',
    description='''
    Plot the density of states and band structure of a molecule
    or material. 
    for help run the command:
    vasp_suite plot_dos_bandstructure -h
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    dos_band.set_defaults(func=plot_BandStruct_DOS_func)

    dos_band.add_argument(
        '--dos_path',
        type=str,
        help='''
    The path to the density of states (DOS) calculation
    '''
    )

    dos_band.add_argument(
        '--bandstruct_path',
        type=str,
        help='''
    The path to the bandstructure calculation
    '''
    )

    dos_band.add_argument(
        '--title',
        type=str,
        help='''
    The title of the created figure
    '''
    )

    dos_band.add_argument(
        '--dos_xlim_min',
        type=float,
        default = -10,
        help='''
    The boundary limit along the x axis for the density of states plot
    in the form:
    '-x'
    '''
    )

    dos_band.add_argument(
        '--dos_xlim_max',
        type=float,
        default = 10,
        help='''
    The boundary limit along the x axis for the density of states plot
    in the form:
    'x'
    '''
    )


    dos_band.add_argument(
        '--dos_ylim_min',
        type=str,
        default = -10,
        help='''
    The boundary limit along the y axis for the density of states plot
    in the form:
    '-y'
    '''
    )

    dos_band.add_argument(
        '--dos_ylim_max',
        type=str,
        default = 10,
        help='''
    The boundary limit along the y axis for the density of states plot
    in the form:
    'y'
    '''
    )

    DOS = subparsers.add_parser(
        'plot_DOS',
        description='''
        Plotter for density of states calculations
        The plotter can plot the following:
                    Total DOS: The density of states of all atoms in the system
                    Orbital DOS: The density of states of either the d or f orbitals of a specific atom in the system

        For help run the following command:
        'vasp_suite plot_DOS -h'

        when plotting the 'total' density of states the following arguments are not required:
            --element
            --element_number
            --orbitals

        xlim and ylim are defaulted to [-10,10] and [-10,10]
        '''
    )
    DOS.set_defaults(func=plot_dos_func)

    DOS.add_argument(
        '--DOS_type',
        type=str,
        default= 'total',
        help='''
        The type of density of states to plot:
            'total'
            'orbital'
        '''
    )
    DOS.add_argument(
        '--element',
        type=str,
        help='''
        The element symbol of the element you want to plot the orbitals of:
        e.g. 'Dy'
        '''
    )

    DOS.add_argument(
        '--element_number',
        type=int,
        help='''
        The number order of which the element appears in the POSCAR:
        The number ordering starts at 0 for the first atom of that element 
        '''
    )

    DOS.add_argument(
        '--orbitals',
        type=str,
        help='''
        The orbitals that you want to plot:
            'd' or 'f'
        '''
    )

    DOS.add_argument(
        '--title',
        type=str,
        help='''
        The name of the system that you are plotting
        '''
    )

    DOS.add_argument(
        '--xlim_min',
        type=float,
        default= -10,
        help='''
        The x axis min limit for the denisty of states plot
        '''
    )
    DOS.add_argument(
        '--xlim_max',
        type=float,
        default= 10,
        help='''
        The x axis max limit for the denisty of states plot
        '''
    )

    DOS.add_argument(
        '--ylim_min',
        type=float,
        default= -10,
        help='''
        The y axis min limit for the denisty of states plot
        '''
    )
    DOS.add_argument(
        '--ylim_max',
        type=float,
        default= 10,
        help='''
        The y axis max limit for the denisty of states plot
        '''
    )
    
    kp = subparsers.add_parser(
        'generate_bandstructure_kpoints',
        description='''
        A program to generate the KPOINTS input file to calculate the bandstructure
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    kp.set_defaults(func=generate_bandstructure_kpoints_func)

    kp.add_argument(
        '--structure',
        type=str,
        help='''
        The POSCAR or CONTCAR file of the structure you wish to calculate the bandstructure
        '''
    )

    bs = subparsers.add_parser(
        'plot_bandstructure',
        description='''
        Plot the bandstructure
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    bs.set_defaults(func=plot_bandstructure_func)

    bs.add_argument(
        '--title',
        type=str,
        help='''
        The name of the system that your are plotting
        '''
    )

    # read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_known_args(arg_list)

    # select parsing option based on sub-parser
    if args in ['generate_input', 'submission_generator', 'structure_compare','convert_cif','convert_to_xyz','plot_dos_bandstructure','plot_DOS','generate_bandstructure_kpoints','plot_bandstructure']:
        args.func(args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)

def main():
    read_args()

if __name__ == "__main__":
    main()
