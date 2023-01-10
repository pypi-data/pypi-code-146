# a module that will write configuration scripts for the user to run to create templates for their calculations
# The required configuration filesn are: input, job, and host

def generate_config_script(config):
    """Generate a configuration script for the user to run to create templates for their calculations.
    The required configuration files are: input, job, and host.
    """
    if config == 'input':
        with open('input_config.py', 'w') as f:
            f.write('''
import configparser as cp

config = cp.ConfigParser()
config['!general'] = {
        'PREC' : 'ACCURATE',
        'LREAL' : '.FALSE.',
        'LASPH' : '.TRUE.',
        'ISMEAR' : 0,
        'SIGMA' : 0.1,
        'NELM' : 100,
        'NELMIN' : 4,
        'NCORE' : 4,
        'EDIFF' : 1e-8,
        'EDIFFG' : -1E-2,}

config['!calc_type'] = {
        'IBRION' : 2,
        'NSW' : 100,
        'ISIF' : 4,
        'POTIM' : 0.5,
        'LWAVE' : '.FALSE.',
        'LCHARG' : '.FALSE.',
        'LORBIT' : 11,}

config['!functional'] = {
        'GGA' : 'PE',}

config['!encut'] = {
        'ENCUT' : 500,}


with open('incar.ini', 'w') as configfile:
    config.write(configfile)
''')
    elif config == 'job':
        with open('job_config.py', 'w') as f:
            f.write('''
import configparser as cp

config = cp.ConfigParser()
config['job'] = {
        'nodes' : 'mutlicore',
        'cores' : 16,
        'module_location' : 'apps/intel-17.0/vasp/6.1.2',
        'vasp_type' : 'vasp_gam'}

with open('job.ini', 'w') as configfile:
    config.write(configfile)
''')
    elif config == 'host':
        with open('host_config.py', 'w') as f:
            f.write('''
import configparser as cp

config = cp.ConfigParser()
config['host'] = {
        # The name of the host
        'hostname' : 'localhost',
        # The architecture of the host (e.g. slurm, sqe, local)
        'architecture' : 'local',
        # The loacation of the potpaw psuedopotential files 
        'potpaw' : '/home/username/potpaw',}

with open('host.ini', 'w') as configfile:
    config.write(configfile)
''')

