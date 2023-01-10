import argparse
from .setup_generator import generate
from ..optimization.optimizer import optimize

def main() -> None:

    # make functions dict 
    functions = {"newsim": generate,
                 "newopti": generate, 
                 "optimize": optimize}

    # Make parser : 
    parser = argparse.ArgumentParser(description='PyCFS command line tool.')

    # Add arguments : 
    parser.add_argument('setup_type', metavar='setup-type', type=str, help='Which setup to generate.')

    parser.add_argument('-s', metavar='--simname', dest="simulation_name", type=str, required=False, default="my_simulation", help='Simulation name to be used.')
    parser.add_argument('-f', metavar='--config', dest="config_file", type=str, required=False, default="config.yaml", help='Name of yaml config file to use.')
    parser.add_argument('-c', metavar='--cfspth', dest="cfs_path", type=str, required=False, default="CFS_PATH", help='Path to OpenCFS on your system.')
    parser.add_argument('-m', metavar='--mesher', dest="mesher_alias", type=str, required=False, default="MESHER_ALIAS", help='Alias for the used mesher if available, else path to mesher.')
    parser.add_argument('-opt', action="store_true", help="Flag to decide if simulation setup is for optimization or not.")

    # Parse and call generator : 
    args = parser.parse_args()

    functions[args.setup_type](args)