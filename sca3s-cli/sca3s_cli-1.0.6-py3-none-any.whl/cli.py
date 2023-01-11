import argparse
import sca3s_cli.functions as functions
from rich import print as rprint


def parse_args():
    """
    Parse CLI arguments given to sca3s_cli.
    """
    parser = argparse.ArgumentParser(description='SCA3S CLI')
    parser.add_argument('function', help='SCA3S function to utilise')
    parser.add_argument('-f', '--file', help='File path of SCA3S compatible JSON')
    parser.add_argument('-j', '--job', help='SCA3S Job ID')
    parser.add_argument('-s', '--scope', help='Credential scope of SCA3S', default='default')
    args = parser.parse_args()
    return args


def main():
    """
    Main invocation point for sca3s_cli
    """
    args = parse_args()
    if args.function == 'submit-job':
        functions.submit_job(args)
    elif args.function == 'list-jobs':
        functions.list_jobs(args)
    elif args.function == 'get-job':
        functions.get_job(args)
    elif args.function == 'delete-job':
        functions.delete_job(args)
    else:
        rprint('Requested function is not defined.')
        return 1


if __name__ == '__main__':
    main()