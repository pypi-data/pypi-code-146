# The command line interface for vasp_suite

# Imports
import argparse
from textwrap import dedent

# Import the package moddules
from . import input
from . import plotter
from . import file_transform
from . import config

# Wrapper functions for argparse
def generate_input_func(args):
    input.generate_input(
            incar_template=args.incar_template)

def generate_job_func(args):
    input.generate_job(
            job_template=args.job_templatem,
            title=args.title
            )

def convert_cif_func(args):
    file_transform.convert_cif(
            cif_file=args.cif_file)

def convert_xyz_func(args):
    file_transform.convert_xyz()

def plot_dos_func(args):
    plotter.plot_dos(
            dos_type=args.dos_type,
            orbitals=args.orbitals)

def generate_config_func(args):
    config.generate_config(
           config =  args.config_type)

# Parser
def read_args(arg_list=None):
    """Reads the command line arguments and returns them as a dictionary"""
    parser = argparse.ArgumentParser(
        prog='vasp_suite',
        description= dedent(
            '''
            A package for dealing with VASP calculations.
            The package can generate input files, it can perform file transformations including:
                 - .cif
                 - .xyz
                 - POSCAR

             The package contains analysis tools for plotting density of states calculated in vasp.
                            
             Available programs:
                 vasp_suite generate_input ...
                 vasp_suite generate_job ...
                 vasp_suite convert_cif ...
                 vasp_suite convert_xyz ...
                 vasp_suite plot_dos ...
                 vasp_suite generate_config ...
                 '''
                 ),
        epilog = dedent(
            '''To display options for a specific program, use vasp_suite <program> -h'''
            ),

        formatter_class=argparse.RawDescriptionHelpFormatter
        )


    subparsers = parser.add_subparsers(dest='prog')

    gen_inp = subparsers.add_parser(
            'generate_input',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    gen_inp.add_defaults(func=generate_input_func)

    gen_inp.add_argument(
            'incar_template',
            help="The template (.ini) file the INCAR file will be generated from Use input_config.py to generate a template file",
            type=str,
            default='input.ini'
            )

    gen_job = subparsers.add+parser(
            'generate_job',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    gen_job.add_defaults(func=generate_job_func)

    gen_job.add_argument(
            'job_template',
            help=dedent('The template (.ini) file the job script will be generated from.'),
            type=str,
            default='job.ini'
            )
    gen_job.add_argument(
            'title',
            help=dedent('The title of the job. This will be used to name the output files.'),
            type=str,
            default='job'
            )

    conv_cif = subparsers.add_parser(
            'convert_cif',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    conv_cif.add_defaults(func=convert_cif_func)

    conv_cif.add_argument(
            'cif_file',
            help="The .cif file to be converted to POSCAR",
            type=str,
            default='POSCAR'
            )

    conv_xzy = subparsers.add_parser(
            'convert_xyz',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    conv_xyz.add_defaults(func=convert_xyz_func)

    dos = subparsers.add_parser(
            'plot_dos',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    dos.add_defaults(func=plot_dos_func)
    
    dos.add_argument(
            'dos_type',
            help="The type of DOS to be plotted (total, orbital)",
            type=str,
            default='total'
            )

    dos.add_argument(
            '--orbitals',
            help="The orbitals to be plotted (d, f)",
            type=str,
            default='d'
            )

    conf = subparsers.add_parser(
            'generate_config',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    conf.add_defaults(func=generate_config_func)

    conf.add_argument(
            'config_type',
            type = str
            )


    # Read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_known_args(arg_list)

    #select program
    if args in ['generate_input', 'generate_job', 'convert_cif', 'convert_xyz', 'plot_dos', 'generate_config']:
        args.func(args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)

def main():
    read_args()
            


